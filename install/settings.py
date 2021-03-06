"""
SETTINGS

This module holds the information for the new project.
Most of them are paths or credentials.
"""

import sys
from os import path
from utils import get_project_directory, random_password, make_project_user

__author__ = 'snake'
ocean = sys.argv[1].lower()
project_user = make_project_user(ocean)
project_directory = get_project_directory()
settings_directory = path.join(project_directory, ocean)
secret_key = random_password()
ssh_pass = random_password()
db_pass = random_password()
