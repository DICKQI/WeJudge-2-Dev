# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-18 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0016_contest_enable_printer_queue'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestaccount',
            name='passwd_retry_counter',
            field=models.SmallIntegerField(default=10),
        ),
    ]