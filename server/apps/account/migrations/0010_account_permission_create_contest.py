# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-19 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_remove_account_preference_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='permission_create_contest',
            field=models.BooleanField(default=False),
        ),
    ]