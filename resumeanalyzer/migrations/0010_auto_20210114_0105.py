# Generated by Django 3.1.3 on 2021-01-13 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumeanalyzer', '0009_auto_20210114_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='summary',
            field=models.CharField(blank=True, max_length=10000, null=True, verbose_name='Summary'),
        ),
    ]
