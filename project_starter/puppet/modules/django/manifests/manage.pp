define django::manage (
  $project_user,
  $project_path,
  $venv_dir,
) {
  exec { "collectstatic-$project_user":
    user        => $project_user,
    cwd         => $project_path,
    path        => ["$venv_dir/bin"],
    command     => "python manage.py collectstatic --noinput",
    refreshonly => true,
  }

  exec { "migrate-$project_user":
    user        => $project_user,
    cwd         => $project_path,
    path        => ["$venv_dir/bin"],
    command     => "python manage.py migrate --noinput",
    refreshonly => true,
  }
}