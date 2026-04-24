# InfluxDB
InfluxDB is used to store the processed sensor data that comes from Node-RED. It keeps the temperature, humidity, and error count values so they can be queried and shown on dashboards.

The web UI is available at:
- local development: `http://localhost:8086`
- Docker service name: `influxdb`

The container is started through [docker-compose.yml](../docker-compose.yml) as the `influxdb` service. It uses the official `influxdb:2.7` image.

---

### Environment variables
InfluxDB is initialized with values from the [.env](../.env) file.

Required variables:
- `INFLUXDB_ADMIN_USERNAME`
- `INFLUXDB_ADMIN_PASSWORD`
- `INFLUXDB_ORG`
- `INFLUXDB_BUCKET`
- `INFLUXDB_ADMIN_TOKEN`
- `INFLUXDB_URL`

An example can be found in [.env.example](../.env.example).

For Docker Compose, `INFLUXDB_URL` should be:

```text
http://influxdb:8086
```

This is the internal Docker network address. From your browser, use `http://localhost:8086` instead.

---

### Persistent storage
The InfluxDB service mounts two local folders:
- `./influxdb/data` to `/var/lib/influxdb2`
- `./influxdb/config` to `/etc/influxdb2`

This means the database data and configuration stay available after the container is restarted.

If these folders are deleted, InfluxDB will be initialized again on the next startup.

---

### Bucket and measurement
Node-RED writes all sensor data to the bucket configured in `INFLUXDB_BUCKET`.

The measurement name is:

```text
sensordata
```

The fields are:
- `temperature`
- `humidity`
- `error_count`

The tag is:
- `room`

Current room tag values:
- `bathroom`
- `bedroom`
- `server_room`

This structure makes it easy to query data for one room or compare rooms in the same dashboard.

---

### Dashboards
The dashboards are stored as InfluxDB templates in [influxdb/templates](../influxdb/templates).

Current templates:
- [influxdb/templates/bathroom_sensors.json](../influxdb/templates/bathroom_sensors.json): dashboard for bathroom temperature and humidity.
- [influxdb/templates/bedroom_sensors.json](../influxdb/templates/bedroom_sensors.json): dashboard for bedroom temperature and humidity.
- [influxdb/templates/server-room_sensors.json](../influxdb/templates/server-room_sensors.json): dashboard for server room temperature and humidity.
- [influxdb/templates/errors.json](../influxdb/templates/errors.json): dashboard for sensor error counts.

The room dashboards show:
- live temperature for the last 15 minutes
- live humidity for the last 15 minutes
- temperature average over 1 hour
- humidity average over 1 hour
- temperature average over 24 hours
- humidity average over 24 hours

The error dashboard shows the amount of bad values in the last hour for each room.

---

### Template importer
The `influxdb-template-importer` service applies the dashboard templates automatically.

It uses:
- image: `influxdb:2.7`
- script: [influxdb/scripts/apply-templates.sh](../influxdb/scripts/apply-templates.sh)
- templates folder: [influxdb/templates](../influxdb/templates)

The script waits until InfluxDB responds to `influx ping`, then runs:

```bash
influx apply --host http://influxdb:8086 --org "$INFLUXDB_ORG" --token "$INFLUXDB_ADMIN_TOKEN" --force yes --file /templates
```

The importer has `restart: "no"`, so it runs once and then stops. This is expected.

---

### Example queries
Live bathroom temperature:

```flux
from(bucket: "sensordata")
  |> range(start: -15m)
  |> filter(fn: (r) => r._measurement == "sensordata")
  |> filter(fn: (r) => r._field == "temperature")
  |> filter(fn: (r) => r.room == "bathroom")
```

Server room humidity average over the last hour:

```flux
from(bucket: "sensordata")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "sensordata")
  |> filter(fn: (r) => r._field == "humidity")
  |> filter(fn: (r) => r.room == "server_room")
  |> mean()
```

Bedroom error count over the 24 hours:

```flux
from(bucket: "sensordata")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "sensordata")
  |> filter(fn: (r) => r._field == "error_count")
  |> filter(fn: (r) => r.room == "bedroom")
  |> sum()
```

Replace `sensordata` with your own bucket name if `INFLUXDB_BUCKET` uses a different value.

---

### Troubleshooting
If InfluxDB does not start, check if all required values are present in [.env](../.env).

If the dashboards are missing, check the logs of the template importer:

```bash
docker logs influxdb-template-importer
```

If Node-RED cannot write data, check:
- the InfluxDB container is healthy
- the admin token in [.env](../.env) is correct
- the bucket and organization match the values used by Node-RED
- `INFLUXDB_URL` is reachable from inside Docker as `http://influxdb:8086`
