"""
TASKS

Regroupment of tasks that will be executed by the
main script. Each task needs to have the decorator
@tasks.add or they will not be detected. Tasks are
executed in order.
"""
from shutil import rmtree, copy
from os import path, renames, rename, getcwd, remove, system
from settings import settings_directory, project_directory, ocean, project_user, secret_key, db_pass
from utils import manage, FileEditor, TaskManager

__author__ = 'snake'
tasks = TaskManager()


@tasks.add
def rename_settings_directory():
    """
    Change the settings directory from
    'ocean' to the chosen project name.
    """
    if not path.exists(settings_directory):
        old_directory = path.join(project_directory, 'ocean')
        renames(old_directory, ocean)


@tasks.add
def rename_config_files():
    """
    Change the config files from
    'ocean' to the chosen project name.
    """
    old_file = path.join(project_directory, 'ocean-prod.ini')
    renames(old_file, "{}-prod.ini".format(ocean))
    old_file = path.join(project_directory, 'ocean-staging.ini')
    renames(old_file, "{}-staging.ini".format(ocean))
    old_file = path.join(project_directory, 'docker', 'nginx', 'ocean.conf')
    renames(old_file, path.join(project_directory, 'docker', 'nginx', "{}.conf".format(ocean)))


@tasks.add
def set_manage_ocean():
    """
    Set the settings path string in manage.py.
    """
    manage_file = path.join(project_directory, 'manage.py')
    with FileEditor(manage_file) as editor:
        editor.replace('ocean.settings', '%s.settings' % ocean)


@tasks.add
def set_docker_deploy():
    """
    Clone docker deploy and move settings and authorized keys
    """
    fabfile_folder = path.join(project_directory, 'fabfile')
    # if folder already exists, delete it
    if path.exists(fabfile_folder):
        rmtree(fabfile_folder)

    system("git clone git@bitbucket.org:nixateam/dockerdeploy.git fabfile")

    # move fabsettings example to deploy folder
    src = path.join(project_directory, 'fabfile', 'fabsettings.py.example')
    if path.exists(src):
        copy(src, path.join(project_directory, 'deploy', 'fabsettings.py'))

    # move authorized_keys
    keys_files = (
        path.join(project_directory, 'fabfile', 'templates', 'authorized_keys'),
        path.join(project_directory, 'fabfile', 'templates', 'authorized_keys_prod'),
    )
    for keys_file in keys_files:
        if path.exists(keys_file):
            copy(keys_file, path.join(project_directory, 'deploy'))


@tasks.add
def set_docker_ocean():
    """
    Set the project name in docker files
    """

    files = (
        path.join(project_directory, 'docker', 'django', 'Dockerfile'),
        path.join(project_directory, 'docker', 'django', 'Dockerfile-staging'),
        path.join(project_directory, 'docker', 'django', 'Dockerfile-prod'),
        path.join(project_directory, 'docker-compose-staging.yml'),
        path.join(project_directory, 'docker-compose-prod.yml'),
        path.join(project_directory, 'gulp', 'Dockerfile'),
        path.join(project_directory, 'docker', 'nginx', 'Dockerfile-staging'),
        path.join(project_directory, 'docker', 'nginx', 'Dockerfile-prod'),
        path.join(project_directory, 'docker', 'nginx', '{}.conf'.format(ocean)),
        path.join(project_directory, '{}-staging.ini'.format(ocean)),
        path.join(project_directory, '{}-prod.ini'.format(ocean)),
    )

    for file_path in files:
        with FileEditor(file_path) as editor:
            editor.replace('ocean', ocean)

    docker_compose_file = path.join(project_directory, 'docker-compose.yml')
    with FileEditor(docker_compose_file) as editor:
        editor.replace('ocean', ocean)
        editor.replace('DB_NAME', ocean)
        editor.replace('DB_USER', project_user)

    fabfile = path.join(project_directory, 'deploy', 'fabsettings.py')
    with FileEditor(fabfile) as editor:
        editor.replace('((ocean))', ocean)


@tasks.add
def set_secret_key():
    """
    Put the secret key into settings.py.
    """
    file_path = path.join(settings_directory, 'settings.py')
    with FileEditor(file_path) as editor:
        editor.replace('SECRET_KEY = \'\'', 'SECRET_KEY = \'%s\'' % secret_key)


@tasks.add
def set_secret_key_env():
    """
    Put the secret key into settings.py.
    """
    file_path = path.join(project_directory, '.env.example')
    with FileEditor(file_path) as editor:
        editor.replace('SECRET_KEY=', 'SECRET_KEY={}'.format(secret_key))


@tasks.add
def set_settings():
    """
    Insert prod and staging settings path string, ssh
    password and database password.
    """
    with FileEditor(path.join(settings_directory, 'settings.py')) as editor:
        editor.replace('((DB_USER))', project_user)
        editor.replace('((DB_NAME))', ocean)
        editor.replace('((DB_PASS))', db_pass)


@tasks.add
def remove_git():
    if path.exists('./.git'):
        rmtree('./.git')


@tasks.add
def remove_project_starter_readme():
    if path.exists('PROJECT_STARTER_README.md'):
        remove('PROJECT_STARTER_README.md')


@tasks.add
def rename_parent_direct():
    """
    Change the current working directory (project_starter) from
    '/project-starter/' to the chosen project name.
    """
    parent_directory = path.dirname(getcwd())
    new_project_directory = path.join(parent_directory, ocean)
    rename(project_directory, new_project_directory)
