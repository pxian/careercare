# Generated by Django 3.0.7 on 2020-12-24 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0017_auto_20201218_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='unprocessed',
            name='status',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
