# Generated by Django 3.1.3 on 2021-01-20 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_cand', '0005_auto_20210121_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcand',
            name='link',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
