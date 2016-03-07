class { 'django': } ->

django::project{'vagrant':
  project_path => '/vagrant',
  project_user => 'vagrant',
  db_user      => 'vagrant',
  db_name      => 'vagrant',
  db_pass      => 'a',
}