# Generated by Django 2.0.2 on 2018-05-01 14:02

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('institution', '0004_auto_20180326_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('is_shibboleth_login_required', models.BooleanField(default=True, help_text='Designates whether this user is required to login via a shibboleth identity provider.', verbose_name='shibboleth login required status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scw_username', models.CharField(blank=True, max_length=50, verbose_name='SCW username')),
                ('hpcw_username', models.CharField(blank=True, max_length=50, verbose_name='HPCW username')),
                ('hpcw_email', models.EmailField(blank=True, max_length=100, verbose_name='HPCW email address')),
                ('raven_username', models.CharField(blank=True, max_length=50, verbose_name='Raven username')),
                ('raven_email', models.EmailField(blank=True, max_length=100, verbose_name='Raven email address')),
                ('description', models.CharField(blank=True, max_length=200)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('account_status', models.PositiveSmallIntegerField(choices=[(1, 'Awaiting Approval'), (2, 'Approved'), (3, 'Declined'), (4, 'Revoked'), (5, 'Suspended'), (6, 'Closed')], default=1)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
        ),
        migrations.CreateModel(
            name='ShibbolethProfile',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.Profile')),
                ('shibboleth_id', models.CharField(blank=True, help_text='Institutional address', max_length=50)),
                ('department', models.CharField(blank=True, max_length=128)),
                ('orcid', models.CharField(blank=True, help_text='16-digit ORCID', max_length=16)),
                ('scopus', models.URLField(blank=True, help_text='Scopus URL')),
                ('homepage', models.URLField(blank=True)),
                ('cronfa', models.URLField(blank=True, help_text='Cronfa URL')),
                ('institution', models.ForeignKey(help_text='Institution user is based', on_delete=django.db.models.deletion.CASCADE, to='institution.Institution')),
            ],
            bases=('users.profile',),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
