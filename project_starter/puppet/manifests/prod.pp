$project_user = "((PROJECT_USER))"
$project_name = "((PROJECT_NAME))"
$db_pass = "((DB_PASS))"
$git_repo = "git@bitbucket.org:nixateam/nixa-fields.git"  # tODO git address here

class { "deploy": } ->

class { "django":
  prod         => true,
} ->

django::project{ $project_name:
  project_name => $project_name,
  project_user => $project_user,
  project_path => "/home/$project_user/project",
  db_user      => $project_user,
  db_name      => $project_name,
  db_pass      => $db_pass,
  git_host     => "bitbucket.org",
  git_repo     => $git_repo,
  prod         => true,
}
