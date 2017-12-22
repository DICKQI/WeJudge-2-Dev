# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-10 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0009_eduschool_now_term'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='course_student', to='education.EduAccount'),
        ),
    ]
