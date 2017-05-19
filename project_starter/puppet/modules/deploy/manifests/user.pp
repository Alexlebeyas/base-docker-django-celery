class deploy::user (
  $username,
  $install = "false"
) {
  $home = "/home/$username"

  group { $username:
    ensure => present,
  }

  user { $username:
    ensure     => present,
    groups     => [$username, 'root'],
    home       => $home,
    managehome => "true",
    shell      => '/bin/bash',
  }

  file { $home:
    ensure  => directory,
    group   => $username,
    owner   => $username,
    mode    => 700,
    require => User[$username],
  }

  file { "$home/.ssh":
    ensure  => directory,
    group   => $username,
    owner   => $username,
    mode    => 700,
    require => File[$home],
  }

  if $install == "true" {
      file { "$home/.ssh/authorized_keys":
      ensure  => file,
      group   => $username,
      owner   => $username,
      mode    => 600,
      content => template("deploy/authorized_keys.erb"),
      require => File["$home/.ssh"],
    }
  }


  file { "/etc/sudoers.d/${$username}":
    ensure  => file,
    content => "${$username} ALL=(ALL) NOPASSWD:ALL",
    mode    => 600,
    require => User[$username],
  }
}