# Generated by Django 3.1.3 on 2021-01-15 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resumeanalyzer', '0012_auto_20210115_1320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobdesc',
            name='jobtext',
        ),
        migrations.AlterField(
            model_name='resume',
            name='jobid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumeanalyzer.jobdesc'),
        ),
    ]
