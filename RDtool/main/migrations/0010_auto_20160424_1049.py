# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-24 02:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20160424_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmds',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 24, 10, 49, 28, 847000), verbose_name=b'update time'),
        ),
    ]
