# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-20 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0025_asgnproblem_hidden_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='asgn',
            name='public_answer_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
