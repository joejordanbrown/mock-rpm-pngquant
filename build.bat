@echo off

REM Build CentOS 7

SET CUREENT_DIR=%~dp0

REM Build docker image
docker build -t local/centos-7_mock-rpm:latest -f "%CUREENT_DIR%/Dockerfile" .

REM Create folders
mkdir data
mkdir result
mkdir scripts

REM Run docker
REM docker run --cap-add=SYS_ADMIN -i -v "%CUREENT_DIR%/scripts:/root/scripts" -v "%CUREENT_DIR%/data:/root/data" -v "%CUREENT_DIR%/result:/root/result" -t local/centos-7_mock-rpm:latest /bin/bash
docker run --cap-add=SYS_ADMIN -i -v "%CUREENT_DIR%/scripts:/root/scripts" -v "%CUREENT_DIR%/data:/root/data" -v "%CUREENT_DIR%/result:/root/result" -t local/centos-7_mock-rpm:latest /root/scripts/mock-build.sh