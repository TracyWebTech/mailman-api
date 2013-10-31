#!/bin/sh
 
set -e
 
NAME=mailmanapi
PIDFILE=/var/run/$NAME.pid
DAEMON="/opt/mailman-api/bin/python /opt/mailman-api/mailman-api-master/scripts/run.py"
DAEMON_OPTS=""
 
export PATH="${PATH:+$PATH:}/usr/sbin:/sbin"
 
case "$1" in
start)
echo -n "Starting daemon: "$NAME
start-stop-daemon --start --quiet --pidfile $PIDFILE --exec $DAEMON -- $DAEMON_OPTS
echo "."
;;
stop)
echo -n "Stopping daemon: "$NAME
start-stop-daemon --stop --quiet --oknodo --pidfile $PIDFILE
echo "."
;;
restart)
echo -n "Restarting daemon: "$NAME
start-stop-daemon --stop --quiet --oknodo --retry 30 --pidfile $PIDFILE
start-stop-daemon --start --quiet --pidfile $PIDFILE --exec $DAEMON -- $DAEMON_OPTS
echo "."
;;
 
*)
echo "Usage: "$1" {start|stop|restart}"
exit 1
esac
 
exit 0
