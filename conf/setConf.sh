#!/usr/bin/env sh

basedir=`pwd`
nginxdir=/etc/nginx/sites-available
vassalsdir=/etc/uwsgi/vassals

sudo cp -v $basedir/mitesh.ninja.conf $nginxdir/mitesh.ninja.conf
sudo cp -v $basedir/mitesh.ninja.uwsgi.ini $vassaldir/mitesh.ninja.uwsgi.conf

# restart the uwsgi vassal process
sudo touch $vassaldir/mitesh.ninja.uwsgi.conf

# check nginx config and restart
sudo nginx -t && sudo service nginx restart || echo "nginx config error"
