from __future__ import with_statement

from datetime import datetime
from time import sleep

from fabric.api import cd, run, env, task
from fabric.context_managers import prefix, settings, hide, shell_env
from fabric.contrib.files import _expand_path, exists, append
from fabric.decorators import with_settings
from fabric.operations import require, put, sudo, local, get

from fabfile.fabsettings import STAGES, DOCKER_COMPOSE_VERSION, WEB_SERVICE, DOCKER_GC_CONTENT, REPOSITORY, \
    PROJECT_NAME, ROOT_USER
from fabfile.install_files import UpStartFile


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


@with_settings(user=ROOT_USER)
def create_deploy_user():
    run('useradd -m -s /bin/bash deploy')
    run('usermod -a -G sudo deploy')
    put('../')


@task
def install():
    require('stage', provided_by=(staging, production))

    with settings(user=ROOT_USER):
        branch = env.default_branch
        # add rsyslog repo
        run('add-apt-repository ppa:adiscon/v8-stable')
        # install security
        run('apt-get update && apt-get install -y unattended-upgrades apt-transport-https ca-certificates git'
            ' curl software-properties-common rsyslog && unattended-upgrades')
        run('rm -rf *')

        # building and installing docker-gc to clean up the server every hour
        run('echo "{}" > /etc/cron.hourly/docker-gc'.format(DOCKER_GC_CONTENT))
        run('chmod +x /etc/cron.hourly/docker-gc')

        # install docker
        run('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -')
        run('add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"')
        run('apt-get update && apt-get remove docker docker-engine docker.io && apt-get install -y docker-ce')
        run('curl -L https://github.com/docker/compose/releases/download/{}/docker-compose-`uname -s`-`uname -m` '
            '> /usr/local/bin/docker-compose'.format(DOCKER_COMPOSE_VERSION))
        run('chmod +x /usr/local/bin/docker-compose && usermod -aG docker {}'.format(STAGES[env.stage]['user']))

        # install rsys config
        put('/fabfile/templates/10-docker.conf', '/etc/rsyslog.d/10-docker.conf')
        run('service rsyslog restart')

        # configure upstart
        with cd('/etc/init/'):
            upstartfile = UpStartFile(
                django=env.DJANGO_SETTINGS_MODULE,
                user=env.user,
                project_name=PROJECT_NAME,
                docker_compose_file=env.docker_compose_file,
            )
            append('nixa_docker.conf', upstartfile.output())

    with settings(user=env.user):
        # git setup
        run('git config --global user.name \'{}\' && git config --global user.email \'dev@nixa.ca\''.format(PROJECT_NAME))

        # install git project
        run('git clone -b {0} {1} {2}'.format(branch, REPOSITORY, PROJECT_NAME))
        run('chown -R {0}:{0} {1}'.format(env.user, PROJECT_NAME))
        move_env_file(env.user)
        move_pip_file(env.user)

        # docker-compose up every services
        with cd('/home/{}/{}'.format(env.user, PROJECT_NAME)):
            run('docker-compose -f {} up --build -d'.format(env.docker_compose_file))
        copy_authorized_keys()

    with settings(user=ROOT_USER):
        # setup ssh security
        run('apt-get install fail2ban')
        run("sed -i '/PermitRootLogin /c\PermitRootLogin no' /etc/ssh/sshd_config")
        run("sed -i '/PasswordAuthentication/c\PasswordAuthentication no' /etc/ssh/sshd_config")
        run("service ssh restart")


@task
def down():
    require('stage', provided_by=(staging, production))
    run('docker ps $(docker ps -q)')


