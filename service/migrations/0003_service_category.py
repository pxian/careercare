# Generated by Django 3.0.7 on 2020-11-21 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20201121_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='category',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
