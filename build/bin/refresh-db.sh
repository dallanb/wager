#!/bin/sh

docker exec -it wager bash -c "python manage.py delete"
docker exec -it wager bash -c "python manage.py create"
docker exec -it wager bash -c "python manage.py load"
