# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import libs.nixa_fields.fields
import apps.accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('lang', models.CharField(choices=[('fr', 'Français'), ('en', 'English')], verbose_name='Email Language', max_length=8, default='fr')),
                ('can_receive_emails', models.BooleanField(verbose_name='Wants to receive emails', default=True)),
                ('email', libs.nixa_fields.fields.EmailField(unique=True, verbose_name='Email', max_length=254)),
                ('password', libs.nixa_fields.fields.PasswordField(verbose_name='Password', max_length=128)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_staff', models.BooleanField(verbose_name='Staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='Active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('first_name', libs.nixa_fields.fields.FirstNameField(verbose_name='First name', max_length=256)),
                ('last_name', libs.nixa_fields.fields.LastNameField(verbose_name='Last name', max_length=256)),
                ('groups', models.ManyToManyField(verbose_name='groups', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', to='auth.Group', blank=True)),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', related_query_name='user', help_text='Specific permissions for this user.', related_name='user_set', to='auth.Permission', blank=True)),
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
