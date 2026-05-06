#!/bin/sh
set -e

host="http://influxdb:8086"

until influx ping --host "$host" >/dev/null 2>&1; do
  echo "Waiting for InfluxDB to respond..."
  sleep 2
done

attempt=1
max_attempts=30

until influx apply \
    --host "$host" \
    --org "$INFLUXDB_ORG" \
    --token "$INFLUXDB_ADMIN_TOKEN" \
    --force yes \
    --file /templates; do
  if [ "$attempt" -ge "$max_attempts" ]; then
    echo "Failed to apply InfluxDB templates after $attempt attempts."
    exit 1
  fi

  echo "InfluxDB template apply failed on attempt $attempt. Retrying..."
  attempt=$((attempt + 1))
  sleep 2
done
