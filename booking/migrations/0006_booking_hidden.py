# Generated by Django 3.0.7 on 2020-12-07 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_booking_reasons'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='hidden',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
