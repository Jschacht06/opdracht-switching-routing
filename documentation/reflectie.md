# Reflectie

## Arthur
Ik vond dit een zeer leuk project om alle onderwerpen van tijdens de lessen toe te passen in de praktijk. Wat ik het meest interessant vond van de originele opdracht was de flow van de MQTT-sensors naar Node-Red en InfluxDB. Deze tools waren nieuw voor mij, maar ik vond het interessant om te zien hoe ze gebruikt kunnen worden om data te verwerken, op te slaan en overzichtelijk weer te geven. Vooral de combinatie van gesimuleerde sensordata, flows in Node-RED en opslag in InfluxDB maakte duidelijk hoe zulke tools in een praktische monitoring-omgeving kunnen worden ingezet. Ik vond het ook nuttig om te leren hoe belangrijk correcte dataverwerking is, zodat er geen foutieve of onbruikbare data in de database terechtkomt.

Daarnaast heb ik ook veel bijgeleerd over Proxmox. Ik had al interesse in virtualisatie, maar door dit project heb ik een beter inzicht gekregen in hoe je virtuele machines, resources, migratie en replicatie in een clusteromgeving kunt gebruiken. Het werken met de JBODs en een TrueNAS VM binnen Proxmox vond ik een leuke extra voor het het project, omdat opslag en virtualisatie zo op een realistische manier gecombineerd werden. Het maakte het project complexer, maar ook interessanter en leuker.

Wat ik vooral meeneem uit dit project, is dat het opzetten van een infrastructuur niet alleen draait om losse onderdelen laten werken, maar vooral om de samenhang tussen die onderdelen. Over het algemeen vond ik dit een leerrijk project waarin ik mijn bestaande kennis verder heb kunnen uitbouwen. Vooral de combinatie van Proxmox, TrueNAS, Docker, Node-RED en InfluxDB maakte het interessant, omdat het project daardoor dichter aanleunde bij een echte infrastructuuromgeving.

## Juha
Dit was een leuk project, door dit te maken heb ik over alle onderdelen veel meer bijgeleerd. Ik heb het meest bijgeleerd op vlak van CI-CD want hier wist ik niks vanaf op voorhand. Ik ben ook enorm blij dat ik nu een basis heb van hoe dit werkt want ik zal dit later ook vaak toepassen op mijn projecten.

De extra opdracht heeft me ook veel bijgeleerd over proxmox/truenas op een iets grotere schaal dan gewoon een thuisinstallatie.


## Takenverdeling
### Arthur:
- Docker compose
- Node-Red setup volledig (+ flow automatisch importeren)
- InfluxDB setup volledig (+ dashboards automatisch importeren)
- Sensor script uitbreiding / extra sensoren

- JBOD passthrough in Proxmox (met hulp van Juha)
- TrueNAS VM setup
- NFS-share opgezet en toegevoegd aan Proxmox

- Documentatie (Docker compose, Influxdb, JBOD, MQTT-broker, Node-Red, Proxmox, snesor script, TrueNAS en NFS)

### Juha:
- Docker compose
- Basis sensor script (mqtt connectie en 1 sensor)
- Dockerfile voor sensor script
- MQTT-broker setup volledig
- Portainer setup volledig
- CICD volledig

- Proxmox setup
- Debian LXC die werkt met CICD (self hosted runner en workflow die automatisch pulled en rebuild)

- Documentatie (CICD)