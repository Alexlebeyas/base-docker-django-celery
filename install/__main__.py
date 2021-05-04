"""
Django Project Installer

Finish the installation of this project template:
>> python install ocean
"""

from utils import cleanup
from tasks import tasks

__author__ = 'snake'
tasks.add(cleanup)
tasks()
