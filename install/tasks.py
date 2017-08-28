"""
TASKS

Regroupment of tasks that will be executed by the
main script. Each task needs to have the decorator
@tasks.add or they will not be detected. Tasks are
executed in order.
"""
from shutil import rmtree
from os import path, renames, rename, getcwd, remove
from settings import settings_directory, project_directory, project_name, project_user, secret_key, db_pass
from utils import manage, FileEditor, TaskManager

__author__ = 'snake'
tasks = TaskManager()


@tasks.add
def rename_settings_directory():
    """
    Change the settings directory from
    'PROJECT_NAME' to the chosen project name.
    """
    if not path.exists(settings_directory):
        old_directory = path.join(project_directory, 'PROJECT_NAME')
        renames(old_directory, project_name)


@tasks.add
def rename_config_files():
    """
    Change the config files from
    'PROJECT_NAME' to the chosen project name.
    """
    old_file = path.join(project_directory, 'PROJECT_NAME-prod.ini')
    renames(old_file, "{}-prod.ini".format(project_name))
    old_file = path.join(project_directory, 'PROJECT_NAME-staging.ini')
    renames(old_file, "{}-staging.ini".format(project_name))
    old_file = path.join(project_directory, 'docker', 'nginx', 'PROJECT_NAME.conf')
    renames(old_file, path.join(project_directory, 'docker', 'nginx', "{}.conf".format(project_name)))


@tasks.add
def set_manage_project_name():
    """
    Set the settings path string in manage.py.
    """
    manage_file = path.join(project_directory, 'manage.py')
    with FileEditor(manage_file) as editor:
        editor.replace('PROJECT_NAME.settings', '%s.settings' % project_name)


@tasks.add
def set_docker_project_name():
    """
    Set the project name in docker files
    """

    files = (
        path.join(project_directory, 'Dockerfile'),
        path.join(project_directory, 'Dockerfile-staging'),
        path.join(project_directory, 'Dockerfile-prod'),
        path.join(project_directory, 'docker-compose-staging.yml'),
        path.join(project_directory, 'docker-compose-prod.yml'),
        path.join(project_directory, 'gulp', 'Dockerfile'),
        path.join(project_directory, 'docker', 'nginx', 'Dockerfile-staging'),
        path.join(project_directory, 'docker', 'nginx', 'Dockerfile-prod'),
        path.join(project_directory, 'docker', 'nginx', '{}.conf'.format(project_name)),
        path.join(project_directory, '{}-staging.ini'.format(project_name)),
        path.join(project_directory, '{}-prod.ini'.format(project_name)),
        path.join(project_directory, '.env.example'),
    )

    for file_path in files:
        with FileEditor(file_path) as editor:
            editor.replace('PROJECT_NAME', project_name)

    docker_compose_file = path.join(project_directory, 'docker-compose.yml')
    with FileEditor(docker_compose_file) as editor:
        editor.replace('PROJECT_NAME', project_name)
        editor.replace('DB_NAME', project_name)
        editor.replace('DB_USER', project_user)

    fabfile = path.join(project_directory, 'fabfile.py')
    with FileEditor(fabfile) as editor:
        editor.replace('((PROJECT_NAME))', project_name)


@tasks.add
def set_secret_key():
    """
    Put the secret key into settings.py.
    """
    settings_file = path.join(settings_directory, 'settings.py')
    with FileEditor(settings_file) as editor:
        editor.replace('SECRET_KEY = \'\'', 'SECRET_KEY = \'%s\'' % secret_key)


@tasks.add
def set_settings():
    """
    Insert prod and staging settings path string, ssh
    password and database password.
    """
    with FileEditor(path.join(settings_directory, 'settings.py')) as editor:
        editor.replace('((DB_USER))', project_user)
        editor.replace('((DB_NAME))', project_name)
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
    new_project_directory = path.join(parent_directory, project_name)
    rename(project_directory, new_project_directory)

# Must make run_test for docker
# @tasks.add
# def run_tests():
#     """
#     Make sure the project installed correctly
#     by executing management startup and test.
#     """
#     manage('makemigrations nixaemails')
#     manage('startup')
#     manage('test')
