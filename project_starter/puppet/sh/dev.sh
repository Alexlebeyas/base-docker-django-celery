#!/bin/bash

puppet apply ../manifests/dev.pp \
  --modulepath=../modules:/etc/puppet/modules
