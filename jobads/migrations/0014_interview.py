# Generated by Django 3.0.7 on 2020-12-09 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_cand', '0003_auto_20201129_0946'),
        ('jobads', '0013_jobad_closing_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('interview', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='test_cand.TestCand')),
                ('jobad', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='jobads.JobAd')),
            ],
        ),
    ]
