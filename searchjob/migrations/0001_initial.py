# Generated by Django 3.1.3 on 2021-01-22 17:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Freelance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, null=True)),
                ('job_title', models.CharField(max_length=100, null=True)),
                ('category', models.CharField(blank='True', default='', max_length=100)),
                ('job_type', models.CharField(blank='True', default='', max_length=100)),
                ('job_description', models.CharField(blank='True', default='', max_length=500)),
                ('city', models.CharField(blank='True', default='', max_length=100)),
                ('working_hour', models.CharField(blank='True', default='', max_length=100)),
                ('pay', models.CharField(blank='True', default='', max_length=100)),
                ('industry', models.CharField(blank='True', default='', max_length=100)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, null=True)),
                ('position_title', models.CharField(max_length=100, null=True)),
                ('employment_type', models.CharField(max_length=100, null=True)),
                ('position_level', models.CharField(max_length=100, null=True)),
                ('job_specialization', models.CharField(max_length=100, null=True)),
                ('job_description', models.TextField(null=True)),
                ('job_requirements', models.TextField(null=True)),
                ('location', models.TextField(null=True)),
                ('salary', models.CharField(blank=True, max_length=100, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ViewedJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('jobad', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='searchjob.jobad')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ViewedFree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('freelance', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='searchjob.freelance')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('title', models.CharField(max_length=100, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('price', models.IntegerField(blank='True', default=0)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AppliedJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Application Processing', max_length=100, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('jobad', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='job_applied', to='searchjob.jobad')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AppliedFree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Application Processing', max_length=100, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('freelance', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='searchjob.freelance')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
