#!/bin/bash

FACTER_install=$1 puppet apply ../manifests/prod.pp \
  --modulepath=../modules:/etc/puppet/modules
