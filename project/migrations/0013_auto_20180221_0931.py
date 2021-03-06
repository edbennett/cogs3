# Generated by Django 2.0.2 on 2018-02-21 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_auto_20180220_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='legacy_id',
        ),
        migrations.AddField(
            model_name='project',
            name='legacy_arcca_id',
            field=models.CharField(blank=True, help_text='Project legacy ID ARCCA', max_length=50, verbose_name='Legacy ARCCA ID'),
        ),
        migrations.AddField(
            model_name='project',
            name='legacy_hpcw_id',
            field=models.CharField(blank=True, help_text='Project legacy ID from HPC Wales', max_length=50, verbose_name='Legacy HPC Wales ID'),
        ),
    ]