@task
def reup(branch=None, nobuild=False):
    require('stage', provided_by=(staging, production))

    if exists_local('.env'):
        move_env_file(env.user)

    branch = branch or env.default_branch

    with cd('/home/{}/{}'.format(env.user, PROJECT_NAME)):
        with prefix(". .env"):
            run('git fetch')
            run('git checkout {}'.format(branch))
            run('git pull')

            with shell_env(DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE):
                if nobuild:
                    sudo('docker-compose -f {} up -d'.format(env.docker_compose_file))
                else:
                    sudo('docker-compose -f {} up --build -d'.format(env.docker_compose_file))


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
def database_rollback(dumpfile=None):
    require('stage', provided_by=(staging, production))
    if exists_local('.env'):
        move_env_file(env.user)
    if dumpfile:
        with cd('/home/{}/{}'.format(env.user, PROJECT_NAME)):
            with prefix(". .env"):
                current_commit_hash = run('echo $(git show --pretty=format:%h -s)')
                docker_db_container = run('echo $(docker-compose -f {} ps -q db)'.format(env.docker_compose_file))

                run('docker-compose -f {0} exec -T'
                    ' db pg_dump -d ${{POSTGRES_DB}} -U ${{POSTGRES_USER}} -h localhost -F c >'
                    ' ./docker/postgresql/dumps/{1}.sql'.format(env.docker_compose_file, current_commit_hash))

                run('docker stop {0} && docker rm {0}'.format(docker_db_container))
                run('docker-compose -f {0} up -d db'.format(env.docker_compose_file))

                docker_db_container = run('echo $(docker-compose -f {} ps -q db)'.format(env.docker_compose_file))
                run('docker cp ./docker/postgresql/dumps/{dumpfile}.sql'
                    ' {docker_db_container}:/{dumpfile}.sql'.format(**{
                    'dumpfile': dumpfile,
                    'docker_db_container': docker_db_container
                }))
                with settings(warn_only=True):
                    # restore the dump sql
                    run('docker-compose -f {0} exec -T'
                        ' db pg_restore -U ${{POSTGRES_USER}} -d ${{POSTGRES_DB}} -C -c ./{1}.sql &&'
                        ' rm ./{0}.sql'.format(env.docker_compose_file, dumpfile))

                    run('docker-compose -f {0} exec -T web python manage.py migrate --noinput'.format(env.docker_compose_file))
    else:
        print('Please use commit variable.')
        raise SystemExit


@task
def rollback(commit=None):
    require('stage', provided_by=(staging, production))

    if commit:
        with cd('/home/{}/{}'.format(env.user, PROJECT_NAME)):
            if exists('docker/postgresql/dumps/{}.sql'.format(commit)):
                pass
            else:
                print("We could not find the sql dump you were requesting")
                raise SystemExit
    else:
        commit = 'HEAD~1'

    if exists_local('.env'):
        move_env_file(env.user)
    with cd('/home/{}/{}'.format(env.user, PROJECT_NAME)):
        with prefix(". .env"):
            run('git fetch')
            current_commit_hash = run('echo $(git show --pretty=format:%h -s)')
            docker_db_container = run('echo $(docker-compose -f {} ps -q db)'.format(env.docker_compose_file))
            run('docker-compose -f {0} exec -T'
                ' db pg_dump -d ${{POSTGRES_DB}} -U ${{POSTGRES_USER}} -h localhost -F c >'
                ' ./docker/postgresql/dumps/{1}.sql'.format(env.docker_compose_file, current_commit_hash))
            run('git checkout {}'.format(commit))
            previous_commit_hash = run('echo $(git show --pretty=format:%h -s)')
            with shell_env(DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE):
                run('docker-compose -f {} build web'.format(env.docker_compose_file))
                run('docker-compose -f {} up --no-deps -d web'.format(env.docker_compose_file))
                # copy over the previous dump.sql to be restored
            # stop the db container and remove it
            run('docker stop {0} && docker rm -v {0}'.format(docker_db_container))
            run('docker-compose -f {0} up -d db'.format(env.docker_compose_file))
            docker_db_container = run('echo $(docker-compose -f {} ps -q db)'.format(env.docker_compose_file))
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
def get_db_dump(commit=None):
    require('stage', provided_by=(staging, production))
    if commit:
        with cd('/home/{}/{}/docker/postgresql/dumps'.format(env.user, PROJECT_NAME)):
            if exists('{}.sql'.format(commit)):
                get('{}.sql'.format(commit), '%(basename)s')
    else:
        print('We are going to make a new database dump and download it for you')
        time_stamp = datetime.now().strftime('%Y_%m_%d__%H_%M_%S')

        with cd('/home/{}/{}'.format(env.user, PROJECT_NAME)):
            with prefix(". .env"):
                run('docker-compose -f {0} exec -T'
                    ' db pg_dump -d ${{POSTGRES_DB}} -U ${{POSTGRES_USER}} -h localhost -F c >'
                    ' ./docker/postgresql/dumps/manual_dump_{1}.sql'.format(env.docker_compose_file, time_stamp))

        with cd('/home/{}/{}/docker/postgresql/dumps'.format(env.user, PROJECT_NAME)):
            if exists('manual_dump_{}.sql'.format(time_stamp)):
                get('manual_dump_{}.sql'.format(time_stamp), '%(dirname)s')


