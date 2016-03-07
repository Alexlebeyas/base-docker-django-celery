#!/bin/bash
# Helper script for testing prod in vagrant environment.

sudo -u vagrant ssh-keygen -N "" -f /home/vagrant/.ssh/id_rsa
cat /home/vagrant/.ssh/id_rsa.pub
cat /home/vagrant/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
