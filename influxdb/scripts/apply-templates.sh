#!/bin/sh
set -e

until influx ping --host http://influxdb:8086 >/dev/null 2>&1; do
  sleep 2
done

influx apply \
  --host http://influxdb:8086 \
  --org "$INFLUXDB_ORG" \
  --token "$INFLUXDB_ADMIN_TOKEN" \
  --force yes \
  --file /templates