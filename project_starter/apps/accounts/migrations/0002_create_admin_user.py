# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    def create_admin_user(apps, schema_editor):
        User = apps.get_model('accounts', 'User')
        User.objects.create(
            email="dev@nixa.ca", password=(
                'pbkdf2_sha256$12000$ffkdLUaJVjNL$54Ti'
                'Mba/CmxJL2P9ASiBHgL0rUF1QImecCwPCDUKsA0='
            ), is_superuser=True, is_staff=True, is_active=True,
            first_name="dev", last_name="at nixa"
        )

    def del_admin_user(apps, schema_editor):
        User = apps.get_model('accounts', 'User')
        User.objects.filter(email="dev@nixa.ca").delete()

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin_user, del_admin_user),
    ]
