PROJECT_NAME = '((PROJECT_NAME))'
# ssh link to repository
REPOSITORY = 'git@bitbucket.org:nixateam/((PROJECT_NAME)).git'  # todo
DOCKER_COMPOSE_VERSION = '1.14.0'
WEB_SERVICE = 'web'
DOCKER_GC_CONTENT = """
#!/bin/bash
docker container prune -f
docker image prune -a -f
rm -rf /var/lib/docker/aufs/diff/*-removing"""

STAGES = {
    'staging': {
        'hosts': ['24.37.82.222'],
        'default_branch': 'develop',
        'port': '',  # todo
        'user': 'deploy',
        'DJANGO_SETTINGS_MODULE': '((PROJECT_NAME)).staging',
        'docker_compose_file': 'docker-compose-staging.yml',
        'authorized_keys_file': 'authorized_keys'
    },
    'production': {
        'hosts': [''],  # todo
        'default_branch': 'master',
        'user': 'deploy',
        'DJANGO_SETTINGS_MODULE': '((PROJECT_NAME)).prod',
        'docker_compose_file': 'docker-compose-prod.yml',
        'authorized_keys_file': 'authorized_keys_prod',
    }
}