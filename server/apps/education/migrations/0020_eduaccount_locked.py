# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-05 00:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0019_auto_20170404_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='eduaccount',
            name='locked',
            field=models.BooleanField(default=False),
        ),
    ]