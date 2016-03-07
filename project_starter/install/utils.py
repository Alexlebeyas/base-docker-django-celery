"""
UTILS

Contains utility functions for other modules in
this package. To avoid circular import, this module
should not import any other module in this package.
"""

import re
from os import system, path, sep
from shutil import rmtree
from uuid import uuid4

__author__ = 'snake'
re_non_alpha = re.compile(r'[^a-z0-9]+')
make_project_user = lambda project_name: re_non_alpha.sub('', project_name.lower())
random_password = lambda: str(uuid4()).replace('-', '')


def run(cmd):
    """
    Call python command.
    """
    system('python %s' % cmd)


def manage(cmd):
    """
    Call management command.
    """
    run('manage.py %s' % cmd)


def cleanup():
    """
    Remove traces of this package.
    """
    rmtree(path.dirname(__file__))


def print_task(task):
    """
    Utility for nice prints.
    """
    print('Executing: %s' % task.__name__)


def get_project_directory():
    """
    Find the path to the top level directory
    of the current project.
    """
    directory = path.abspath(__file__)
    directory = sep.join(directory.split(sep)[:-2])
    return directory


class FileEditor(object):
    """
    Update a file at `filepath`. Using the "with"
    statement, the content of the file is loaded
    into self.content and saved on exit.
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.file = None
        self.content = ''

    def __enter__(self):
        self.file = open(self.filepath, mode='r+')
        self.content = self.file.read()
        return self

    def __exit__(self, *a, **k):
        self.file.seek(0)
        self.file.write(self.content)
        self.file.truncate()
        self.file.close()

    def replace(self, old, new):
        """
        Typical search and replace of `old` with `new`
        and update the current file's content.
        """
        self.content = self.content.replace(old, new)

    def replace_token(self, token, value):
        """
        Search and replace ((token)) inside file and
        replace content with `value`
        """
        self.replace('((%s))' % token, value)


class TaskManager(object):
    """
    This object takes charge of keeping a list of task
    functions to be executed during installation. Also
    provides the decorator @tasks.add where 'tasks' is
    an instance of TaskManager.
    """

    def __init__(self):
        self.tasks = []

    def __iter__(self):
        return iter(self.tasks)

    def __str__(self):
        return '<TaskManager: %s>' % str(self.tasks)

    def __call__(self):
        """
        Execute all tasks.
        """
        for task in self:
            print_task(task)
            task()

    def add(self, func):
        """
        Decorator for adding a task to the
        list of tasks to be executed.
        """
        self.tasks.append(func)
