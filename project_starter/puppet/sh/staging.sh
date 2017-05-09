#!/bin/bash

FACTER_install=$1 FACTER_branch=$2 puppet apply ../manifests/staging.pp \
  --modulepath=../modules:/etc/puppet/modules
