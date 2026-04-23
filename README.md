# TO DO
- Influxdb dashboard/graph for node red data
- CI/CD
- TrueNAS backup VM in case the main VM doesn't work
- documentation on debian vm setup
- documentation on node-red setup
- documentation on sensor script
- documentation on influxdb
- documentation on mqtt broker

# opdracht-switching-routing

Command to start everything: ``docker-compose up --build``


## web-ui

- zues: ``10.10.40.101:8006``
- artemis: ``10.10.40.102:8006``
- luc: ``10.10.40.103:8006``
- truenas: ``10.10.40.104``

* node-red: ``localhost:1880``
* influxdb: ``localhost:8086``


## idea

both artemis and luc are connected to the two jbods, artemis runs the truenas vm by default. the jbods are passed through to truenas via the pci adapter on artemis. when artemis goes down luc takes over the vm and runs it on it's own, with the pci connection with the jbods.

there's only one vm, stored in local-zfs, which will be replicated from artemis to luc every minute.