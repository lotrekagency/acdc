#!/bin/bash


if [ "$1" = "start" ]; then
    gunicorn campaign_service.wsgi -c gunicorn_settings.py --name gunicorn_campaign_service --timeout=500 --graceful-timeout=500 --log-file error_logs.log
fi

if [ "$1" = "restart" ]; then
    sleep 2
    ps aux | grep gunicorn_campaign_service | awk '{ print $2 }' | xargs kill -HUP
fi
