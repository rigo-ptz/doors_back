# Generated by Django 2.0.2 on 2018-04-08 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doors', '0007_lesson_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='keycell',
            name='user_who_get',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]