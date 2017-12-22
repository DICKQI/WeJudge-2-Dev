#!/bin/sh
python3 manage.py celery worker -E -l info -n default > /wejudge/log/celery_default.log 2>&1 &
python3 manage.py celery worker -E -l info -n judge_queue -Q judge_queue > /wejudge/log/celery_judge.log 2>&1 & 
python3 manage.py celery worker -E -l info -n code_cross_check -Q code_cross_check > /wejudge/log/celery_cscheck.log 2>&1 &
