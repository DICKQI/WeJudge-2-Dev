# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-15 01:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20170120_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='permission_administrator',
            field=models.BooleanField(default=False),
        ),
    ]
