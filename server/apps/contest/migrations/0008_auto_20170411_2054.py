# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-11 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0007_auto_20170411_2045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faq',
            name='children',
        ),
        migrations.AddField(
            model_name='faq',
            name='children',
            field=models.ManyToManyField(blank=True, to='contest.FAQ'),
        ),
    ]
