# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-20 05:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0003_auto_20170119_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='classifications',
        ),
        migrations.RemoveField(
            model_name='problemclassify',
            name='author',
        ),
        migrations.AddField(
            model_name='problemclassify',
            name='problemset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='problem.ProblemSet'),
        ),
        migrations.AddField(
            model_name='problemsetitem',
            name='accepted',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='problemsetitem',
            name='classifications',
            field=models.ManyToManyField(blank=True, to='problem.ProblemClassify'),
        ),
        migrations.AddField(
            model_name='problemsetitem',
            name='submission',
            field=models.IntegerField(default=0),
        ),
    ]
