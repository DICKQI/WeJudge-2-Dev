# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-03 07:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0017_auto_20170403_1413'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='arrangement',
            options={'verbose_name': '教学-课程-排课', 'verbose_name_plural': '教学-课程-排课'},
        ),
        migrations.AlterModelOptions(
            name='asgn',
            options={'verbose_name': '作业信息', 'verbose_name_plural': '作业信息'},
        ),
        migrations.AlterModelOptions(
            name='asgnaccesscontrol',
            options={'verbose_name': '作业访问权限-控制', 'verbose_name_plural': '作业访问权限-控制'},
        ),
        migrations.AlterModelOptions(
            name='asgnproblem',
            options={'verbose_name': '作业题目项信息', 'verbose_name_plural': '作业题目项信息'},
        ),
        migrations.AlterModelOptions(
            name='asgnreport',
            options={'verbose_name': '作业实验报告信息', 'verbose_name_plural': '作业实验报告信息'},
        ),
        migrations.AlterModelOptions(
            name='asgnvisitrequirement',
            options={'verbose_name': '作业访问权限-调课请求', 'verbose_name_plural': '作业访问权限-调课请求'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': '教学-课程', 'verbose_name_plural': '教学-课程'},
        ),
        migrations.AlterModelOptions(
            name='eduacademy',
            options={'verbose_name': '教学-学院', 'verbose_name_plural': '教学-学院'},
        ),
        migrations.AlterModelOptions(
            name='eduaccount',
            options={'verbose_name': '教学系统 马甲账户', 'verbose_name_plural': '教学系统 马甲账户'},
        ),
        migrations.AlterModelOptions(
            name='edudepartment',
            options={'verbose_name': '教学-院系', 'verbose_name_plural': '教学-院系'},
        ),
        migrations.AlterModelOptions(
            name='edumajor',
            options={'verbose_name': '教学-专业', 'verbose_name_plural': '教学-专业'},
        ),
        migrations.AlterModelOptions(
            name='eduschool',
            options={'verbose_name': '教学-学校', 'verbose_name_plural': '教学-学校'},
        ),
        migrations.AlterModelOptions(
            name='eduyearterm',
            options={'verbose_name': '教学-学年学期', 'verbose_name_plural': '教学-学年学期'},
        ),
        migrations.AlterModelOptions(
            name='judgestatus',
            options={'verbose_name': '作业评测记录', 'verbose_name_plural': '作业评测记录'},
        ),
        migrations.AlterModelOptions(
            name='problemclassify',
            options={'verbose_name': '题目分类', 'verbose_name_plural': '题目分类'},
        ),
        migrations.AlterModelOptions(
            name='problemset',
            options={'verbose_name': '教学-题目集', 'verbose_name_plural': '教学-题目集'},
        ),
        migrations.AlterModelOptions(
            name='problemsetitem',
            options={'verbose_name': '教学-题目集-题目项', 'verbose_name_plural': '教学-题目集-题目项'},
        ),
        migrations.AlterModelOptions(
            name='repository',
            options={'verbose_name': '教学资源仓库', 'verbose_name_plural': '教学资源仓库'},
        ),
        migrations.AlterModelOptions(
            name='repositoryfs',
            options={'verbose_name': '教学资源仓库文件系统表', 'verbose_name_plural': '教学资源仓库文件系统表'},
        ),
        migrations.AlterModelOptions(
            name='solution',
            options={'verbose_name': '作业题目的解决情况', 'verbose_name_plural': '作业题目的解决情况'},
        ),
    ]
