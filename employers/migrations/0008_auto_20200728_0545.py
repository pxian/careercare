# Generated by Django 3.0.7 on 2020-07-28 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employers', '0007_auto_20200728_0539'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employer',
            old_name='location',
            new_name='address',
        ),
    ]
