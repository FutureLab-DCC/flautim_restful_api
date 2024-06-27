#!/bin/sh
### BEGIN INIT INFO
# Provides:          <NAME>
# Required-Start:    $local_fs $network $named $time $syslog
# Required-Stop:     $local_fs $network $named $time $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       <DESCRIPTION>
### END INIT INFO

HOME=

DJANGO_COMMAND=$HOME/django.sh
CELERY_COMMAND=$HOME/celery.sh
RUNAS=root

DJANGO_PIDFILE=/var/run/django.pid
DJANGO_LOGFILE=/var/log/django.log

CELERY_PIDFILE=/var/run/celery.pid
CELERY_LOGFILE=/var/log/celery.log

start() {
  if [ -f $CELERY_PIDFILE ] && kill -0 $(cat $CELERY_PIDFILE); then
    echo 'Service Celery is already running' >&2
  else
    echo 'Starting Celery service…' >&2
    local CMD="$CELERY_COMMAND &> \"$CELERY_LOGFILE\" & echo \$!"
    su -c "$CMD" $RUNAS > "$CELERY_PIDFILE"
    echo 'Service Celery started' >&2
  fi
  
  if [ -f $DJANGO_PIDFILE ] && kill -0 $(cat $DJANGO_PIDFILE); then
    echo 'Service Django is already running' >&2
  else
    echo 'Starting Django service…' >&2
    local CMD="$DJANGO_COMMAND &> \"$DJANGO_LOGFILE\" & echo \$!"
    su -c "$CMD" $RUNAS > "$DJANGO_PIDFILE"
    echo 'Service Django started' >&2
  fi
}

stop() {
  if [ ! -f "$DJANGO_PIDFILE" ] || ! kill -0 $(cat "$DJANGO_PIDFILE"); then
    echo 'Service Django is not running' >&2
  else 
    echo 'Stopping Django service…' >&2
    kill -15 $(cat "$DJANGO_PIDFILE") && rm -f "$DJANGO_PIDFILE"
    echo 'Service Django stopped' >&2
  fi

  if [ ! -f "$CELERY_PIDFILE" ] || ! kill -0 $(cat "$CELERY_PIDFILE"); then
    echo 'Service Celery is not running' >&2
  else 
    echo 'Stopping Celery service…' >&2
    kill -15 $(cat "$CELERY_PIDFILE") && rm -f "$CELERY_PIDFILE"
    echo 'Service Celery stopped' >&2
  fi
  
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