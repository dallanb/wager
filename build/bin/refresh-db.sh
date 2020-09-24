#!/bin/sh

docker exec -it wager bash -c "python manage.py reset_db"
docker exec -it wager bash -c "python manage.py init"