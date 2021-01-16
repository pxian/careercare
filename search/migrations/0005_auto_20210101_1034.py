# Generated by Django 3.0.7 on 2021-01-01 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('test_cand', '0004_auto_20201218_1644'),
        ('search', '0004_tsearch'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('messages', models.TextField(null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('cand', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='test_cand.TestCand')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='TSearch',
        ),
    ]
