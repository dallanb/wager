#!/bin/sh

echo "Waiting for server..."

while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' 0.0.0.0:80/ping)" != "200" ]]; do sleep 1; done

echo "Server launched"

#docker exec wager python manage.py create
#docker exec wager python manage.py load
#docker exec wager py.test --disable-pytest-warnings -s
