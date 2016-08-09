# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-04 07:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='cmds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20, verbose_name=b'User name')),
                ('md5_name', models.CharField(max_length=32, verbose_name=b'MD5 name')),
                ('cmd_path', models.CharField(max_length=32, verbose_name=b'Command Path')),
                ('cmd', models.CharField(max_length=256, verbose_name=b'Command run')),
                ('cmd_status', models.CharField(max_length=20, verbose_name=b'Command status')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'Create time')),
                ('update_time', models.DateTimeField(default=datetime.datetime(2016, 4, 4, 15, 37, 57, 429000), verbose_name=b'update time')),
            ],
            options={
                'db_table': 'Commands',
                'verbose_name': 'Commands run',
                'verbose_name_plural': 'Commands run',
            },
        ),
        migrations.DeleteModel(
            name='Advertisement',
        ),
    ]