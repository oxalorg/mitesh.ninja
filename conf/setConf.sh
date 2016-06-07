#!/usr/bin/env sh

basedir=`pwd`
nginxdir=/etc/nginx/sites-available
vassaldir=/etc/uwsgi/vassals

sudo cp -iv $basedir/mitesh.ninja.conf $nginxdir/mitesh.ninja.conf
sudo cp -iv $basedir/mitesh.ninja.uwsgi.ini $vassaldir/mitesh.ninja.uwsgi.ini

# restart the uwsgi vassal process
sudo touch $vassaldir/mitesh.ninja.uwsgi.ini || echo "uwsgi touch failed."

# check nginx config and restart
sudo nginx -t && echo "Now RUN: sudo service nginx restart" || echo "nginx config error"
