# Generated by Django 2.0.2 on 2018-08-21 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20180820_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='join_mailing_list',
            field=models.BooleanField(default=False),
        ),
    ]
