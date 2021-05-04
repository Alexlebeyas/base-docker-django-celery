from __future__ import absolute_import
from django.conf import settings
from django.core.management import BaseCommand
from django.utils import translation
from logging import getLogger


__author__ = 'snake'


class ModuleCommand(BaseCommand):
    module = None
    logger = getLogger('main')

    def add_arguments(self, parser):
        parser.add_argument('method')

    def handle(self, method, **options):
        # Activate default language to avoid i18n/l10n errors in management functions.
        translation.activate(settings.LANGUAGE_CODE)

        try:
            getattr(self.module, method)()
        except Exception as e:
            self.logger.exception(e)
            raise