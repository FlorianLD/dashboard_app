@echo off
REM Build and start containers
docker compose up --build

REM Stop containers after they exit
docker compose down