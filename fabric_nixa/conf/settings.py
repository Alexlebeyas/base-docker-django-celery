from uuid import uuid4

PROJECT_NAME = 'dockertest'
# ssh link to repository
REPOSITORY = 'git@bitbucket.org:rsampana/dockertest.git'  # todo
DOCKER_COMPOSE_VERSION = '1.14.0'
WEB_SERVICE = 'web'
DOCKER_GC_CONTENT = """
#!/bin/bash
docker container prune -f
docker image prune -a -f
rm -rf /var/lib/docker/aufs/diff/*-removing"""

STAGES = {
    'staging': {
        'hosts': ['192.168.2.105'],
        'default_branch': 'develop',
        'port': '',  # todo
        # 'user': 'root',
        'deploy_user': 'deploy',
        'root_user': 'root',
        'DJANGO_SETTINGS_MODULE': 'dockertest.staging',
        'docker_compose_file': 'docker-compose-staging.yml',
        'authorized_keys_file': 'authorized_keys'
    },
    'production': {
        'hosts': [''],  # todo
        'default_branch': 'master',
        # 'user': 'deploy',
        'DJANGO_SETTINGS_MODULE': 'dockertest.prod',
        'docker_compose_file': 'docker-compose-prod.yml',
        'authorized_keys_file': 'authorized_keys_prod',
    }
}

DEPLOY_USER = 'deploy'
ROOT_USER = 'root'

random_password = lambda: str(uuid4()).replace('-', '')
