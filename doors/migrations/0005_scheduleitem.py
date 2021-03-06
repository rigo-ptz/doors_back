# Generated by Django 2.0.2 on 2018-04-06 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doors', '0004_auto_20180404_2346'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField(verbose_name='Время начала')),
                ('time_end', models.DateTimeField(verbose_name='Время окончания')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doors.Room')),
            ],
            options={
                'verbose_name': 'Занятие',
                'verbose_name_plural': 'Занятия',
            },
        ),
    ]
