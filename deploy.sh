#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "Stopping containers before cleaning InfluxDB..."
docker compose down

echo "Deleting InfluxDB data and config..."
rm -rf ./influxdb/data
rm -rf ./influxdb/config

echo "Recreating InfluxDB folders..."
mkdir -p ./influxdb/data
mkdir -p ./influxdb/config

echo "Pulling latest Docker images..."
docker compose pull

echo "Starting updated containers..."
docker compose up -d --remove-orphans

echo "Cleaning up unused old Docker images..."
docker image prune -f

echo "Current container status:"
docker compose ps