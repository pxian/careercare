# Generated by Django 3.0.7 on 2020-06-11 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0004_auto_20200611_0345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobad',
            name='employer',
        ),
    ]
