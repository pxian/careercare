# Generated by Django 3.0.7 on 2020-12-02 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_booking_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='reasons',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
