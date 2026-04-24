# Proxmox
Proxmox runs the virtual machines and connects them to the shared storage. For the TrueNAS setup, Proxmox has two important jobs:
- pass the JBOD PCI card through to the TrueNAS VM
- add the TrueNAS NFS share as storage for VM disks

The Proxmox web UIs are listed in the main [README.md](../README.md).

The TrueNAS-side setup is documented in [truenas-nfs.md](truenas-nfs.md).

---

### JBOD passthrough
To use the disks from the two JBODs, the PCI card connected to the JBODs has to be passed through to the TrueNAS VM.

We first checked the connected PCI devices from Proxmox with:

```bash
lspci -nn
```

In the output, `01:00.0` and `0a:00.0` showed up as RAID controllers. After checking the hardware, the card connected to the JBODs was `0a:00.0`.

---

### Add the PCI mapping
Because we use a Proxmox cluster, the PCI device is added as a resource mapping on cluster level.

Steps:
1. Open the Proxmox web UI.
2. Select the cluster.
3. Open the `Resource Mappings` tab.
4. Click `Add`.
5. Select the PCI device connected to the JBODs. In our setup this was `0a:00.0`.
6. Give the mapping a clear name. We used `JBOD-connections`.
7. Keep the other settings at their default values.
8. Click `Create`.

After this, the mapped PCI device should be available to assign to a VM.

---

### Attach the PCI mapping to TrueNAS
To give the TrueNAS VM access to the JBODs:
1. Select the TrueNAS VM in Proxmox.
2. Open the `Hardware` tab.
3. Open the `Add` dropdown.
4. Select `PCI Device`.
5. Keep the default mapped device option.
6. Select the `JBOD-connections` mapping.
7. Click `Add`.
8. Start or reboot the VM.

After the reboot, TrueNAS should be able to see the disks from the JBODs.

---

### Add the NFS share
The NFS share from TrueNAS can be added as storage in Proxmox. In our setup, this share is used as storage for VM disks.

The NFS share itself is created in TrueNAS. Those steps are documented in [truenas-nfs.md](truenas-nfs.md).

Steps:
1. In Proxmox, select the cluster.
2. Click `Storage`.
3. Click `Add`.
4. Select `NFS`.
5. Enter an ID for the storage.
6. Add the TrueNAS IP address in the `Server` field.
7. Add the full NFS export path in the `Export` field.
8. Select what content the storage should be used for. We use the default option, `disk images`.
9. Save the storage.

The export path can be copied from the TrueNAS UI under `Shares`.

---

### Use the share for VM storage
When creating a new VM or LXC, select the NFS storage in the disk section instead of the default local storage.

To add the share as an extra disk to an existing VM or LXC:
1. Select the VM or LXC in Proxmox.
2. Open the `Hardware` tab.
3. Click `Add`.
4. Select `Hard Disk`.
5. Choose the NFS share in the storage dropdown.
6. Configure the disk size and save it.

Before adding storage to VMs or LXCs, check that the TrueNAS pool still has enough free space.

---

### Troubleshooting
If TrueNAS cannot see the JBOD disks, check:
- the correct PCI device was mapped
- the PCI mapping is attached to the TrueNAS VM
- the TrueNAS VM was rebooted after adding the PCI device

If Proxmox cannot see the NFS export, check:
- the TrueNAS IP address is reachable from Proxmox
- the export path is copied correctly
- the NFS share is enabled in TrueNAS
- any configured networks or hosts allow the Proxmox nodes

If a VM cannot use the NFS storage, check:
- the Proxmox storage entry allows `disk images`
- the NFS share has enough free space
- the TrueNAS dataset permissions allow the mapped NFS user
