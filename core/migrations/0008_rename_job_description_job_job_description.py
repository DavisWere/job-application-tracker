# Generated by Django 5.0.6 on 2024-06-22 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_rename_job_title_job_job_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='Job_description',
            new_name='job_description',
        ),
    ]