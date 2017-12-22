# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-07 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_auto_20170405_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestsolution',
            name='best_code_size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='contestsolution',
            name='best_memory',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='contestsolution',
            name='best_time',
            field=models.IntegerField(default=0),
        ),
    ]