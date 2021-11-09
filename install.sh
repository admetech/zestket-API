#!/bin/bash

# copy the setting file manually and edit it before running this script
echo "Make sure the setting file exist befor running this script"

# update the OS
apt update

# # install nginx
# sudo apt install -y nginx

# install pip3
apt install -y python3-pip libpq-dev python-apt

# GDAL binary and Python binding are available through ubuntugis repository
# add-apt-repository ppa:ubuntugis/ubuntugis-unstable -y
apt install -y gdal-bin python3-gdal

# install virtualenv
pip3 install virtualenv pipenv

# create the virtualenv
virtualenv venv

# install python3.9
apt install -y python3.9-minimal

# # install pipenv in virtual env
# VIRTUAL_ENV="venv" python3.9 -m pip install pipenv

# # update the env with the pipfile
# VIRTUAL_ENV="venv" python3.9 -m pipenv --python="venv/bin/python3.9" install --deploy

# update the pipenv
python3.9 -m pipenv install --deploy

# update the migrations
# DJANGO_ENV=production python3.9 -m pipenv run python3.9 manage.py migrate

# update the static files
# DJANGO_ENV=production python3.9 -m pipenv run python3.9 manage.py collectstatic

# to test the latest updates are working or not
# DJANGO_ENV=production python3.9 -m pipenv run python3.9 manage.py runserver

# to test gunicon is working
# DJANGO_ENV=production python3.9 -m pipenv run gunicorn --bind 0.0.0.0:8000 website.wsgis

# copy the gunicorn.socket
sudo cp config/mktyz_gunicorn.socket /etc/systemd/system/mktyz_gunicorn.socket

# copy the gunicorn.service
sudo cp config/mktyz_gunicorn.service /etc/systemd/system/mktyz_gunicorn.service

# start gunicorn service
sudo systemctl start mktyz_gunicorn.socket
sudo systemctl enable mktyz_gunicorn.socket

# reload the socket
sudo systemctl daemon-reload

# activate the socket
curl --unix-socket /run/mktyz_gunicorn.sock localhost

# copy the ngnix config 
sudo cp config/nginx_site.config /etc/nginx/sites-available/mktyz_api

# activate the site
sudo ln -s /etc/nginx/sites-available/mktyz_api /etc/nginx/sites-enabled

# # update the firewall
# sudo ufw allow 'Nginx Full'

# restart the services
sudo systemctl restart nginx mktyz_gunicorn.service mktyz_gunicorn.socket

# locations
# Gunicorn Service  : /etc/systemd/system/mktyz_gunicorn.service
# Gunicorn Socket   : /etc/systemd/system/mktyz_gunicorn.socket
# Webiste Socket (connecting Django and Ngnix)  : /run/mktyz_gunicorn.sock
# Ngnix Config      : /etc/nginx/sites-available/resource   

# # install certboot to get the SSL certificate
# sudo apt install -y software-properties-common
# sudo add-apt-repository universe -y
# sudo add-apt-repository ppa:certbot/certbot -y
# sudo apt update
# sudo apt install -y certbot python3-certbot-nginx

# # get ssl certificate
# sudo certbot --nginx
