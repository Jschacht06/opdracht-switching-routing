#!/usr/bin/env bash
set -e

echo "Building Docker images..."
docker compose build

echo "Stopping old containers..."
docker compose down

echo "Starting updated stack..."
docker compose up -d --remove-orphans

echo "Current container status:"
docker compose ps
