# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-06 05:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20160406_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmds',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 6, 13, 2, 4, 422000), verbose_name=b'update time'),
        ),
    ]
