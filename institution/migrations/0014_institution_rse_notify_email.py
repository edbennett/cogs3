# Generated by Django 2.0.2 on 2018-08-16 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0013_institution_allows_rse_requests'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='rse_notify_email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]