#!/bin/sh
# For use by jenkins test step
echo "Waiting for server..."

while [[ ! "$(docker ps -aq -f status=running -f health=healthy -f name=wager)" ]]; do sleep 1; done

echo "Server ready"

docker exec wager py.test --disable-pytest-warnings -s --junitxml tests.xml --cov-report xml --cov-report term --cov-branch --cov=src
