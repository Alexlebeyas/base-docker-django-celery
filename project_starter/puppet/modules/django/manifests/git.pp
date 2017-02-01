define django::git (
  $project_path,
  $project_user,
  $project_name,
  $git_repo,
  $git_host,
  $staging = false,
  $branch = "staging",
) {
  $known_hosts = "/home/$project_user/.ssh/known_hosts"

  if !$staging {
    $setting_file = "local_settings.erb"
    $project_branch = "master"
  } else {
    $setting_file = "local_settings_staging.erb"
    $project_branch = $branch
  }
  exec { "$git_host-$project_user-ssh-keyscan":
    user    => $project_user,
    path    => ["/bin", "/usr/bin"],
    unless  => "grep -q $git_host $known_hosts",
    command => "ssh-keyscan -H $git_host >> $known_hosts && echo \"# $git_host\" >> $known_hosts",
  } ->

  vcsrepo { $project_path:
    ensure   => latest,
    provider => git,
    source   => $git_repo,
    user     => $project_user,
    revision => $branch,
  } ->

  file { "$project_path/$project_name/local_settings.py":
    ensure  => file,
    group   => $project_user,
    owner   => $project_user,
    mode    => 744,
    content => template("django/$setting_file"),
  }
}
