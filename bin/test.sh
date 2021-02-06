#!/bin/sh

echo "Waiting for server..."

while [[ ! "$(docker ps -aq -f status=running -f health=healthy -f name=wager)" ]]; do sleep 1; done

echo "Server launched"

docker exec wager python manage.py create
docker exec wager python manage.py load
docker exec wager py.test --disable-pytest-warnings -s
