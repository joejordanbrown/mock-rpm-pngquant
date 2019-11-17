#! /usr/bin/sh

# Build CentOS 7

CUREENT_DIR="$(dirname $(readlink -f $0))"

# Build docker image
docker build -t local/centos-7_mock-rpm:latest -f "${CUREENT_DIR}/Dockerfile" .

# Create folders
mkdir data
mkdir result
mkdir scripts

# Run docker
# docker run --cap-add=SYS_ADMIN -i -v "${CUREENT_DIR}/scripts:/root/scripts" -v "${CUREENT_DIR}/data:/root/data" "${CUREENT_DIR}/result:/root/result -t local/centos-7_mock-rpm:latest /bin/bash
docker run --cap-add=SYS_ADMIN -i -v "${CUREENT_DIR}/scripts:/root/scripts" -v "${CUREENT_DIR}/data:/root/data" -v "${CUREENT_DIR}/result:/root/result" -t local/centos-7_mock-rpm:latest /root/scripts/mock-build.sh