@task
def get_logs():
    require('stage', provided_by=(staging, production))
    time_stamp = datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
    with cd('/home/{}/{}'.format(env.user, PROJECT_NAME)):
        get('/var/log/docker', 'logs/{}_{}/%(path)s'.format(env.stage, time_stamp))


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
    put('~/.pip/pip.conf', '/home/{}/{}/pip.conf'.format(stage_user, PROJECT_NAME))


def copy_authorized_keys():
    run('cp ~/{}/fabconfig/templates/{} ~/.ssh/authorized_keys'.format(PROJECT_NAME, env.authorized_keys_file))
    run('chmod 600 ~/.ssh/authorized_keys')


@task
def replicate_db_on_local():
    require('stage', provided_by=(staging, production))
    time_stamp = datetime.now().strftime('%Y_%m_%d__%H_%M_%S')

    with cd('/home/{}/{}'.format(env.user, PROJECT_NAME)):
        with prefix(". .env"):
            run('docker-compose -f {0} exec -T'
                ' db pg_dump -d ${{POSTGRES_DB}} -U ${{POSTGRES_USER}} -h localhost -F c >'
                ' ./docker/postgresql/dumps/manual_dump_{1}.sql'.format(env.docker_compose_file, time_stamp))

    with cd('/home/{}/{}/docker/postgresql/dumps'.format(env.user, PROJECT_NAME)):
        if exists('manual_dump_{}.sql'.format(time_stamp)):
            get('manual_dump_{}.sql'.format(time_stamp), '%(dirname)s')

    # stop all containers
    local('docker stop $(docker ps -a -q)')

    # bring up old db
    local('docker-compose up -d db')
    db_container = local('docker-compose -f {} ps -q db'.format(env.docker_compose_file), capture=True)

    # remove old db
    local('docker stop {docker_container}'.format(docker_container=db_container))
    local('docker rm -v {docker_container}'.format(docker_container=db_container))

    # create new db
    local('docker-compose up -d')
    db_container = local('echo $(docker-compose -f {} ps -q db)'.format(env.docker_compose_file), capture=True)
    local_pg_user = local("docker exec -ti {} bash -c \'echo $POSTGRES_USER\'".format(db_container), capture=True)
    local_pg_db = local("docker exec -ti {} bash -c \'echo $POSTGRES_DB\'".format(db_container), capture=True)

    # copy dump on new db
    local('docker cp ./manual_dump_{time_stamp}.sql {db_container}:/'.format(
        time_stamp=time_stamp, db_container=db_container))

    # restore on new db
    with settings(warn_only=True):
        local('docker-compose -f docker-compose.yml exec -T '
              'db pg_restore -U {local_pg_user} -d {local_pg_db} -C -c ./manual_dump_{time_stamp}.sql'.format(
                    time_stamp=time_stamp, local_pg_db=local_pg_db, local_pg_user=local_pg_user))

    # stop new db
    local('docker stop $(docker ps -q)')
    print('Task done. Ready to run docker-compose up')


@task
def replicate_media_on_local():
    require('stage', provided_by=(staging, production))
    with cd('/home/{}/{}'.format(env.user, PROJECT_NAME)):
        with prefix(". .env"):
            run('docker-compose -f {0} exec -T'
                ' web tar -czvf ./media.tar.gz  media'.format(env.docker_compose_file))
            web_container = run('echo $(docker-compose -f {} ps -q web)'.format(env.docker_compose_file))
            run('docker cp {web_container}:/{project_name}/media.tar.gz ./'.format(
                web_container=web_container, project_name=PROJECT_NAME))
            if exists('media.tar.gz'):
                get('media.tar.gz', '%(dirname)s')
    local('tar -xzvf ./media.tar.gz')
    local('rm media.tar.gz')
