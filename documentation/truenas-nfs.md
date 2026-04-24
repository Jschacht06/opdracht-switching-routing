# TrueNAS and NFS
TrueNAS is used as shared storage for the Proxmox environment. It creates a storage pool from the JBOD disks and exposes that storage to Proxmox through NFS.

The TrueNAS web UI is available at:
- TrueNAS: `10.10.40.104`

The Proxmox-side setup is documented in [proxmox.md](proxmox.md).

---

### Installation
TrueNAS was installed with the default settings. During installation we used the default `truenas_admin` account to finish the first configuration in the web UI.

At the end of the installation, we shut down the VM instead of rebooting it. This gave us time to let Proxmox attach the PCI card with the JBODs before starting TrueNAS again.

The PCI passthrough steps are documented in [proxmox.md](proxmox.md).

---

### Admin account
We also created our own admin account. This account still has full admin rights, but uses a less common username than `truenas_admin`.

Account settings:
- username: `athena`
- access: SMB access, SSH access, and full TrueNAS admin access
- password login over SSH: enabled
- home directory: `/mnt/jbod-pool/users/athena`
- all other settings: default

---

### Storage pool
We created one TrueNAS storage pool from the JBOD disks.

Pool layout:
- pool name: `JBOD-pool`
- disks used: 12 HDDs from each JBOD
- vdev count: 6
- vdev layout: mirrors
- drives per mirror vdev: 4
- spare drives: 3 drives of 1 TB

We did not enable encryption because we don't need it for this test setup. Feel free to enable it for your own setup if you'd like.

---

### Create the pool
Steps:
1. Open the TrueNAS web UI.
2. Go to `Storage`.
3. Click `Create Pool`.
4. Enter the pool name. We used `JBOD-pool`.
5. Leave encryption disabled. (personal choice)
6. In the data menu, choose `mirror` as the layout.
7. Click `Manual Disk Selection`.
8. Add 6 vdevs with the button in the top right corner.
9. Filter by disk size to make disk selection easier.
10. Add four 560 GB drives to each of the first three vdevs.
11. Change the disk size filter.
12. Add four 1 TB drives to each of the remaining three vdevs.
13. Click `Save Selection`.
14. In the spare menu, select three 1 TB drives as spares.
15. Continue to the review section.
16. Click `Create Pool`.

After this, the pool should be visible in TrueNAS.

---

### Dataset
A pool alone is not enough to expose storage to other systems. We first created a dataset on the pool.

Steps:
1. Go to `Datasets`.
2. Select the pool.
3. Click `Add Dataset`.
4. Enter a dataset name.
5. Keep the preset set to `generic`.
6. Leave the advanced settings at their default values.
7. Save the dataset.

---

### NFS share
The dataset is shared with Proxmox through NFS.

Steps:
1. Go to `Shares`.
2. In the `UNIX (NFS) Shares` section, click `Add`.
3. Under `Path`, select the dataset path.
4. Add a description for the share.
5. Open the advanced options.
6. Select a `maproot user` and `maproot group`.
7. Optionally add networks or hosts if the share should be limited to specific clients.
8. Save the share.

The `maproot user` and `maproot group` decide which TrueNAS account the Proxmox root user maps to when it accesses the share. If you select `root`, Proxmox can act as the TrueNAS root account on that dataset. If you select another account, access can be limited through the dataset ACL settings.

**Important:** If you add networks or hosts to the NFS share, only those clients will be able to access it.

After creating the NFS share, add it as Proxmox storage by following [proxmox.md](proxmox.md).

---

### Troubleshooting
If TrueNAS cannot see the JBOD disks, check:
- the PCI mapping is attached to the TrueNAS VM in Proxmox
- the TrueNAS VM was rebooted after adding the PCI device
- the correct PCI device was mapped in Proxmox

If Proxmox cannot see the NFS export, check:
- the NFS share is enabled in TrueNAS
- the TrueNAS IP address is reachable from Proxmox
- the export path is copied correctly
- any configured networks or hosts allow the Proxmox nodes

If a VM cannot use the NFS storage, check:
- the NFS share has enough free space
- the `maproot user` and `maproot group` have enough permissions on the dataset
- the Proxmox storage setup in [proxmox.md](proxmox.md)
