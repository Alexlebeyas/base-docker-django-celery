from __future__ import with_statement
import os
from datetime import datetime
from fabric.api import cd, run, env, task
from fabric.context_managers import prefix, settings, hide, shell_env
from fabric.operations import require, put, sudo, local, get
from fabric.contrib.files import _expand_path, exists

PROJECT_NAME = '((PROJECT_NAME))'
# ssh link to repository
REPOSITORY = 'git@bitbucket.org:nixateam/((PROJECT_NAME)).git'  # todo
DOCKER_COMPOSE_VERSION = '1.14.0'
WEB_SERVICE = 'web'
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


def set_stage(stage='staging'):
    env.stage = stage
    for option, value in STAGES[env.stage].items():
        setattr(env, option, value)


@task
def staging():
    set_stage('staging')


@task
def production():
    set_stage('production')


@task
def install():
    require('stage', provided_by=(staging, production))

    branch = env.default_branch
    # add rsyslog repo
    sudo('add-apt-repository ppa:adiscon/v8-stable')
    # install security
    sudo('apt-get update && apt-get install -y unattended-upgrades apt-transport-https ca-certificates git'
        ' curl software-properties-common rsyslog && unattended-upgrades')
    # git setup
    run('git config --global user.name \'{}\' && git config --global user.email \'dev@nixa.ca\''.format(PROJECT_NAME))
    # building and installing docker-gc to clean up the server every hour
    run('rm -rf *')
    sudo('echo "#!/bin/bash\ndocker system prune -a -f" > /etc/cron.hourly/docker-gc')
    sudo('chmod +x /etc/cron.hourly/docker-gc')
    # install docker
    sudo('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -')
    sudo('add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"')
    sudo('apt-get update && apt-get remove docker docker-engine docker.io && apt-get install -y docker-ce')
    sudo('curl -L https://github.com/docker/compose/releases/download/{}/docker-compose-`uname -s`-`uname -m` '
        '> /usr/local/bin/docker-compose'.format(DOCKER_COMPOSE_VERSION))
    sudo('chmod +x /usr/local/bin/docker-compose && usermod -aG docker {}'.format(env.user))
    # install git project
    run('git clone {} {}'.format(REPOSITORY, PROJECT_NAME))
    sudo('chown -R {0}:{0} {1}'.format(env.user, PROJECT_NAME))
    move_env_file(env.user)
    move_pip_file(env.user)
    # docker-compose up every services
    with cd('/home/{}/{}'.format(env.user, PROJECT_NAME)):
        run('git checkout {}'.format(branch))
        # copy rsyslog conf from docker settings to rsyslog config
        sudo('cp /home/deploy/{}/config/rsyslog/10-docker.conf /etc/rsyslog.d/'.format(PROJECT_NAME))
        sudo('service rsyslog restart')
        # compose up
        sudo('docker-compose -f {} up --build -d'.format(env.docker_compose_file))
    copy_authorized_keys()
    # setup ssh security
    sudo('apt-get install fail2ban')
    sudo("sed -i '/PermitRootLogin /c\PermitRootLogin no' /etc/ssh/sshd_config")
    sudo("sed -i '/PasswordAuthentication/c\PasswordAuthentication no' /etc/ssh/sshd_config")
    sudo("service ssh restart")


@task
def deploy(branch=None, commit=None, service=WEB_SERVICE):
    require('stage', provided_by=(staging, production))
    if exists_local('.env'):
        move_env_file(env.user)

    if branch and commit:
        print("You can provide either a branch or a commit, not both")
        raise SystemExit

    branch = branch or env.default_branch
    if commit is not None:
        branch = None

    with cd('/home/{}/{}'.format(env.user, PROJECT_NAME)):
        with prefix(". .env"):
            compose_services = run('docker-compose -f {0} config --services'.format(env.docker_compose_file))
            compose_services = compose_services.split('\r\n')
            if service not in compose_services:
                print('Please choose to deploy a service in the following list: {}'.format(compose_services[:-1]))
                raise SystemExit

            run('git fetch')
            current_commit_hash = run('echo $(git show --pretty=format:%h -s)')
            run('git checkout {}'.format(branch or commit))
            if commit is None:
                run('git pull origin {}'.format(branch))

            run('mkdir -p ./docker/postgresql/dumps')
            run('docker-compose -f {0} exec -T'
                ' db pg_dump $POSTGRES_DB -U $POSTGRES_USER -h localhost -F c >'
                ' ./docker/postgresql/dumps/{1}.sql'.format(env.docker_compose_file, current_commit_hash))

            with shell_env(DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE):
                run('docker-compose -f {} build {}'.format(env.docker_compose_file, service))
                run('docker-compose -f {} up --no-deps -d {}'.format(env.docker_compose_file, service))
                if service == WEB_SERVICE:
                    run('docker-compose -f {} exec -T {} python manage.py collectstatic --noinput'.format(
                        env.docker_compose_file, service))
                    run('docker-compose -f {} exec -T {} python manage.py migrate'.format(
                        env.docker_compose_file, service))


