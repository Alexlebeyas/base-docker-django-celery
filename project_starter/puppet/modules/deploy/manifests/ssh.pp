class deploy::ssh {
  class { 'ssh::server':
    storeconfigs_enabled => false,
    options => {
      'PasswordAuthentication' => 'no',
      'PermitRootLogin'        => 'no',
      'Port'                   => [22, 2222],
    },
  }
}
