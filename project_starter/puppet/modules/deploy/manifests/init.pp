class deploy (
  $username = 'deploy',
) {

  class { 'deploy::user':
    username => 'deploy',
  }

  class { 'deploy::filesystem':
    username => 'deploy',
    require  => Class['deploy::user'],
  }

  class { 'deploy::ssh':
    require => Class['deploy::filesystem'],
  }
}