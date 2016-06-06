#!/usr/bin/venv sh
ssh -t mitu@server1.mitesh.ninja "cd /var/www/mitesh.ninja/public/ && git pull github master || echo 'Something went wrong'"
