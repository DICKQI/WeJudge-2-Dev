# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-28 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0024_problemsetsolution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemsetsolution',
            name='best_code_size',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='problemsetsolution',
            name='best_memory',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='problemsetsolution',
            name='best_time',
            field=models.IntegerField(default=-1),
        ),
    ]
