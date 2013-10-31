#!/bin/bash

PUPPET_VERSION=`dpkg -l | grep puppet-common | awk '{ print $3 }' | cut -d- -f1`
dpkg --compare-versions "$PUPPET_VERSION" "<" "3.3" ; OUTDATED=$?

if [ $OUTDATED -eq 0 ] ; then 
    wget -O /tmp/puppet_apt.deb http://apt.puppetlabs.com/puppetlabs-release-precise.deb &> /dev/null
    dpkg -i /tmp/puppet_apt.deb
    DEBIAN_FRONTEND=noninteractive apt-get update -y
    DEBIAN_FRONTEND=noninteractive apt-get install puppet -y
fi

cp /vagrant/puppet/hiera.yaml /etc/puppet/hiera.yaml -f

# TODO make a generic function to help verify if it's already installed
sudo puppet module install saz-timezone --version 1.1.0 --force
sudo puppet module install seocam-supervisor --version 0.0.1 --force

update-locale LC_ALL=''
