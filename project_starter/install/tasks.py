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
        path.join(settings_directory, 'staging.py')
    )
    for file_path in files:
        with FileEditor(file_path) as editor:
            editor.replace_token('DB_USER', project_user)
            editor.replace_token('DB_NAME', project_name)
            editor.replace_token('DB_PASS', db_pass)


@tasks.add
def set_puppet_prod_settings():
    """
    Insert project variables into puppet's prod.pp.
    """
    files = (
        path.join(project_directory, 'puppet', 'manifests', 'prod.pp'),
        path.join(project_directory, 'puppet', 'manifests', 'staging.pp'),
    )
    for file_path in files:
        with FileEditor(file_path) as editor:
            editor.replace_token('PROJECT_USER', project_user)
            editor.replace_token('PROJECT_NAME', project_name)
            editor.replace_token('DB_PASS', db_pass)


@tasks.add
def set_puppet_deploy_settings():
    """
    Insert project variables into puppet's deploy.py.
    """
    puppet_prod_settings_file = path.join(project_directory, 'puppet', 'deploy.py')
    with FileEditor(puppet_prod_settings_file) as editor:
        editor.replace_token('PROJECT_USER', project_user)


@tasks.add
def run_tests():
    """
    Make sure the project installed correctly
    by executing management startup and test.
    """
    manage('startup')
    manage('test')
