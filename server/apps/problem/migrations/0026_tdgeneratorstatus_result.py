# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-18 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0025_auto_20170728_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='tdgeneratorstatus',
            name='result',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
