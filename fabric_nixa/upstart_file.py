class UpStartFile(object):
    TEMPLATE = """
description "Nixa Docker"
author "ryan"

start on filesystem and started docker
stop on runlevel [!2345]

# Automatically restart process if crashed (limit 3 times in 4 minutes)
respawn limit 3 240

# our process forks(clones) many times (maybe 10) so expect fork, or expect daemon are useless.
# we use the technique explained here http://stackoverflow.com/questions/12200217/can-upstart-expect-respawn-be-used-on-processes-that-fork-more-than-twice

# start the container in the pre-start script
pre-start script
    # wait (if necessary) for our docker context to be accessible
    while [ ! -f /home/{user}/{project_name}/{docker_compose_file} ]
    do
      sleep 1
    done
    set -a
    . /home/{user}/{project_name}/.env
    export DJANGO_SETTINGS_MODULE="{django}" && /usr/local/bin/docker-compose -f /home/{user}/{project_name}/{docker_compose_file} up -d
end script

# run a process that stays up while our docker container is up. Upstart will track this PID
script
    while docker ps | grep -q "{project_name}_"; do
            sleep 2
    done
end script

# stop docker container after the stop event has completed
post-stop script
    if docker ps | grep -q {project_name}__;
    then
        /usr/local/bin/docker-compose -f /home/{user}/{project_name}/{docker_compose_file} stop
    fi
end script
"""

    def __init__(self, django='none', user='none', project_name='none', docker_compose_file='none'):
        self.django = django
        self.user = user
        self.project_name = project_name
        self.docker_compose_file = docker_compose_file

    def output(self):
        return self.TEMPLATE.format(**{
            'django': self.django,
            'user': self.user,
            'project_name': self.project_name,
            'docker_compose_file': self.docker_compose_file,
        })
