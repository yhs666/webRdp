# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-16 01:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20160424_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name=b'User name')),
                ('hash', models.CharField(max_length=32, verbose_name=b'MD5 name')),
                ('cmd', models.CharField(max_length=256, verbose_name=b'Command run')),
                ('submit', models.CharField(max_length=50, verbose_name=b'submit command')),
                ('jumpboxrun', models.DateTimeField(verbose_name=b'Run in Jumpbox')),
                ('cmddone', models.DateTimeField(verbose_name=b'cmd done')),
                ('cmdstatus', models.CharField(max_length=50, verbose_name=b'cmd done status')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'Create time')),
            ],
            options={
                'db_table': 'Commands logs',
                'verbose_name': 'Commands logs',
                'verbose_name_plural': 'Commands logs',
            },
        ),
        migrations.AlterModelOptions(
            name='cluster',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='cmds',
            name='update_time',
        ),
    ]
