"""
TASKS

Regroupment of tasks that will be executed by the
main script. Each task needs to have the decorator
@tasks.add or they will not be detected. Tasks are
executed in order.
"""

from os import path, renames
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
    docker_file = path.join(project_directory, 'Dockerfile')
    with FileEditor(docker_file) as editor:
        editor.replace('PROJECT_NAME', project_name)
    docker_compose_file = path.join(project_directory, 'docker-compose.yml')
    with FileEditor(docker_compose_file) as editor:
        editor.replace('DB_NAME', project_name)
        editor.replace('DB_USER', project_user)

    gulp_docker_file = path.join(project_directory, 'gulp', 'Dockerfile')
    with FileEditor(gulp_docker_file) as editor:
        editor.replace('PROJECT_NAME', project_name)


@tasks.add
def set_secret_key():
    """
    Put the secret key into settings.py.
    """
    settings_file = path.join(settings_directory, 'settings.py')
    with FileEditor(settings_file) as editor:
        editor.replace('SECRET_KEY = \'\'', 'SECRET_KEY = \'%s\'' % secret_key)


@tasks.add
def set_prod_settings():
    """
    Insert prod and staging settings path string, ssh
    password and database password.
    """
    files = (
        path.join(settings_directory, 'prod.py'),
        path.join(settings_directory, 'staging.py'),
        path.join(settings_directory, 'settings.py'),
    )
    for file_path in files:
        with FileEditor(file_path) as editor:
            editor.replace('((DB_USER))', project_user)
            editor.replace('((DB_NAME))', project_name)
            editor.replace('((DB_PASS))', db_pass)


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
