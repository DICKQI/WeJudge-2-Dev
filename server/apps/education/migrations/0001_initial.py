# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-14 14:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arrangement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
                ('day_of_week', models.IntegerField(default=0)),
                ('start_week', models.IntegerField(default=0)),
                ('end_week', models.IntegerField(default=0)),
                ('odd_even', models.IntegerField(default=0)),
                ('start_section', models.IntegerField(default=0)),
                ('end_section', models.IntegerField(default=0)),
                ('start_time', models.TimeField(default=datetime.time(0, 0))),
                ('end_time', models.TimeField(default=datetime.time(0, 0))),
            ],
        ),
        migrations.CreateModel(
            name='Asgn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('description', models.TextField(default='')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('full_score', models.FloatField(default=0)),
                ('lang', models.SmallIntegerField(default=0)),
                ('rank_list', models.TextField(default='')),
                ('rank_list_cache_time', models.IntegerField(default=0)),
                ('hide_problem_title', models.BooleanField(default=False)),
                ('hide_problem_subcode', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AsgnAccessControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.IntegerField(default=0)),
                ('end_time', models.IntegerField(default=0)),
                ('enabled', models.BooleanField(default=False)),
                ('arrangement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Arrangement')),
            ],
        ),
        migrations.CreateModel(
            name='AsgnProblems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(db_index=True, default=0)),
                ('accepted', models.IntegerField(default=0)),
                ('submission', models.IntegerField(default=0)),
                ('require', models.BooleanField(default=False)),
                ('score', models.FloatField(default=0)),
                ('lang', models.SmallIntegerField(default=0)),
                ('ignore_pe', models.BooleanField(default=True)),
                ('pe_score', models.IntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='AsgnReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judge_score', models.FloatField(default=0)),
                ('finally_score', models.FloatField(default=0)),
                ('ac_counter', models.IntegerField(default=0)),
                ('submission_counter', models.IntegerField(default=0)),
                ('solved_counter', models.IntegerField(default=0)),
                ('impression', models.TextField(blank=True, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('teacher_check', models.BooleanField(default=False)),
                ('teacher_remark', models.TextField(blank=True, null=True)),
                ('asgn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Asgn')),
            ],
        ),
        migrations.CreateModel(
            name='AsgnVisitRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag', models.SmallIntegerField(default=-1)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('proc_time', models.DateTimeField(blank=True, null=True)),
                ('arrangement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Arrangement')),
                ('asgn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Asgn')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EduAcademy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='EduAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('sex', models.SmallIntegerField(choices=[(-1, '未知'), (0, '女'), (1, '男')], default=-1)),
                ('nickname', models.CharField(blank=True, max_length=50, null=True)),
                ('realname', models.CharField(blank=True, max_length=50, null=True)),
                ('headimg', models.CharField(blank=True, max_length=50, null=True)),
                ('motto', models.CharField(blank=True, max_length=255, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_login_time', models.IntegerField()),
                ('role', models.SmallIntegerField(default=0)),
                ('academy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.EduAcademy')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EduDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('academy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.EduAcademy')),
            ],
        ),
        migrations.CreateModel(
            name='EduMajor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.EduDepartment')),
            ],
        ),
        migrations.CreateModel(
            name='EduSchool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='EduYearTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.SmallIntegerField(default=2016)),
                ('term', models.SmallIntegerField(default=1)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.EduSchool')),
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
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.EduAccount')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProblemSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('description', models.TextField(default='')),
                ('image', models.CharField(default='', max_length=255)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.EduAccount')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemSetItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.IntegerField(default=0)),
                ('submission', models.IntegerField(default=0)),
                ('permission', models.SmallIntegerField(default=0)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education_problemset_entity', to='problem.Problem')),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('handle', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('max_size', models.IntegerField(default=1073741824)),
                ('cur_size', models.IntegerField(default=0)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.EduAccount')),
            ],
        ),
        migrations.CreateModel(
            name='RepositoryFS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_dir', models.BooleanField(default=False)),
                ('index', models.IntegerField(default=0)),
                ('name', models.CharField(default='', max_length=255)),
                ('size', models.IntegerField(default=0)),
                ('download_count', models.IntegerField(default=0)),
                ('entity', models.TextField(default='')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.RepositoryFS')),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_visit_time', models.DateTimeField(auto_now_add=True)),
                ('submission', models.IntegerField(default=0)),
                ('ignore', models.IntegerField(default=0)),
                ('accepted', models.IntegerField(default=0)),
                ('pe', models.IntegerField(default=0)),
                ('first_ac_time', models.DateTimeField(blank=True, null=True)),
                ('best_memory', models.IntegerField(default=0)),
                ('best_time', models.IntegerField(default=0)),
                ('best_code_size', models.IntegerField(default=0)),
                ('score', models.FloatField(default=0)),
                ('asgn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Asgn')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.EduAccount')),
                ('judge_status', models.ManyToManyField(blank=True, to='education.JudgeStatus')),
                ('problems', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.AsgnProblems')),
            ],
        ),
        migrations.AddField(
            model_name='repository',
            name='file_system',
            field=models.ManyToManyField(blank=True, to='education.RepositoryFS'),
        ),
        migrations.AddField(
            model_name='problemset',
            name='items',
            field=models.ManyToManyField(blank=True, to='education.ProblemSetItem'),
        ),
        migrations.AddField(
            model_name='problemset',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.EduSchool'),
        ),
        migrations.AddField(
            model_name='judgestatus',
            name='problem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.ProblemSetItem'),
        ),
        migrations.AddField(
            model_name='eduaccount',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.EduDepartment'),
        ),
        migrations.AddField(
            model_name='eduaccount',
            name='major',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.EduMajor'),
        ),
        migrations.AddField(
            model_name='eduaccount',
            name='master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account'),
        ),
        migrations.AddField(
            model_name='eduaccount',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.EduSchool'),
        ),
        migrations.AddField(
            model_name='eduacademy',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.EduSchool'),
        ),
        migrations.AddField(
            model_name='course',
            name='academy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.EduAcademy'),
        ),
        migrations.AddField(
            model_name='course',
            name='arrangements',
            field=models.ManyToManyField(blank=True, to='education.Arrangement'),
        ),
        migrations.AddField(
            model_name='course',
            name='assistants',
            field=models.ManyToManyField(blank=True, related_name='course_assistants', to='education.EduAccount'),
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.EduDepartment'),
        ),
        migrations.AddField(
            model_name='course',
            name='major',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.EduMajor'),
        ),
        migrations.AddField(
            model_name='course',
            name='repositories',
            field=models.ManyToManyField(blank=True, to='education.Repository'),
        ),
        migrations.AddField(
            model_name='course',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.EduSchool'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ManyToManyField(blank=True, null=True, related_name='course_teacher', to='education.EduAccount'),
        ),
        migrations.AddField(
            model_name='course',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.EduYearTerm'),
        ),
        migrations.AddField(
            model_name='asgnvisitrequirement',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.EduAccount'),
        ),
        migrations.AddField(
            model_name='asgnvisitrequirement',
            name='source_arrangement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_arrangement', to='education.Arrangement'),
        ),
        migrations.AddField(
            model_name='asgnreport',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.EduAccount'),
        ),
        migrations.AddField(
            model_name='asgnproblems',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.ProblemSetItem'),
        ),
        migrations.AddField(
            model_name='asgn',
            name='access_control',
            field=models.ManyToManyField(blank=True, to='education.AsgnAccessControl'),
        ),
        migrations.AddField(
            model_name='asgn',
            name='black_list',
            field=models.ManyToManyField(blank=True, related_name='black_list', to='education.EduAccount'),
        ),
        migrations.AddField(
            model_name='asgn',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Course'),
        ),
        migrations.AddField(
            model_name='asgn',
            name='judge_status',
            field=models.ManyToManyField(blank=True, to='education.JudgeStatus'),
        ),
        migrations.AddField(
            model_name='asgn',
            name='problemset',
            field=models.ManyToManyField(blank=True, to='education.AsgnProblems'),
        ),
        migrations.AddField(
            model_name='asgn',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to='education.EduAccount'),
        ),
        migrations.AddField(
            model_name='arrangement',
            name='students',
            field=models.ManyToManyField(blank=True, to='education.EduAccount'),
        ),
    ]