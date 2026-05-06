#!/usr/bin/env bash
set -e

echo "Pulling latest Docker images..."
docker compose pull

echo "Starting updated containers..."
docker compose up -d --remove-orphans

echo "Cleaning up unused old Docker images..."
docker image prune -f

echo "Current container status:"
docker compose ps