# https://easyengine.io/tutorials/nginx/using-pagespeed/

class django::nginx {
  package { "nginx":
    ensure => present,
  }

  service { "nginx":
    ensure  => running,
    enable  => true,
    require => Package["nginx"],
  }
}


define django::nginx::site (
  $project_path,
  $project_user,
  $staging = false
) {

  if (!$staging) {
    $content = "nginx.erb"
  } else {
    $content = "nginx_staging.erb"
  }
# tODO have nginx actually listen to allowed hosts instead of catchall
  exec { "nginx-remove-default-$project_user":
    onlyif      => "test -f /etc/nginx/sites-enabled/default",
    command     => "rm default",
    cwd         => "/etc/nginx/sites-enabled",
    path        => ["/bin", "/usr/bin"],
  }

  file { "/etc/nginx/sites-available/$project_user":
    ensure      => file,
    group       => $project_user,
    owner       => $project_user,
    mode        => 644,
    content     => template("django/$content"),
    notify      => Service['nginx'],
  }

  file { "/etc/nginx/sites-enabled/$project_user":
    ensure      => 'link',
    target      => "/etc/nginx/sites-available/$project_user",
    notify      => Service['nginx'],
    require     => [
      File["/etc/nginx/sites-available/$project_user"],
      Exec["nginx-remove-default-$project_user"],
    ],
  }
}