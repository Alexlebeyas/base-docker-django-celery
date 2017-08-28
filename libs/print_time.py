from __future__ import unicode_literals, print_function
import re
from django.db import connection
from time import time
from six import wraps

__author__ = 'snake'

PRINT_TIME_MSG = 'PRINTTIME "%s": %s'
QUERY_COUNT_MSG = 'QUERY COUNT: %s'
QUERIES_MSG = '%s\n'

re_query_split = re.compile(r' (FROM|WHERE|- PARAMS) ')


def format_query(query):
    query = re_query_split.sub(r'\n \1', query)
    return query


class PrintTime(object):
    def __init__(self, name=None, show_queries=False, output=print, msg=PRINT_TIME_MSG):
        self.name = name
        self.show_queries = show_queries
        self.query_start = 0
        self.output = output
        self.msg = msg

    def __call__(self, func):
        self.name = self.name if self.name else func.__name__

        def _wrapper(*args, **kwargs):
            self._start()
            try:
                func_return = func(*args, **kwargs)
            finally:
                self._finish()
            return func_return

        return wraps(func)(_wrapper)

    def __enter__(self):
        self._start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._finish()

    def _start(self):
        if self.show_queries:
            self.query_start = len(connection.queries)
        self.start = time()

    def _finish(self):
        time_ = round(time() - self.start, 3)
        self.output(self.msg % (self.name, time_, ))

        if self.show_queries:
            connection_queries = connection.queries[self.query_start:]
            self.output(QUERY_COUNT_MSG % len(connection_queries))
            self.output(QUERIES_MSG % '\n'.join(format_query(query['sql']) for query in connection_queries))