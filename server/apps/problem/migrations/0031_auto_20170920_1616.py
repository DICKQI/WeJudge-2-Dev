# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-20 16:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0030_codedrafts'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='codedrafts',
            options={'verbose_name': '用户草稿箱', 'verbose_name_plural': '用户草稿箱'},
        ),
    ]