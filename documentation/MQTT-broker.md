# MQTT broker
The MQTT broker is the message bus between the sensor simulator and Node-RED. The sensor simulator publishes JSON sensor values to MQTT topics, and Node-RED subscribes to those topics to process the data.

We use Eclipse Mosquitto for this. The broker runs in Docker through the `mosquitto` service in [docker-compose.yml](../docker-compose.yml).

---

### Docker setup
The service uses:
- image: `eclipse-mosquitto:2`
- container name: `mqtt-broker`
- restart policy: `unless-stopped`

The broker exposes two ports:
- `1883`: normal MQTT traffic
- `9001`: MQTT over WebSockets

The Docker Compose service mounts three local folders:
- [mqtt-broker/config](../mqtt-broker/config) to `/mosquitto/config`
- `mqtt-broker/data` to `/mosquitto/data`
- `mqtt-broker/log` to `/mosquitto/log`

The config folder is tracked in the repository. The data and log folders are used by Mosquitto at runtime.

---

### Configuration file
The Mosquitto configuration is stored in [mqtt-broker/config/mosquitto.conf](../mqtt-broker/config/mosquitto.conf).

Current configuration:

```conf
listener 1883
listener 9001
protocol websockets

persistence true
persistence_file mosquitto.db
persistence_location /mosquitto/data/

allow_anonymous true
```

---

### Listeners
The broker has two listeners.

Port `1883` is used for normal MQTT clients. This is the port used by the sensor simulator and Node-RED.

Port `9001` is configured for WebSockets. This can be useful for clients that need to connect from a browser or another environment where WebSockets are easier than a raw MQTT TCP connection.

---

### Persistence
Persistence is enabled with:

```conf
persistence true
```

Mosquitto stores its persistence database as:

```text
mosquitto.db
```

Inside the container, this file is stored in:

```text
/mosquitto/data/
```

Because [docker-compose.yml](../docker-compose.yml) mounts `mqtt-broker/data` to `/mosquitto/data`, this data survives container restarts.

---

### Anonymous access
Anonymous access is enabled:

```conf
allow_anonymous true
```

This keeps the setup simple for the lab environment. The sensor simulator and Node-RED do not need usernames or passwords to connect.

For a production setup, this should be changed. At minimum, add authentication and only allow trusted clients or trusted networks to publish and subscribe.

---

### Topics
The sensor simulator publishes to these topics:
- `/home/sensors/bathroom`
- `/home/sensors/bedroom`
- `/home/sensors/server_room`

Node-RED subscribes to the same topics in [node-red-data/flows.json](../node-red-data/flows.json).

The messages are JSON and contain:
- `temperature`
- `humidity`

More detail about the generated data is documented in [sensor-script.md](sensor-script.md).

---

### How the services use MQTT
The sensor simulator connects to:
- broker: `mosquitto`
- port: `1883`

Node-RED also connects to:
- broker: `mosquitto`
- port: `1883`

`mosquitto` is the Docker Compose service name. Containers in the same Docker network can use this name as the hostname.

From outside Docker, use:
- host: `localhost`
- port: `1883`

---

### Testing the broker
Start the stack with:

```bash
docker-compose up --build
```

Check the broker logs with:

```bash
docker logs mqtt-broker
```

You can also test the broker with an MQTT client by subscribing to one of the sensor topics:

```bash
mosquitto_sub -h localhost -p 1883 -t /home/sensors/bathroom
```

If the simulator is running, you should receive JSON messages every few seconds.

---

### Troubleshooting
If the simulator cannot connect to MQTT, check for these things:
- the `mqtt-broker` container is running
- [mqtt-broker/config/mosquitto.conf](../mqtt-broker/config/mosquitto.conf) still has listener `1883`
- the simulator still uses broker name `mosquitto`

If Node-RED does not receive messages, check this:
- the MQTT input nodes in [node-red-data/flows.json](../node-red-data/flows.json)
- the topic names match the sensor script
- the Node-RED container depends on `mosquitto` in [docker-compose.yml](../docker-compose.yml)

If an external MQTT client cannot connect, check if these things are true:
- port `1883` is mapped in [docker-compose.yml](../docker-compose.yml)
- no firewall is blocking the port
- the client is connecting to the host machine, not the Docker service name
