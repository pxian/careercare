# Generated by Django 3.1.3 on 2021-01-22 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210123_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_exp',
            name='description',
            field=models.CharField(blank='True', default='', max_length=10000),
        ),
    ]