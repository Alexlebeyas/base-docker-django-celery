from uuid import uuid4

ocean = '((ocean))'
# ssh link to repository
REPOSITORY = 'git@bitbucket.org:nixateam/((ocean)).git'  # todo
DOCKER_COMPOSE_VERSION = '1.14.0'
WEB_SERVICE = 'web'
DOCKER_GC_CONTENT = """
#!/bin/bash
docker container prune -f
docker image prune -a -f
rm -rf /var/lib/docker/aufs/diff/*-removing"""

STAGES = {
    'staging': {
        'hosts': ['22.37.82.222'],
        'default_branch': 'develop',
        'port': '',  # todo
        'user': 'deploy',
        'DJANGO_SETTINGS_MODULE': '((ocean)).staging',
        'docker_compose_file': 'docker-compose-staging.yml',
        'authorized_keys_file': 'authorized_keys'
    },
    'production': {
        'hosts': [''],  # todo
        'default_branch': 'master',
        'user': 'deploy',
        'DJANGO_SETTINGS_MODULE': '((ocean)).prod',
        'docker_compose_file': 'docker-compose-prod.yml',
        'authorized_keys_file': 'authorized_keys_prod',
    }
}

ROOT_USER = 'root'

random_password = lambda: str(uuid4()).replace('-', '')
