# Generated by Django 5.0.6 on 2024-06-22 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_jobs_type_of_job_jobs_date_posted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='application_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='date_posted',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
