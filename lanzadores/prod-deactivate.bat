@echo off
docker-compose -f ..\docker\docker-compose.prod.yml down
docker image prune -a -f
docker volume prune -a -f