# Sensor simulation script
The sensor simulation script creates fake sensor data for three rooms and publishes it to the MQTT broker. This gives us a steady stream of data for testing Node-RED, InfluxDB, and the dashboards without needing physical sensors.

The script is located at [sensors/sensors.py](../sensors/sensors.py).

It runs in the `sensors-simulator` container, which is built from [sensors/Dockerfile](../sensors/Dockerfile).

---

### Docker setup
The `sensors` service is defined in [docker-compose.yml](../docker-compose.yml).

It:
- builds from the `sensors` folder
- uses the container name `sensors-simulator`
- restarts automatically unless stopped
- depends on the `mosquitto` service

The Docker image uses `python:3.11-slim`, installs the dependencies from [sensors/requirements.txt](../sensors/requirements.txt), copies [sensors/sensors.py](../sensors/sensors.py), and starts the script with:

```bash
python sensors.py
```

The only Python dependency is:

```text
paho-mqtt==1.6.1
```

---

### MQTT connection
The script connects to the MQTT broker with these settings:

```python
BROKER = "mosquitto"
PORT = 1883
```

`mosquitto` is the Docker Compose service name for the MQTT broker. Because all containers are on the same Docker network, the script can connect to the broker with that name.

The script publishes to three topics:
- `/home/sensors/bathroom`
- `/home/sensors/bedroom`
- `/home/sensors/server_room`

Node-RED subscribes to these same topics.

---

### Message format
Every MQTT message is JSON.

Example:

```json
{
  "temperature": 294.53,
  "humidity": 0.48
}
```

The script sends:
- `temperature` in Kelvin
- `humidity` as a decimal value

Node-RED converts these values later:
- Kelvin to Celsius
- decimal humidity to percentage

---

### Generated values
The script generates values for each room every 5 seconds.

Normal value ranges:

| Room | Temperature range | Humidity range |
| --- | --- | --- |
| Bathroom | `290.00 K` to `302.50 K` | `0.50` to `0.85` |
| Bedroom | `282.50 K` to `297.50 K` | `0.40` to `0.55` |
| Server room | `295.50 K` to `320.00 K` | `0.30` to `0.45` |

After generating the normal values, the script can replace them with abnormal values. This happens through the `error()` function.

---

### Error simulation
The `error()` function gives each value a 5% chance to become abnormal.

```python
def error(value, bad_min, bad_max, chance=0.05):
    if random.random() < chance:
        return round(random.uniform(bad_min, bad_max), 2)
    return value
```

This is intentional. It allows Node-RED and InfluxDB to test error detection and error dashboards.

Abnormal value ranges:

| Room | Temperature error range | Humidity error range |
| --- | --- | --- |
| Bathroom | `235.00 K` to `255.00 K` | `1.10` to `1.50` |
| Bedroom | `330.00 K` to `380.00 K` | `0.95` to `1.15` |
| Server room | `350.00 K` to `380.00 K` | `0.95` to `1.15` |

Node-RED checks these values after conversion and writes `error_count` to InfluxDB.

---

### Timing
The script runs forever in a `while True` loop.

At the end of every loop it waits 5 seconds:

```python
time.sleep(5)
```

This means each room gets a new MQTT message about every 5 seconds.

---

### Testing the script
Start the full stack with:

```bash
docker-compose up --build
```

To check if the simulator is running:

```bash
docker logs sensors-simulator
```

The script does not print messages by default, so an empty log does not always mean it is broken. To verify the data, use the Node-RED debug sidebar or subscribe to the MQTT topics with any MQTT client.

You can also check if Node-RED and InfluxDB are receiving data:
- Node-RED: open `http://localhost:1880`
- InfluxDB: open `http://localhost:8086`

---

### Changing the simulated data
To add another room:
1. Add a new MQTT topic constant in [sensors/sensors.py](../sensors/sensors.py).
2. Add value generation for that room inside the loop.
3. Publish a JSON message to the new topic.
4. Add a matching MQTT input node in Node-RED.
5. Add error checks and InfluxDB dashboard queries for the new room.

To change how often data is sent, change the value in `time.sleep(5)`.

To change how often abnormal values are created, change the `chance` value in the `error()` function call.

---

### Troubleshooting
If the simulator cannot connect to MQTT, check for these things:
- the `mosquitto` container is running
- the broker name is still `mosquitto`
- port `1883` is enabled in the MQTT broker configuration

If Node-RED receives no messages, check:
- the topic names in [sensors/sensors.py](../sensors/sensors.py)
- the topic names in the Node-RED MQTT input nodes
- the `sensors-simulator` container is running

If too many errors appear in InfluxDB, check the abnormal ranges and the `chance` argument used by the `error()` function.
