#!/bin/sh

. ~/.bashrc
python manage.py delete
python manage.py create
python manage.py load
python -m py.test --disable-pytest-warnings -s
