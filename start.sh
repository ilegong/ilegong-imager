#!/bin/bash

echo 'starting...'
package="ilegong_imager"
cd latest
nohup gunicorn $package.wsgi:application -b 127.0.0.1:8000 --reload >/var/log/imager/imager.log 2>&1 &
pid=$!
echo $pid > /var/run/imager/imager.pid

echo "start imager with pid $pid successfully"