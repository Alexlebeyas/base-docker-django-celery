# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import apps.accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('lang', models.CharField(verbose_name='Language', default='fr', max_length='10', choices=[('fr', 'Français'), ('en', 'English')])),
                ('can_receive_emails', models.BooleanField(default=True, verbose_name='Want to receive mails')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('password', models.CharField(max_length=128, verbose_name='Password')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='Staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='Active')),
                ('first_name', models.CharField(max_length=75, verbose_name='First name')),
                ('last_name', models.CharField(max_length=75, verbose_name='Last name')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', to='auth.Group', related_name='user_set', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions', to='auth.Permission', related_name='user_set', related_query_name='user')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', apps.accounts.models.UserManager()),
            ],
        ),
    ]
