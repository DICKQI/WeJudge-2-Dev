# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 00:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wejudge.db.converter


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20170905_0032'),
        ('problem', '0029_tcgeneratorstatus_auth_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeDrafts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, default='')),
                ('lang', models.SmallIntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.Problem')),
            ],
            bases=(models.Model, wejudge.db.converter.ModelConverter),
        ),
    ]
