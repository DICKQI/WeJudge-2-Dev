# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-20 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0039_asgn_archive_lock'),
    ]

    operations = [
        migrations.AddField(
            model_name='asgnreport',
            name='attachment',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
