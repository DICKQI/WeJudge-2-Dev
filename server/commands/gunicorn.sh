#/bin/sh
gunicorn --chdir /wejudge/server --worker-class=gevent server.wsgi:application -b 0.0.0.0:666 --reload
