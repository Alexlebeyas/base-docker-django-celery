#!/bin/sh

# wait for Redis server to start
sleep 10

# remove pid
rm -r './celerybeat.pid'

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
sh -c "celery beat -A hitiit360.celeryconf -l INFO"