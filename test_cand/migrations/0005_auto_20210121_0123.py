# Generated by Django 3.1.3 on 2021-01-20 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_cand', '0004_auto_20201218_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcand',
            name='skills',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='testcand',
            name='title',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
