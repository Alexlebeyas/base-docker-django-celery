define django::user (
  $project_user,
) {
  $key_file = "/home/$project_user/.ssh/id_rsa"

  group { $project_user:
    ensure => present,
  } ->

  user { $project_user:
    ensure     => present,
    groups     => [$project_user],
    home       => "/home/$project_user",
    managehome => "true",
    shell      => '/bin/bash',
  } ->

  file { "/home/$project_user":
    ensure  => directory,
    group   => $project_user,
    owner   => $project_user,
    mode    => 755,
  } ->

  file { "/home/$project_user/.ssh":
    ensure  => directory,
    group   => $project_user,
    owner   => $project_user,
    mode    => 700,
  } ->

  exec { "ssh-key-$project_user":
    user    => $project_user,
    path    => ["/usr/bin"],
    onlyif  => "test ! -f $key_file",
    command => "ssh-keygen -N \"\" -f $key_file",
  }
}