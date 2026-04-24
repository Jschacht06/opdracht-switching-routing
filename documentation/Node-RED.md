# Node-RED
Node-RED is used as the data processing layer between the MQTT broker and InfluxDB. It subscribes to the simulated sensor topics, converts the incoming values to readable units, checks if the values are outside the expected range, and writes the cleaned data to InfluxDB.

The web UI is available at:
- local development: `http://localhost:1880`
- Docker service name: `nodered`

The container is started through [docker-compose.yml](../docker-compose.yml) as the `nodered` service. It depends on both `mosquitto` and `influxdb`, because the flow needs MQTT input and an InfluxDB output.

---

### Files used by Node-RED
The Node-RED configuration lives in the [node-red-data](../node-red-data) folder.

Important files:
- [node-red-data/flows.json](../node-red-data/flows.json): contains the actual Node-RED flow.
- [node-red-data/settings.js](../node-red-data/settings.js): contains the Node-RED runtime settings.
- [node-red-data/package.json](../node-red-data/package.json): lists the extra Node-RED packages we need.
- [node-red-data/Dockerfile](../node-red-data/Dockerfile): builds our custom Node-RED image and installs the required packages.

The Dockerfile starts from the official `nodered/node-red` image and installs the dependencies from [node-red-data/package.json](../node-red-data/package.json). The most important dependency is `node-red-contrib-influxdb`, which adds the InfluxDB output nodes used in the flow.

---

### Flow overview
The flow is called `Sensor handling`.

It has three MQTT input nodes:
- `MQTT bathroom sensor`: subscribes to `/home/sensors/bathroom`
- `MQTT bedroom sensor`: subscribes to `/home/sensors/bedroom`
- `MQTT server room sensor`: subscribes to `/home/sensors/server_room`

All three inputs receive JSON data from the sensor simulator. A message looks like this before it is processed:

```json
{
  "temperature": 295.42,
  "humidity": 0.41
}
```

The temperature is sent in Kelvin and the humidity is sent as a decimal value. Node-RED converts this into degrees Celsius and a percentage.

---

### Data conversion
The `temp & humi conversion` function node converts the raw sensor values:
- temperature: Kelvin to Celsius
- humidity: decimal value to percentage

Example:
- `295.42 K` becomes `22.27 C`
- `0.41` becomes `41%`

The converted message keeps the same structure, but with readable values:

```json
{
  "temperature": 22.27,
  "humidity": 41
}
```

---

### Bad value checking
The `bad value check` function node checks if a sensor value is outside the expected range for its room. If one of the values is outside the range, Node-RED adds `error: true` to the payload.

The expected ranges are:

| Room | Temperature range | Humidity range |
| --- | --- | --- |
| Bathroom | `16.5 C` to `29.5 C` | `50%` to `85%` |
| Bedroom | `9.0 C` to `24.5 C` | `40%` to `55%` |
| Server room | `22 C` to `47 C` | `30%` to `45%` |

The simulator sometimes sends abnormal values on purpose, so this check lets us count those errors later in InfluxDB.

---

### Writing to InfluxDB
The `data formatting for InfluxDB` function prepares the message for the InfluxDB output node.

The fields written to InfluxDB are:
- `temperature`
- `humidity`
- `error_count`

The tag written to InfluxDB is:
- `room`

The room tag is taken from the MQTT topic. For example, `/home/sensors/server_room` becomes `server_room`.

The InfluxDB output node writes to:
- measurement: `sensordata`
- bucket: `${INFLUXDB_BUCKET}`
- organization: `${INFLUXDB_ORG}`
- URL: `${INFLUXDB_URL}`

These values come from the [.env](../.env) file and are passed into the Node-RED container by Docker Compose.

---

### Debug nodes
The flow contains a few debug nodes:
- `MQTT input debug`
- `conversion debug`
- `bad value debug`
- `data formatting debug`

They are disabled by default. You can enable them in the Node-RED editor when you want to inspect the data at a specific point in the flow.

This is useful when:
- MQTT messages are not arriving.
- The conversion looks wrong.
- The error count is higher than expected.
- InfluxDB is not receiving data.

---

### Deploying changes
If you change the flow in the Node-RED web UI, click `Deploy` in the top right corner. The flow is stored in [node-red-data/flows.json](../node-red-data/flows.json), because the [node-red-data](../node-red-data) folder is mounted into the container as `/data`.

If you change dependencies in [node-red-data/package.json](../node-red-data/package.json), rebuild the container:

```bash
docker-compose up --build
```

---

### Troubleshooting
If Node-RED does not receive MQTT data, check if the MQTT broker is running and if the broker host is still set to `mosquitto`. This is the Docker Compose service name and works inside the Docker network.

If Node-RED receives MQTT data but InfluxDB stays empty, check for these things:
- the InfluxDB container is healthy
- the [.env](../.env) file contains the correct `INFLUXDB_ORG`, `INFLUXDB_BUCKET`, `INFLUXDB_ADMIN_TOKEN`, and `INFLUXDB_URL`
- `INFLUXDB_URL` is set to `http://influxdb:8086` when running through Docker Compose
- the InfluxDB output node is still using measurement `sensordata`
