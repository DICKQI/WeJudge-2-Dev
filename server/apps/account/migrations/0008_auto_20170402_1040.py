# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-02 02:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_account_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='cookie_token',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
