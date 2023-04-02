#!/usr/bin/env bash
echo '***************'
echo 'Clean Tests'
echo '***************'
docker-compose down

echo '***************'
echo 'Start new test session'
echo '***************'

docker-compose run web python manage.py test

echo '***************'
echo 'Stop containers after tests'
echo '***************'
docker-compose stop
