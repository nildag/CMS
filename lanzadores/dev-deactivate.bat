@echo off
docker-compose -f ..\docker\dev\docker-compose.dev.yml down
docker image prune -a -f
docker volume prune -a -f