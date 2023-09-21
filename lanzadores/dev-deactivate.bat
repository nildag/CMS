@echo off
docker-compose -f ..\docker\docker-compose.dev.yml down
docker image prune -a -f
docker volume prune -a -f