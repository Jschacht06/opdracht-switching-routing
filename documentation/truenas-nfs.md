# TrueNAS
We installed TrueNAS with the default settings and chose to configure everything in the web UI with the 'truenas_admin' account. At the end of the installation, we chose to shut down instead of rebooting because we then connected the PCI card with the JBODs to the VM and removed the CD drive.

We also created a new account for ourselves. It is still a full admin account, but with a less common name than the 'truenas_admin' account to be safe.

The settings for this account are:
- username: athena
- allowed access: SMB access, SSH access, and TrueNAS access is set to full admin
- allow SSH login with password is enabled
- the home directory is set to `/mnt/jbod-pool/users/athena`
- all settings that aren't mentioned are set to default

---

### JBOD passthrough
To be able to use the drives from the two JBODs that are connected to two of our nodes, we selected the server's PCI connector for passthrough to the TrueNAS VM.

Here's how to add it in Proxmox:
1. Figure out which PCI card you need to select for passthrough. We used `lspci -nn` to view the connected PCI devices. In the output, we saw that `01:00.0` and `0a:00.0` were RAID controllers. After some searching around, we found out that the card with the JBODs connected was `0a:00.0`.
2. We're using a cluster, so to add it, click on the cluster and open the Resource Mappings tab near the bottom.
3. Click on Add and select the device you want to add (`0a:00.0` in this case) from the list.
4. Give it a name. This is the name for the device. We chose 'JBOD-connections'.
5. Leave the other settings at their default values and click Create. The PCI card should now show up with your chosen name.

To give a VM access to this card, do this:
1. Select the VM you want to give access to the JBODs and go to the Hardware tab.
2. Open the Add dropdown menu and select 'PCI Device'.
3. Keep the default mapped device option and choose the device you just added.
4. Click Add and start or reboot the VM.

---

### TrueNAS pool/vdev creation
We added 12 HDDs from each JBOD to our storage pool. They are separated into 6 vdevs, all of which are mirrors containing 4 drives each.

Here's how to do it:
1. Go to the TrueNAS web UI and select the Storage tab in the navigation bar on the left.
2. Click on Create Pool.
3. Start by giving the pool a name. We named it 'JBOD-pool'. Then click Next. In the General Information menu, where you choose the name, there is also an option to encrypt all the data in that pool. We left it unchecked because we don't need it.
4. In the data menu, we chose 'mirror' for the layout option and then clicked on 'Manual Disk Selection' to configure it manually.
5. Add 6 vdevs using the button in the top right corner.
6. To make your life a bit easier, filter the disks by size. Our first filter was all 560 GB drives. Then drag 4 of them into the first vdev.
7. Do this again for the other 2 vdevs.
8. Change the disk size filter. We then chose the 1 TB drives and dragged 4 of them into each of the remaining vdevs.
9. When you're done configuring the vdevs, click on Save Selection.
10. All the other setup options are optional. We skipped most of them except for the spare step.
11. In the spare menu, we selected 3 1 TB drives as spares. You never know 🙃
12. Like we mentioned earlier, we left the rest of the options empty and went straight to the review section.
13. Click on Create Pool and the pool should now be available.

---

### Make the pool usable
By just creating the pool, you still can't use it to store data yet. First, we have to create a dataset. Then, to be able to use it from any other device, we need to add a network share to it.

Here are the steps to create a dataset:
1. In the web UI, go to the Datasets tab in the navigation bar on the left.
2. Select the pool you want to use and click on Add Dataset in the top right corner.
3. Give the dataset a name and keep the preset at 'generic'. We left all the advanced settings at their default values.

To add the network share, do this:
1. Navigate to the Shares tab in the navigation bar on the left.
2. In the 'UNIX (NFS) Shares' field, click on Add.
3. Under Path, select the path to the dataset you want to share.
4. Give the share a description. It's not required, but it can come in handy when you have multiple shares.
5. Open the advanced options and select a user and group for the 'maproot user' and 'maproot group'. These determine what rights the connection will have. If you select root, the Proxmox root user will be able to act as the TrueNAS root account on that dataset. If you select any other account, you can limit the rights through the ACL settings of the shared dataset.
6. If you want to limit who can see the share, you can add networks or even specific hosts.

**IMPORTANT: If you add networks, only devices on that network will be able to see the share, and if you add specific hosts, only those hosts will be able to see it.**

---

### Use the TrueNAS share in Proxmox
You can add the NFS share as storage in Proxmox. In our case, we use that share as storage for our other VMs.

Follow these steps to add the share:
1. In Proxmox, select the cluster and click on Storage.
2. Click on Add and select NFS.
3. Give it an ID. This will be the name for the storage, like 'local-zfs'.
4. Add the IP address of your TrueNAS server to the Server section and put the full share path into the Export box. You can copy the share path from the TrueNAS UI under Shares.
5. Select what content the share will be used for. In our case, it's the default: disk images.

If you want to use this share as a boot drive for a VM or LXC when you create a new one, you need to change the default storage space in the Disks section from 'local-zfs' to the share you just created.

If you want to add this share as external storage to a VM or LXC, follow these steps:
1. Select your VM or LXC and go to the Hardware tab.
2. Click on Add and choose Hard Disk.
3. Select the NFS share in the storage dropdown menu.

**Note: Please check if the share still has enough storage space before adding it to VMs or LXCs. If they start to use more storage than is available, you won't have a great time =)**