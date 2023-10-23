@echo off
docker-compose -f ..\docker\prod\docker-compose.prod.yml up -d --build
