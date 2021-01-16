# Generated by Django 3.1.3 on 2021-01-13 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import resumeanalyzer.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resumeanalyzer', '0006_auto_20210113_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobdesc',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resume',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='jobdesc',
            name='jobdesc',
            field=models.FileField(blank=True, null=True, storage=resumeanalyzer.models.FailOnDuplicateFileSystemStorage(), unique=True, upload_to='jobdesc/', verbose_name='Upload Job Description'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='resume',
            field=models.FileField(blank=True, null=True, storage=resumeanalyzer.models.FailOnDuplicateFileSystemStorage(), unique=True, upload_to='resumes/', verbose_name='Upload Resumes'),
        ),
    ]
