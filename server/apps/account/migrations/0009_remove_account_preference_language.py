# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-07 15:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20170402_1040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='preference_language',
        ),
    ]
