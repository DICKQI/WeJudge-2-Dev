# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0038_auto_20170816_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='asgn',
            name='archive_lock',
            field=models.BooleanField(default=False),
        ),
    ]
