class django::py (
  $py_version = "3.4",
) {
  package { "python-setuptools":
    ensure => present,
  }
  package { "python-psycopg2":
    ensure => present,
  }

  class { "python" :
    version    => $py_version,
    pip        => true,
    dev        => true,
    virtualenv => true,
  }
}

define django::py::venv (
  $project_user,
  $project_path,
  $venv_dir,
  $py_version = "3.4",
  $pip_requirements = "requirements.txt",
) {
  python::virtualenv { "python-env-$project_user" :
    ensure       => present,
    version      => $py_version,
    requirements => "$project_path/$pip_requirements",
    venv_dir     => $venv_dir,
    owner        => $project_user,
    group        => $project_user,
    cwd          => $project_path,
  }

  python::pip { "uwsgi-$project_user" :
    pkgname    => "uwsgi",
    virtualenv => $venv_dir,
    owner      => $project_user,
    require    => Python::Virtualenv["python-env-$project_user"],
  }

  python::pip { "psycopg2-$project_user" :
    pkgname    => "psycopg2",
    ensure     => "2.6.1",
    virtualenv => $venv_dir,
    owner      => $project_user,
    require    => Python::Virtualenv["python-env-$project_user"],
  }

  python::pip { "django-redis-cache-$project_user" :
    pkgname    => "django-redis-cache",
    ensure     => "1.6.3",
    virtualenv => $venv_dir,
    owner      => $project_user,
    require    => Python::Virtualenv["python-env-$project_user"],
  }

#  python::pip { "celery-$project_user" :
#    pkgname    => "celery",
#    ensure     => "3.1.18",
#    virtualenv => $venv_dir,
#    owner      => $project_user,
#    require    => Python::Virtualenv["python-env-$project_user"],
#  }
}