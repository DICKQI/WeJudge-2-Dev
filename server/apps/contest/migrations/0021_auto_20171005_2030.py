# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-05 20:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0020_auto_20170824_2100'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contestsolution',
            unique_together=set([('author', 'contest', 'problem')]),
        ),
    ]