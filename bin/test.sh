#!/bin/sh

docker exec wager python manage.py create
docker exec wager python manage.py load
docker exec wager py.test --disable-pytest-warnings -s
