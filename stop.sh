#!/bin/bash
echo 'stopping...'
pid=`cat /var/run/imager/imager.pid`
kill -9 $pid

echo "stopping imager successfully"