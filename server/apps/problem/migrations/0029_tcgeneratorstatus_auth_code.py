# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-19 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0028_auto_20170819_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='tcgeneratorstatus',
            name='auth_code',
            field=models.CharField(default='', max_length=200),
        ),
    ]