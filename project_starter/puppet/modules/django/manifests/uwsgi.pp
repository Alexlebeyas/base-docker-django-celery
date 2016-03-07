define django::uwsgi (
  $home,
  $project_path,
  $project_user,
  $project_name,
  $venv_dir,
  $logs,
) {

  file { "$home/uwsgi.ini":
    ensure  => file,
    group   => $project_user,
    owner   => $project_user,
    mode    => 700,
    content => template("django/uwsgi.erb"),
  }
}