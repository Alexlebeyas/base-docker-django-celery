class deploy::filesystem (
  $username,
) {
  file { "/etc/puppet/sync":
    ensure  => directory,
    group   => $username,
    owner   => $username,
    mode    => 755,
    notify  => Exec["sync-permissions"],
  }

  exec { "sync-permissions":
    command     => "chown $username:$username -R sync/ && chmod 755 -R sync/",
    cwd         => "/etc/puppet",
    path        => ["/bin"],
    refreshonly => true,
  }
}