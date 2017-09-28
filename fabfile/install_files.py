from os.path import join, realpath, dirname


class UpStartFile:

    def __init__(self, django='none', user='none', project_name='none', docker_compose_file='none'):
        with open(join(dirname(realpath(__file__)), 'templates', 'upstart_file.conf'), 'r') as template_file:
            self.TEMPLATE = template_file.read()
        self.django = django
        self.user = user
        self.project_name = project_name
        self.docker_compose_file = docker_compose_file

    def output(self):
        return self.TEMPLATE.format(**{
            'django': self.django,
            'user': self.user,
            'project_name': self.project_name,
            'docker_compose_file': self.docker_compose_file,
        })


class RsysDockerConf:

    def __init__(self):
        with open(join(dirname(realpath(__file__)), 'templates', '10-docker.conf'), 'r') as template_file:
            self.TEMPLATE = template_file.read()

    def output(self):
        return self.TEMPLATE

