# Generated by Django 2.0.2 on 2018-06-19 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180619_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account_status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Awaiting Approval'), (1, 'Approved'), (2, 'Declined'), (3, 'Revoked'), (4, 'Suspended'), (5, 'Closed')], default=0, verbose_name='Current Status'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='previous_account_status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Awaiting Approval'), (1, 'Approved'), (2, 'Declined'), (3, 'Revoked'), (4, 'Suspended'), (5, 'Closed')], default=0, verbose_name='Previous Status'),
        ),
    ]
