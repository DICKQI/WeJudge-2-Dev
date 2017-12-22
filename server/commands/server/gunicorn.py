# coding=utf-8
import sys
import os
import multiprocessing

path_of_current_dir = "/wejudge/server"

sys.path.insert(0, path_of_current_dir)

log_path = "/wejudge/log"

worker_class = 'gevent'
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1

chdir = path_of_current_dir

worker_connections = 1000
timeout = 30
max_requests = 2000
graceful_timeout = 30

loglevel = 'critical'

reload = True
debug = True

bind = "%s:%s" % ("0.0.0.0", 2333)
errorlog = '%s/wejudge_error.log' % log_path
accesslog = '%s/wejudge_access.log' % log_path
