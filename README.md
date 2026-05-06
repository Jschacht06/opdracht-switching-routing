# Opdracht Switching & Routing

This repository contains the Docker stack and documentation for the switching and routing assignment environment. The project combines a small monitoring stack with Proxmox, TrueNAS, JBOD storage, and deployment documentation.

The application side runs with Docker Compose:

- Mosquitto MQTT broker
- sensor simulator
- Node-RED flows
- InfluxDB dashboards and storage
- Portainer

The infrastructure side documents the Proxmox nodes, the TrueNAS VM, NFS storage, and the physical JBOD cabling.

## Quick Start

Start or rebuild the Docker stack manually:

```bash
docker compose up --build
```

Deploy the full stack with the deployment script:

```bash
./deploy.sh
```

The Docker Compose stack is documented in [documentation/docker-compose.md](documentation/docker-compose.md).

## Services

| Service | URL | Notes |
| --- | --- | --- |
| Node-RED | `http://localhost:1880` or `http://<server-ip>:1880` | Flow editor and MQTT processing |
| InfluxDB | `http://localhost:8086` or `http://<server-ip>:8086` | Time-series database and dashboards |
| Portainer | `https://localhost:9443` or `https://<server-ip>:9443` | Docker management UI |
| MQTT | `<server-ip>:1883` | Mosquitto broker |

When Docker runs inside a VM, replace `localhost` with the VM IP address.

## Infrastructure

| Host | Address | Role |
| --- | --- | --- |
| Zeus | `10.10.40.101:8006` | Proxmox node, mini PC that runs the standard project |
| Artemis | `10.10.40.102:8006` | Proxmox node that currently hosts the TrueNAS VM |
| Luc | `10.10.40.103:8006` | Proxmox node that was intended as the TrueNAS backup/failover node |
| TrueNAS | `10.10.40.104` | Storage manager |

## Current Reality

The original plan was to make the TrueNAS VM movable between Artemis and Luc. Artemis would normally run the VM, while Luc would be able to take over during maintenance or failure. Both nodes would have a PCI connection to the JBODs, and the TrueNAS VM disk would be replicated from Artemis to Luc.

That is not the current state of the rack.

The TrueNAS VM exists on Artemis and currently cannot be moved safely. Luc was taken out of the rack because of a hardware fault, so it is no longer available as a backup node for Artemis. Zeus is still present, but it is a mini PC and cannot connect to the JBOD hardware. Because of that, Zeus cannot replace Luc for the TrueNAS failover role.

The practical result is:

- Artemis is the only active node that can run the TrueNAS VM with the JBODs attached.
- There is currently no working backup/failover node for the Artemis TrueNAS setup.
- The intended Artemis-to-Luc VM failover design should be treated as documentation of the goal, not as the active production state.
- Any maintenance on Artemis or the JBOD path has to be planned carefully, because storage availability depends on that node.

## Intended Storage Design

The intended design was:

1. Artemis and Luc are both connected to the two JBODs.
2. Artemis runs the TrueNAS VM by default.
3. The JBODs are passed through to TrueNAS through the PCI adapter on Artemis.
4. If Artemis goes down, Luc starts the same TrueNAS VM with its own PCI connection to the JBODs.
5. The VM disk is stored on `local-zfs` and replicated from Artemis to Luc every minute.

This design requires Luc to be physically present, healthy, and connected to the JBODs. Without Luc, the design is not operational.

## Documentation

| Topic | File |
| --- | --- |
| Docker Compose stack | [documentation/docker-compose.md](documentation/docker-compose.md) |
| CI/CD deployment | [documentation/CICD.md](documentation/CICD.md) |
| Proxmox setup | [documentation/proxmox.md](documentation/proxmox.md) |
| TrueNAS NFS setup | [documentation/truenas-nfs.md](documentation/truenas-nfs.md) |
| JBOD cabling | [documentation/jbod.md](documentation/jbod.md) |
| MQTT broker | [documentation/MQTT-broker.md](documentation/MQTT-broker.md) |
| Node-RED | [documentation/Node-RED.md](documentation/Node-RED.md) |
| InfluxDB | [documentation/InfluxDB.md](documentation/InfluxDB.md) |
| Sensor script | [documentation/sensor-script.md](documentation/sensor-script.md) |

## Useful Commands

Start the stack:

```bash
docker compose up -d
```

Start the stack and rebuild images:

```bash
docker compose up --build
```

View logs:

```bash
docker compose logs -f
```

Stop the stack:

```bash
docker compose down
```

Redeploy:

```bash
./deploy.sh
```

## Open Work

- Document the Debian VM setup.
- Revisit the TrueNAS migration/failover plan after Luc is repaired or replaced with hardware that can connect to the JBODs.
