# JBOD connections
The JBODs are connected to the Proxmox servers with SFF-8088 cables. Each Proxmox server needs a PCI card with two external SFF-8088 ports so it can connect to both JBODs.

The Proxmox PCI passthrough and resource mapping setup is documented in [proxmox.md](proxmox.md).

---

### Physical cabling
Each JBOD has four external SFF-8088 ports. For this setup, each server gets one cable to each JBOD.

Steps:
1. Plug one SFF-8088 cable into one of the four ports on the first JBOD.
2. Plug the other end of that cable into one of the SFF-8088 ports on the first server.
3. Plug a second SFF-8088 cable into one of the four ports on the second JBOD.
4. Plug the other end of that cable into the second SFF-8088 port on the same server.
5. Repeat the same cabling for the second server:
   - one cable from the second server to the first JBOD
   - one cable from the second server to the second JBOD

After cabling, both Proxmox servers should have a direct connection to both JBODs.

---

### Expected layout
In our setup:
- the first server has one SFF-8088 cable to each JBOD
- the second server has one SFF-8088 cable to each JBOD
- both JBODs are available through the PCI card on each server

This makes it possible to create one Proxmox Datacenter resource mapping name, for example `JBOD-connections`, with a separate PCI device entry for each node.

---

### Checks
The JBOD-connected PCI card should show up as a storage or RAID controller. Use the correct PCI device address when creating the Proxmox resource mapping.
