# Generated by Django 3.0.7 on 2021-01-10 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0021_auto_20210110_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobad',
            name='max_salary',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='jobad',
            name='min_salary',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
