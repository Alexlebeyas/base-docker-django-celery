define django::supervisor (
  $home,
  $project_user,
  $logs,
  $venv_dir,
) {
  file { "/etc/supervisor/conf.d/program_django_$project_user.conf":
    ensure  => file,
    group   => $project_user,
    owner   => $project_user,
    mode    => 744,
    content => template("django/supervisord.erb"),
    notify  => Exec["supervisor-reload-$project_user"],
  }

  exec { "supervisor-reload-$project_user":
    user        => "root",
    path        => ["/usr/bin", "/usr/local/bin"],
    command     => "supervisorctl reload",  # tODO reload is not good for multiple projects running on single node.
    refreshonly => true,
  }
}