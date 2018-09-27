from __future__ import print_function, absolute_import, unicode_literals
import os
from django.core.management import BaseCommand, call_command
from django.conf import settings
from django.db import connection
from .ns import nixasaur

__author__ = 'snick'

NAME = settings.DATABASES['default']['NAME']
ENGINE = settings.DATABASES['default']['ENGINE']


class Command(BaseCommand):
    """
    Startup restores the main database to its original state. Loads fixtures. Create base user.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--prod',
            action='store_true',
            default=False,
            help='Do a startup in production. yeah really.',
        )

    def handle(self, prod, **options):
        if settings.DEBUG or prod:
            print(nixasaur)
            self.drop_tables()
            self.migrate()
            self.load_fixtures()
        elif not prod and not settings.DEBUG:
            print("You must add --prod to make a startup in production")

    @staticmethod
    def drop_sqlite():
        """
        Removes the sqlite db file.
        """
        if os.path.exists(NAME):
            os.remove(NAME)

    @staticmethod
    def drop_postgres():
        """
        Introspect all table names and perform DROP statement on each of them.
        """
        tables = connection.introspection.table_names()
        cursor = connection.cursor()
        for table in tables:
            cursor.execute("DROP TABLE %s CASCADE;" % table)

    @classmethod
    def drop_tables(cls):
        """
        Identify the database backend and execute the matching function to reset it.
        """
        if "sqlite" in ENGINE:
            cls.drop_sqlite()
        elif "postgres" in ENGINE:
            cls.drop_postgres()

    @staticmethod
    def migrate():
        call_command('migrate')

    @staticmethod
    def load_fixtures():
        for initial_fixture in settings.STARTUP_INITIAL_FIXTURES:
            print(initial_fixture)
            call_command('loaddata', initial_fixture, )
