# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-18 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20170518_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountremembermetokens',
            name='token',
            field=models.CharField(blank=True, db_index=True, default='', max_length=100),
        ),
    ]
