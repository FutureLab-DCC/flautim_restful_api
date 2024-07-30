#!/bin/sh
### BEGIN INIT INFO
# Provides:          <NAME>
# Required-Start:    $local_fs $network $named $time $syslog
# Required-Stop:     $local_fs $network $named $time $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       <DESCRIPTION>
### END INIT INFO

HOME=/var/www/flautim

DJANGO_COMMAND=$HOME/django.sh
CELERY_COMMAND=$HOME/celery.sh

start() {
 nohup $CELERY_COMMAND & 
 nohup $DJANGO_COMMAND &
}

stop() {
  PIDS=`ps -ax | grep celery | awk -v OFS='\t' '{print $1 }'`
  for PID in $PIDS
  do
    kill -9 $PID
  done

  PIDS=`ps -ax | grep manage.py | awk -v OFS='\t' '{print $1 }'`
  for PID in $PIDS
  do
    kill -9 $PID
  done

}

status() {
  if [ -f $CELERY_PIDFILE ] && kill -0 $(cat $CELERY_PIDFILE); then
    echo 'Service Celery is running' >&2
  else
    echo 'Service Celery is not running' >&2
  fi
  
  if [ -f $DJANGO_PIDFILE ] && kill -0 $(cat $DJANGO_PIDFILE); then
    echo 'Service Django is running' >&2
  else
    echo 'Service Django is not running' >&2
  fi
}

case "$1" in
  start)
    start
    ;;
  status)
    status
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: $0 {status|start|stop|restart}"
esac