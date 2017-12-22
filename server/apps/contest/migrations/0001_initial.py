# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-05 01:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import wejudge.db.converter


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('problem', '0013_auto_20170403_1512'),
        ('account', '0008_auto_20170402_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('sponsor', models.TextField(blank=True, default='')),
                ('pause', models.BooleanField(default=False)),
                ('lang', models.SmallIntegerField(default=0)),
                ('rank_list', models.TextField(blank=True, default='')),
                ('rank_list_cache_time', models.IntegerField(default=0)),
                ('rank_list_stop_at', models.DateTimeField(blank=True, null=True)),
                ('penalty_items', models.CharField(blank=True, default='1,2,3,4,5,6', max_length=100)),
                ('penalty_time', models.TimeField(default=datetime.time(0, 20))),
                ('rank_list_cache_before_stop', models.TextField(blank=True, default='')),
                ('hide_problem_title', models.BooleanField(default=False)),
                ('cross_check', models.BooleanField(default=False)),
                ('cross_check_ratio', models.FloatField(default=0.8)),
            ],
            options={
                'verbose_name': '比赛信息',
                'verbose_name_plural': '比赛信息',
            },
            bases=(models.Model, wejudge.db.converter.ModelConverter),
        ),
        migrations.CreateModel(
            name='ContestAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('sex', models.SmallIntegerField(choices=[(-1, '未知'), (0, '女'), (1, '男')], default=-1)),
                ('nickname', models.CharField(blank=True, max_length=50, null=True)),
                ('realname', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('headimg', models.CharField(blank=True, max_length=50, null=True)),
                ('motto', models.CharField(blank=True, max_length=255, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_login_time', models.DateTimeField(blank=True, null=True)),
                ('locked', models.BooleanField(default=False)),
                ('role', models.SmallIntegerField(default=0)),
                ('can_bind_master', models.BooleanField(default=True)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.Contest')),
                ('master', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
            options={
                'verbose_name': '比赛服账户',
                'verbose_name_plural': '比赛服账户',
            },
        ),
        migrations.CreateModel(
            name='ContestCodeAnalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('levenshtein_similarity_ratio', models.FloatField(default=0)),
                ('contest', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='contest.Contest')),
            ],
            options={
                'verbose_name': '比赛-简单代码查重',
                'verbose_name_plural': '比赛-简单代码查重',
            },
        ),
        migrations.CreateModel(
            name='ContestProblem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(default=0)),
                ('accepted', models.IntegerField(default=0)),
                ('submission', models.IntegerField(default=0)),
                ('lang', models.SmallIntegerField(default=0)),
                ('status_editable', models.BooleanField(default=False)),
                ('entity', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='problem.Problem')),
            ],
            options={
                'verbose_name': '比赛题目设置',
                'verbose_name_plural': '比赛题目设置',
            },
            bases=(models.Model, wejudge.db.converter.ModelConverter),
        ),
        migrations.CreateModel(
            name='ContestSolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.IntegerField(default=0)),
                ('submission', models.IntegerField(default=0)),
                ('penalty', models.IntegerField(default=0)),
                ('first_ac_time', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='contest.ContestAccount')),
                ('contest', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='contest.Contest')),
            ],
            options={
                'verbose_name': '比赛题目-解决情况',
                'verbose_name_plural': '比赛题目-解决情况',
            },
            bases=(models.Model, wejudge.db.converter.ModelConverter),
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('content', models.TextField(blank=True, default='')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('answer_content', models.TextField(blank=True, default='')),
                ('answer_time', models.DateTimeField(auto_now=True)),
                ('is_private', models.BooleanField(default=True)),
                ('answer_referee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_referees', to='contest.ContestAccount')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.ContestAccount')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.Contest')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contest.FAQ')),
            ],
            options={
                'verbose_name': '比赛题目-问答系统',
                'verbose_name_plural': '比赛题目-问答系统',
            },
        ),
        migrations.CreateModel(
            name='JudgeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag', models.SmallIntegerField(default=-2)),
                ('lang', models.SmallIntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('exe_time', models.IntegerField(default=0)),
                ('exe_mem', models.IntegerField(default=0)),
                ('code_len', models.IntegerField(default=0)),
                ('code_path', models.CharField(default='', max_length=255)),
                ('result', models.TextField(blank=True, default='', null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contest.ContestAccount')),
                ('problem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contest_status_problem', to='problem.Problem')),
                ('virtual_problem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contest_status_vproblem', to='contest.ContestProblem')),
            ],
            options={
                'verbose_name': '比赛-评测记录',
                'verbose_name_plural': '比赛-评测记录',
            },
            bases=(models.Model, wejudge.db.converter.ModelConverter),
        ),
        migrations.AddField(
            model_name='contestsolution',
            name='judge_status',
            field=models.ManyToManyField(blank=True, to='contest.JudgeStatus'),
        ),
        migrations.AddField(
            model_name='contestsolution',
            name='problem',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='contest.ContestProblem'),
        ),
        migrations.AddField(
            model_name='contestcodeanalysis',
            name='problem',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='contest.ContestProblem'),
        ),
        migrations.AddField(
            model_name='contestcodeanalysis',
            name='status1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status1', to='contest.JudgeStatus'),
        ),
        migrations.AddField(
            model_name='contestcodeanalysis',
            name='status2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status2', to='contest.JudgeStatus'),
        ),
        migrations.AddField(
            model_name='contest',
            name='cross_check_ignore_problem',
            field=models.ManyToManyField(blank=True, related_name='cc_ignore_problem', to='contest.ContestProblem'),
        ),
        migrations.AddField(
            model_name='contest',
            name='judge_status',
            field=models.ManyToManyField(blank=True, to='contest.JudgeStatus'),
        ),
        migrations.AddField(
            model_name='contest',
            name='problems',
            field=models.ManyToManyField(blank=True, to='contest.ContestProblem'),
        ),
    ]