# Generated by Django 3.0.7 on 2020-06-11 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employers', '0003_auto_20200608_0610'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_title', models.CharField(max_length=100, null=True)),
                ('employment_type', models.CharField(max_length=100, null=True)),
                ('position_level', models.CharField(max_length=100, null=True)),
                ('job_specialization', models.CharField(max_length=100, null=True)),
                ('job_requirements', models.TextField(null=True)),
                ('state', models.CharField(max_length=100, null=True)),
                ('area', models.CharField(max_length=100, null=True)),
                ('monthly_salary', models.CharField(max_length=100, null=True)),
                ('opening_date', models.DateField(auto_now_add=True)),
                ('closing_date', models.DateField(null=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employers.Employer')),
            ],
        ),
    ]
