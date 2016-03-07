class django::postgresql {
  class { 'postgresql::server': }

  package { 'libpq-dev':
    ensure => present,
  }
}

define django::postgresql::role (
  $db_user,
  $db_name,
  $db_pass,
) {
  postgresql::server::role { $db_user:
    password_hash => postgresql_password($db_user, $db_pass),
    createdb      => true,
  } ->

  postgresql::server::database { $db_name :
    owner   => $db_user,
  }
}