# Generated by Django 3.1.3 on 2021-01-22 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210123_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_exp',
            name='duration',
            field=models.CharField(blank='True', default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='employee_exp',
            name='position_level',
            field=models.CharField(blank='True', choices=[('Senior Manager', 'Senior Manager'), ('Manager', 'Manager'), ('Senior Executive', 'Senior Executive'), ('Junior Executive', 'Junior Executive'), ('Fresh / Entry Level', 'Fresh / Entry Level'), ('Non-Executive', 'Non-Executive')], default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='employee_exp',
            name='state',
            field=models.CharField(blank='True', default='', max_length=1000),
        ),
    ]
