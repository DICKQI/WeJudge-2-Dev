# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-14 14:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountProblemVisited',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submissions', models.IntegerField(default=0)),
                ('accepted', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
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
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('difficulty', models.SmallIntegerField(choices=[(0, '未分级'), (1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')], default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(default='')),
                ('input', models.TextField(default='')),
                ('output', models.TextField(default='')),
                ('sample_input', models.TextField(default='')),
                ('sample_output', models.TextField(default='')),
                ('hint', models.TextField(default='')),
                ('source', models.TextField(default='')),
                ('problem_type', models.SmallIntegerField(choices=[(0, '正常模式'), (1, '代码填空模式'), (2, '手动批改模式')], default=0)),
                ('lang', models.SmallIntegerField(default=0)),
                ('judge_fs_root', models.CharField(default='', max_length=255)),
                ('judge_config', models.TextField(default='')),
                ('pause_judge', models.BooleanField(default=True)),
                ('count_sub', models.IntegerField(default=0)),
                ('count_ac', models.IntegerField(default=0)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemClassify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='problem.ProblemClassify')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('description', models.TextField(default='')),
                ('image', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProblemSetItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.SmallIntegerField(default=0)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.Problem')),
            ],
        ),
        migrations.CreateModel(
            name='TDGeneratorStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag', models.SmallIntegerField(default=0)),
                ('exe_time', models.IntegerField(default=0)),
                ('exe_mem', models.IntegerField(default=0)),
                ('lang', models.SmallIntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.Problem')),
            ],
        ),
        migrations.AddField(
            model_name='problemset',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='pset_items', to='problem.ProblemSetItem'),
        ),
        migrations.AddField(
            model_name='problemset',
            name='judge_status',
            field=models.ManyToManyField(blank=True, related_name='pset_judge_status', to='problem.JudgeStatus'),
        ),
        migrations.AddField(
            model_name='problemset',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pset_manager', to='account.Account'),
        ),
        migrations.AddField(
            model_name='problem',
            name='classifications',
            field=models.ManyToManyField(blank=True, to='problem.ProblemClassify'),
        ),
        migrations.AddField(
            model_name='judgestatus',
            name='problem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='problem.ProblemSetItem'),
        ),
        migrations.AddField(
            model_name='accountproblemvisited',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.Problem'),
        ),
    ]