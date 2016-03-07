#!/bin/bash

puppet apply ../manifests/prod.pp \
  --modulepath=../modules:/etc/puppet/modules
