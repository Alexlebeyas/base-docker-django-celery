#!/usr/bin/python

"""
Deployment script
"""

from __future__ import print_function, absolute_import
import argparse
from subprocess import call

__author__ = 'snake'

PROJECT_USER = '((PROJECT_USER))'
DEPLOY_USER = 'deploy'
PROD_HOST = '127.0.0.1'  # tODO Prod IP here
STAGING_HOST = '127.0.0.1'  # tODO Staging IP here

commands = {}
command = lambda f: commands.__setitem__(f.__name__, f) or f


@command
def deploy(user=DEPLOY_USER, host=PROD_HOST, debug=False, **kwargs):
    # PROD
    if not debug:
        rsync(user=user, host=host)
    ssh('cd /etc/puppet/sync/sh && sudo ./prod.sh', user=user, host=host)


@command
def deploy_staging(user=DEPLOY_USER, host=STAGING_HOST, debug=False, **kwargs):
    # STAGING
    if not debug:
        rsync(user=user, host=host)
    ssh('cd /etc/puppet/sync/sh && sudo ./staging.sh', user=user, host=host)


@command
def git_key(user=DEPLOY_USER, host=PROD_HOST, project_user=PROJECT_USER, **kwargs):
    ssh('sudo cat /home/%(project_user)s/.ssh/id_rsa.pub' % {
        'project_user': project_user,
    }, user=user, host=host)


@command
def rsync(local='.', remote='/etc/puppet/sync', user=DEPLOY_USER, host=PROD_HOST, **kwargs):
    call_command('rsync -rtvz -e ssh %(local)s %(user)s@%(host)s:%(remote)s' % {
        'local': local,
        'user': user,
        'host': host,
        'remote': remote,
    })


@command
def install_puppet(user='root', host=PROD_HOST, debug=False, **kwargs):
    # PROD
    ssh('mkdir /etc/puppet', user=user, host=host)
    ssh('mkdir --mode=755 /opt', user=user, host=host)
    rsync(user=user, host=host)
    ssh('cd /etc/puppet/sync/sh && chmod 770 *.sh && sudo ./install.sh', user=user, host=host)

    if not debug:
        deploy(user=user, host=host)


@command
def install_puppet_staging(user='root', host=STAGING_HOST, debug=False, **kwargs):
    # STAGING
    install_puppet(user=user, host=host, debug=debug)


def ssh(cmd, user, host):
    call_command('ssh %(user)s@%(host)s "%(cmd)s"' % {
        'user': user,
        'host': host,
        'cmd': cmd.replace('"', '\\"'),
    })


def call_command(cmd):
    call((cmd,), shell=True)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root', action='store_true', help='ssh as root')
    parser.add_argument('-d', '--debug', action='store_true', help='run with minimal execution')
    parser.add_argument('command', nargs='?', help=', '.join(commands.keys()))
    args = parser.parse_args()
    kwargs = {'debug': args.debug}
    if args.root:
        kwargs['user'] = 'root'
    commands.get(args.command, deploy)(**kwargs)


parse_args()