@task
def rollback():
    require('stage', provided_by=(staging, production))
    if exists_local('.env'):
        move_env_file(env.user)
    with cd('/home/{}/{}'.format(env.user, PROJECT_NAME)):
        with prefix(". .env"):
            run('git fetch')
            current_commit_hash = run('echo $(git show --pretty=format:%h -s)')
            docker_db_container = run('echo $(docker-compose -f {} ps -q db)'.format(env.docker_compose_file))
            run('docker-compose -f {0} exec -T'
                ' db pg_dump ${{DB_NAME}} -U ${{POSTGRES_USER}} -h localhost -F c >'
                ' ./docker/postgresql/dumps/{1}.sql'.format(env.docker_compose_file, current_commit_hash))
            run('git checkout HEAD~1')
            previous_commit_hash = run('echo $(git show --pretty=format:%h -s)')
            with shell_env(DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE):
                run('docker-compose -f {} build web'.format(env.docker_compose_file))
                run('docker-compose -f {} up --no-deps -d web'.format(env.docker_compose_file))
                # copy over the previous dump.sql to be restored
            # stop the db container and remove it
            run('docker stop {0} && docker rm {0}'.format(docker_db_container))
            # bring the db container back up in detached mode
            run('docker-compose -f {0} up -d db'.format(env.docker_compose_file))
            run('docker cp ./docker/postgresql/dumps/{previous_commit_hash}.sql'
                ' {docker_db_container}:/{previous_commit_hash}.sql'.format(**{
                'previous_commit_hash': previous_commit_hash,
                'docker_db_container': docker_db_container
            }))
            with settings(warn_only=True):
                # restore the dump sql
                run('docker-compose -f {0} exec -T'
                    ' db pg_restore -U ${{POSTGRES_USER}} -d ${{POSTGRES_DB}} -C -c ./{1}.sql &&'
                    ' rm ./{0}.sql'.format(env.docker_compose_file, previous_commit_hash))
                # migrate the database
                run('docker-compose -f {} exec -T web python manage.py collectstatic --noinput'.format(
                    env.docker_compose_file))
                run('docker-compose -f {0} exec -T web python manage.py migrate'.format(env.docker_compose_file))


@task
def get_logs():
    require('stage', provided_by=(staging, production))
    time_stamp = datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
    with cd('/home/{}/{}'.format(env.user, PROJECT_NAME)):
        run('cp -r /var/log/docker /home/{}/log_{}'.format(env.user, time_stamp))
        run('tar -cvzf log_{1}.tgz /home/{0}/log_{1}'.format(env.user, time_stamp))
        get('log_{}.tgz'.format(time_stamp), '%(path)s')
        run('rm -r /home/{0}/log_{1}'.format(env.user, time_stamp))
@task
def copy_media_files():
    require('stage', provided_by=(staging, production))
    with cd('/home/{}/{}'.format(env.user, PROJECT_NAME)):
        web_id = run('echo $(docker-compose -f {} ps -q web)'.format(env.docker_compose_file))
        run('docker cp ./media/. {}:/{}/media/'.format(web_id, PROJECT_NAME))
        run('docker exec -ti {} chown -R uwsgi:101 /{}/media/'.format(web_id, PROJECT_NAME))


def exists_local(path):
    cmd = 'stat %s' % _expand_path(path)
    with settings(hide('everything'), warn_only=True):
        return not local(cmd).failed


def move_env_file(stage_user):
    put('.env', '/home/{}/{}/.env'.format(stage_user, PROJECT_NAME))
    local('rm .env')


def move_pip_file(stage_user):
    put('pip.conf', '/home/{}/{}/pip.conf'.format(stage_user, PROJECT_NAME))


def copy_authorized_keys():
    run('cp ~/{}/config/{} ~/.ssh/authorized_keys'.format(PROJECT_NAME, env.authorized_keys_file))
    run('chmod 600 ~/.ssh/authorized_keys')
