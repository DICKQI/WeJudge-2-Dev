# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-03 06:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0016_auto_20170331_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='judgestatus',
            name='virtual_problem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asgn_status_vproblem', to='education.AsgnProblem'),
        ),
        migrations.AlterField(
            model_name='judgestatus',
            name='problem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asgn_status_problem', to='problem.Problem'),
        ),
    ]
