# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-09 08:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0008_auto_20170308_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='eduschool',
            name='now_term',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.EduYearTerm'),
        ),
    ]
