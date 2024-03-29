# Generated by Django 3.1.3 on 2021-01-15 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resumeanalyzer', '0011_jobdesc_jobtext'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='jobid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='resumeanalyzer.jobdesc'),
        ),
        migrations.AddField(
            model_name='resume',
            name='rate',
            field=models.FloatField(default=0),
        ),
    ]
