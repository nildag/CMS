@echo off
docker-compose -f ..\docker\docker-compose.prod.yml up -d --build
