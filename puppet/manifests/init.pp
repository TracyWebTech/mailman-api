
include vim
include ntp
include locale
include timezone
include supervisor

package { 'mailman':
  ensure => installed,
}

package { 'sqlite3':
  ensure => installed,
}

package { 'libsqlite3-dev':
  ensure => installed,
}

package { 'mailcatcher':
  ensure   => installed,
  provider => gem,
  require  => Package['libsqlite3-dev', 'sqlite3'],
}

package { 'git':
  ensure => installed,
}

# req to install python pkgs
package { 'python-pip':
  ensure => installed,
}

# req to create virtualenvs
package { 'virtualenvwrapper':
  ensure   => installed,
  provider => pip,
  require  => Package['python-pip'],
}

# links virtualenvwrapper to load automaticaly
file { '/etc/bash_completion.d/virtualenvwrapper.sh':
  ensure => link,
  target => '/usr/local/bin/virtualenvwrapper.sh',
}

# req for any compilation
package { 'build-essential':
  ensure => installed,
}

# req for compiling every python pkg
package { 'python-dev':
  ensure => installed,
}

supervisor::app { 'mailcatcher':
  command   => '/opt/vagrant_ruby/bin/mailcatcher --foreground --ip 0.0.0.0',
  directory => '/home/vagrant/',
  user      => 'vagrant',
  require   => Package['mailcatcher'],
}
