#!/bin/bash

FACTER_branch=$1 puppet apply ../manifests/staging.pp \
  --modulepath=../modules:/etc/puppet/modules
