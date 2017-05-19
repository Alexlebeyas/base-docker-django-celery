class deploy (
  $username = 'deploy',
  $install = 'false'
) {

  class { 'deploy::user':
    username => 'deploy',
    install  => $install,
  }

  class { 'deploy::filesystem':
    username => 'deploy',
    require  => Class['deploy::user'],
  }

  class { 'deploy::ssh':
    require => Class['deploy::filesystem'],
  }
}