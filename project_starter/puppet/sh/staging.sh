#!/bin/bash

puppet apply ../manifests/staging.pp \
  --modulepath=../modules:/etc/puppet/modules
