# Generated by Django 3.1.3 on 2021-01-16 19:49

from django.db import migrations, models
import resumeanalyzer.models


class Migration(migrations.Migration):

    dependencies = [
        ('resumeanalyzer', '0015_auto_20210115_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobdesc',
            name='jobdesc',
            field=models.FileField(storage=resumeanalyzer.models.FailOnDuplicateFileSystemStorage(), unique=True, upload_to='jobdesc/', verbose_name='Upload Job Description'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='resume',
            field=models.FileField(storage=resumeanalyzer.models.FailOnDuplicateFileSystemStorage(), unique=True, upload_to='resumes/', verbose_name='Upload Resumes'),
        ),
    ]