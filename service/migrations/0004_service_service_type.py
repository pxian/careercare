# Generated by Django 3.0.7 on 2020-11-28 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_service_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
