# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-28 15:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wejudge.db.converter


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20170607_2106'),
        ('problem', '0023_problem_single_testcase'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemSetSolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.IntegerField(default=0)),
                ('submission', models.IntegerField(default=0)),
                ('penalty', models.IntegerField(default=0)),
                ('best_memory', models.IntegerField(default=0)),
                ('best_time', models.IntegerField(default=0)),
                ('best_code_size', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('first_ac_time', models.DateTimeField(blank=True, null=True)),
                ('used_time', models.FloatField(default=0)),
                ('used_time_real', models.FloatField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.Problem')),
                ('problemset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.ProblemSet')),
                ('virtual_problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.ProblemSetItem')),
            ],
            options={
                'verbose_name_plural': '题目集的题目解决情况',
                'verbose_name': '题目集的题目解决情况',
            },
            bases=(models.Model, wejudge.db.converter.ModelConverter),
        ),
    ]