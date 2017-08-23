#!/bin/sh

# wait for Redis server to start
sleep 10

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
sh -c "celery worker -A hitiit360.celeryconf -l INFO"