# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-19 06:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0002_auto_20161216_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemset',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pset_manager', to='account.Account'),
        ),
    ]
