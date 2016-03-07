define django::filesystem (
  $home,
  $project_user,
  $logs,
) {
  file { "$home/activate":
    ensure  => file,
    group   => $project_user,
    owner   => $project_user,
    mode    => 700,
    content => template("django/activate.erb"),
  }

  file { $logs:
    ensure  => directory,
    group   => $project_user,
    owner   => $project_user,
    mode    => 755,
  }
}