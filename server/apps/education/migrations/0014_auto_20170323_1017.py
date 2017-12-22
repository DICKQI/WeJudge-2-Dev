# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-23 02:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0013_auto_20170321_0859'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AsgnProblems',
            new_name='AsgnProblem',
        ),
        migrations.RenameField(
            model_name='asgn',
            old_name='problemset',
            new_name='problems',
        ),
        migrations.RenameField(
            model_name='solution',
            old_name='problems',
            new_name='problem',
        ),
        migrations.RemoveField(
            model_name='problemsetitem',
            name='permission',
        ),
        migrations.AlterField(
            model_name='asgnproblem',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.Problem'),
        ),
    ]
