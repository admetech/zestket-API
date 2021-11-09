#!/bin/bash

# update the env with the pipfile
VIRTUAL_ENV="venv" python3.7 -m pipenv --python="venv/bin/python3.7" install --deploy

# update the pipenv
python3.7 -m pipenv install --deploy

# update the migrations
DJANGO_ENV=production python3.7 -m pipenv run python3.7 manage.py migrate

# restart the services
sudo systemctl restart nginx gunicorn
