# Generated by Django 2.0.2 on 2018-04-07 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doors', '0006_auto_20180407_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]