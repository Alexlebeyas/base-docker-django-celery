#!/bin/bash

apt-get update
apt-get -y install puppet
puppet module install puppetlabs-postgresql --version 4.6.0; true
puppet module install puppetlabs-vcsrepo --version 1.3.1; true
puppet module install saz-ssh --version 2.8.1; true
puppet module install thomasvandoren-redis --version 0.10.0; true
