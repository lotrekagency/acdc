#!/bin/bash

if [ "$1" = "stop" ]; then
    cat huey.pid | xargs kill -9
    rm huey.pid
fi

if [ "$1" = "start" ]; then
    rm huey_logs.log
    python manage.py run_huey --logfile huey_logs.log &> /dev/null &
    echo $! > huey.pid
fi
