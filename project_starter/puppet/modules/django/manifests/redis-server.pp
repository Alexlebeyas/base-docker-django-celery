# tODO try other redis modules

class django::redis-server {
  $redis_user = "redis"

  group { $redis_user:
    ensure => present,
  } ->

  user { $redis_user:
    ensure     => present,
    groups     => [$redis_user],
  } ->

  class { "redis":
    redis_user         => $redis_user,
    redis_group        => $redis_user,
    version            => "2.8.18",
    redis_bind_address => "localhost",
  }
}
