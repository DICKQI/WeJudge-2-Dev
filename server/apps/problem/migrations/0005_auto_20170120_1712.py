# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-20 09:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0004_auto_20170120_1350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='count_ac',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='count_sub',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='judge_fs_root',
        ),
    ]
