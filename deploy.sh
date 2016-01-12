#!/bin/bash
trap 'echo CTRL-C was pressed, will exit; exit 1' 2

package="ilegong_imager"
if [ ! -f $package.zip ]; then
  echo "$package.zip does not exist.";
  exit 1;
fi


ext=$(date +"%Y%m%d%H%M")
rm -rf $package
mkdir $package
unzip $package.zip -d $package 2>&1
cp backup/settings.py $package/$package/
mv $package packages/$ext

unlink latest
ln -s packages/$ext latest
mv $package.zip backup/$package.zip$ext

./restart.sh