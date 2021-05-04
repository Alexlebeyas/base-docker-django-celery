from os.path import join, realpath, dirname


class UpStartFile:

    def __init__(self, django='none', user='none', ocean='none', docker_compose_file='none'):
        with open(join(dirname(realpath(__file__)), 'templates', 'upstart_file.conf'), 'r') as template_file:
            self.TEMPLATE = template_file.read()
        self.django = django
        self.user = user
        self.ocean = ocean
        self.docker_compose_file = docker_compose_file

    def output(self):
        return self.TEMPLATE.format(**{
            'django': self.django,
            'user': self.user,
            'ocean': self.ocean,
            'docker_compose_file': self.docker_compose_file,
        })
