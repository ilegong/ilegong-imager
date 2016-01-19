#!/bin/sh
trap 'echo CTRL-C was pressed, will exit; exit 1' 2
package="ilegong_imager"
rm -rf $package.zip

zip -r $package.zip . -x ".git/*" "*.zip" "*.sh"> /dev/null

scp -P 9527 $package.zip iler@static.tongshijia.com:/www/imager/
