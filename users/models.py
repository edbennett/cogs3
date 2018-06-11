import django_rq

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext as _

from institution.models import Institution
from openldap.api import user_api


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    scw_username = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='SCW username',
    )
    hpcw_username = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='HPCW username',
    )
    hpcw_email = models.EmailField(
        max_length=100,
        blank=True,
        verbose_name='HPCW email address',
    )
    raven_username = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Raven username',
    )
    raven_email = models.EmailField(
        max_length=100,
        blank=True,
        verbose_name='Raven email address',
    )
    uid_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='UID Number',
    )
    description = models.CharField(
        max_length=200,
        blank=True,
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
    )
    AWAITING_APPROVAL = 1
    APPROVED = 2
    DECLINED = 3
    REVOKED = 4
    SUSPENDED = 5
    CLOSED = 6
    STATUS_CHOICES = (
        (AWAITING_APPROVAL, 'Awaiting Approval'),
        (APPROVED, 'Approved'),
        (DECLINED, 'Declined'),
        (REVOKED, 'Revoked'),
        (SUSPENDED, 'Suspended'),
        (CLOSED, 'Closed'),
    )
    account_status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=AWAITING_APPROVAL,
    )

    def account_status_message(self):
        if self.account_status == self.AWAITING_APPROVAL:
            message = _('access request is currently awaiting approval.')
        elif self.account_status == self.APPROVED:
            # TODO - Check if system resources have been allocated
            message = _('access request has been approved and your account is currently being created.')
        elif self.account_status == self.DECLINED:
            message = _('access request has been declined.')
        elif self.account_status == self.REVOKED:
            message = _('access has been revoked.')
        elif self.account_status == self.SUSPENDED:
            message = _('access has been suspended.')
        elif self.account_status == self.CLOSED:
            message = _('has been closed.')
        return _('Your {company_name} account {message}').format(
            company_name=settings.COMPANY_NAME,
            message=message,
        )

    def update_ldap_account(self):
        """
        Ensure account status updates are propogated to the user's LDAP account.
        """
        if self.account_status == self.APPROVED:
            if self.scw_username:
                user_api.activate_user_account.delay(user=self.user)
            else:
                user_api.create_user.delay(user=self.user)
        else:
            user_api.deactivate_user_account.delay(user=self.user)

    def reset_account_status(self):
        """
        Reset user account status to Awaiting Approval.
        """
        self.account_status = Profile.AWAITING_APPROVAL
        self.save()

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'


class ShibbolethProfile(Profile):
    shibboleth_id = models.CharField(
        max_length=50,
        blank=True,
        help_text='Institutional address',
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        help_text='Institution user is based',
    )
    department = models.CharField(
        max_length=128,
        blank=True,
    )
    orcid = models.CharField(
        max_length=16,
        blank=True,
        help_text='16-digit ORCID',
    )
    scopus = models.URLField(
        blank=True,
        help_text='Scopus URL',
    )
    homepage = models.URLField(blank=True)
    cronfa = models.URLField(
        blank=True,
        help_text='Cronfa URL',
    )


class CustomUserManager(BaseUserManager):
    """
    A CustomUser manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager".
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_shibboleth_login_required', False)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_shibboleth_login_required') is not False:
            raise ValueError('Superuser must have is_shibboleth_login_required=False.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField(unique=True, null=True)
    is_shibboleth_login_required = models.BooleanField(
        default=True,
        help_text='Designates whether this user is required to login via a shibboleth identity provider.',
        verbose_name='shibboleth login required status',
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.',
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text='Designates that this user has all permissions without explicitly assigning them.',
        verbose_name='superuser status',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(
        blank=True,
        max_length=30,
        verbose_name='first name',
    )
    last_name = models.CharField(
        blank=True,
        max_length=30,
        verbose_name='last name',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
        if self.is_shibboleth_login_required:
            _, domain = self.email.split('@')
            institution = Institution.objects.get(base_domain=domain)
            ShibbolethProfile.objects.update_or_create(
                user=self,
                defaults={
                    'shibboleth_id': self.email,
                    'institution': institution,
                },
            )
        else:
            Profile.objects.update_or_create(user=self)
        self.profile.save()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Users'
