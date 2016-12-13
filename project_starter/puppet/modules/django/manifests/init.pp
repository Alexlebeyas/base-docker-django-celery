class django (
  $prod = false,
  $py_version = '3.4',
) {
  class { "django::postgresql": }
  class { "django::redis-server": }
  class { "django::py":
    py_version => $py_version,
  }

  if $prod {
    class { "django::nginx": }
    package { "git": }
    package { "fail2ban": }
    package { "supervisor": }
  }
}

define django::project (
  $project_path,
  $project_user,
  $db_user,
  $db_name,
  $db_pass,
  $project_name = false,
  $git_repo = false,
  $git_host = false,
  $prod = false,
  $staging = false,
  $py_version = '3.4',
) {
  $home = "/home/$project_user"
  $logs = "$home/logs"
  $venv_dir = "/home/${project_user}/venv"

# tODO passworded redis instance
# tODO add puppet to startproject

  django::user { $project_user:
    project_user => $project_user,
  } ->

  django::filesystem { "filesystem-$project_user":
    home         => $home,
    project_user => $project_user,
    logs         => $logs,
  }

  django::postgresql::role { "postgresql-$project_user":
    db_user => $db_user,
    db_name => $db_name,
    db_pass => $db_pass,
  }

  if !$prod {
    django::py::venv { "venv-$project_user":
      project_user => $project_user,
      project_path => $project_path,
      venv_dir     => $venv_dir,
      py_version   => $py_version,
      require      => [
        Django::Filesystem["filesystem-$project_user"],
        Django::Postgresql::Role["postgresql-$project_user"],
      ],
    }
  } else {
    $app_restart = [
      Exec["collectstatic-$project_user"],
      Exec["migrate-$project_user"],
      Exec["supervisor-reload-$project_user"],
    ]

    django::manage { "manage-$project_user":
      project_user => $project_user,
      project_path => $project_path,
      venv_dir     => $venv_dir,
    }

    django::git { "git-$project_user":
      project_path => $project_path,
      project_user => $project_user,
      project_name => $project_name,
      git_repo     => $git_repo,
      git_host     => $git_host,
      staging      => $staging,
      notify       => $app_restart,
      require      => [
        Django::Filesystem["filesystem-$project_user"],
        Django::Postgresql::Role["postgresql-$project_user"],
      ],
    } ->

    django::py::venv { "venv-$project_user":
      project_user => $project_user,
      project_path => $project_path,
      venv_dir     => $venv_dir,
      notify       => $app_restart,
    } ->

    django::uwsgi { "uwsgi-$project_user":
      home           => $home,
      project_path   => $project_path,
      project_user   => $project_user,
      project_name   => $project_name,
      venv_dir       => $venv_dir,
      logs           => $logs,
      notify         => Exec["supervisor-reload-$project_user"],
    } ->

    django::supervisor { "supervisor-$project_user":
      home           => $home,
      project_user   => $project_user,
      logs           => $logs,
      venv_dir       => $venv_dir,
    } ->

    django::nginx::site { "nginx-$project_user":
      project_path   => $project_path,
      project_user   => $project_user,
      staging        => $staging,
    }
  }
}