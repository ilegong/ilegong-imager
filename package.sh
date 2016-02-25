#!/bin/sh
trap 'echo CTRL-C was pressed, will exit; exit 1' 2
package="ilegong_imager"
rm -rf $package.zip

zip -r $package.zip . -x ".git/*" "*.zip" "*.sh"> /dev/null

if [ "$1" = "" ]; then
  host="static.tongshijia.com"
else
  host=$1
fi
echo "upload to host $host"

scp -P 9527 $package.zip iler@$host:/www/imager/
