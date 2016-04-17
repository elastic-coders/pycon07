# Pycon7 blog app

Lets you:

- make friends
- post status to your profile page
- see all your friends posts on your feed


# Setup

Write a simple django app+DRF implementing the main stories.

How fast does it run?

Incomplete list of commands run:

    cd src/
    pyenv local 3.4.4
    python -m venv virtual
    source virtual/bin/activate
    pip install django djangorestframework
    django-admin startproject pycon7 .
    python manage.py startapp blog
    # add app to INSTALLED_APPS
    python manage.py makemigrations
    python manage.py createsuperuser
    python manage.py runserver


# Run it with uwsgi

    uwsgi --module pycon7.wsgi --http :8000 -p 5

Scaling up uwsgi


# Fanout on write

with Celery workers

How can we run periodic (scheduled) tasks?

Scaling up wokers


# Elasticsearch
