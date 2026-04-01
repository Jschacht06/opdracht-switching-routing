# TrueNAS
We installed TrueNAS with the default settings and chose to configure everything in the web-ui with the truenas_admin account. At the end of the installation we chose to shut down instead of reboot, because we then connected the PCI-card with the JBODs to the VM and removed the CD-drive.

We also created a new account for ourselves, it's still a full admin account but with a less common name than the truenas_admin account to be safe. 

The settings for this account are:
- username: athena
- allow access: SMB access, SSH acces and TrueNAS acces is set to full admin
- allow SSH login with password is enabled
- the home directory is set to /mnt/jbod-pool/users/athena
- all settings that aren't mentioned are set to default

---

### JBOD passthrough
To be able to use the drives from the two JBODs that are connected to two of our nodes we just selected the server's PCI-connector for passthrough to the TrueNAS VM.

Here's how to do add it to proxmox:
1. Figure out which PCI card you need to select for passthrough. We used ``lspci -nn`` to view the connected PCI devices, in the output we saw that 01:00.0 and 0a:00.0 were RAID-controllers. After some searching around we found out that our card with the JBODs connected is the 0a:00.0.
2. We're using a cluster so to add it you click on the datacenter and open the resource mappings tab (near the bottom).
3. Click on add and select the device you want to add (0a:00.0 in this case) from the list.
4. Give it a name, this is the name for the device (we chose 'JBOD-connections').
5. Leave the other settings on default and click create, now the PCI card should show up with your chosen name.

To give a VM access to this card do this:
1. Select the VM you want to give access to the JBODs and go to the hardware tab.
2. Open the add dropdown menu and select 'PCI Device'.
3. Keep the default mapped device option and choose the device you just added.
4. Click on add and start/reboot the VM.

---

### TrueNAS pool/vdev creation
We added 12 HDDs from each JBOD to our storage pool, they're separated in 6 vdevs that are all mirrors, containing 4 drives each.

Here's how to do it:
1. Go to the TrueNAS web ui and select the 'storage' tab in the navigation bar on the left.
2. Click on 'create pool'.
3. Start of by giving the pool a name (we named it "JBOD-pool") and click on next. In the 'general information' menu where you chose the name there's also an option to encrypt all the data in that pool, we left it unchecked as we don't need it.
4. In the data menu we chose 'mirror' for the layout option and then clicked on 'Manual Disk Selection' to configure it manually.
5. Add 6 vdevs (via the button in the top right corner).
6. To make your life a bit easier filter the disks by size (our first filter was all 560GB drives), then drag 4 of them into the first vdev.
7. Do this again for the another 2 vdevs.
8. Change the disk size filter (now we chose the 1TB drives) and drag 4 of them into each of the remaining vdevs.
9. When you're done configuring the vdevs click on 'save selection'.
10. All the other setup options are optional, we skipped most of them except from the spare step.
11. In the spare menu we selected 3 1TB drives as spares, you never know 🙃.
12. Like we mentioned earlier the rest of the options we left empty and went straigth to the review section.
13. Click on 'create pool' and the pool should now be available.

---

### Make pool useable
By just creating the pool you still can't use it to store data for now, we have to create a dataset first. Then to be able to use it from any other device we need to add a network share on it.

Here are the steps to do make a dataset:
1. In the web ui go to the 'datasets' tab in the navigation bar on the left.
2. Select the pool you want to use and click on 'add dataset' in the top right corner.
3. Give the dataset a name and keep the preset at 'generic', we left all the advanced settings default.

To add the network share do this:
1. Navigate to the 'shares' tab in the navigation bar on the left.
2. In the 'UNIX (NFS) Shares' field click on 'add'.
3. Under path you need to select the path to the dataset you want to share.
4. Give the share a description, it's not required but can come in handy when you have multiple shares.
5. Open the advanced options and select a user and group for the 'maproot user' and 'maproot group', these determine what rights that the connection will have. If you select root, the Proxmox root user will be able to act as the TrueNAS root account on that dataset. If you select any other account you can limit the rights through the ACL settings of the shared dataset.
6. If you want to limit who can see the share, you can add networks or even specific hosts. 

**==IMPORTANT: if you add networks, only devices on that network will be able to see the share and if you add specific hosts, only those hosts can see it.==**

---

### Use TrueNAS share in Proxmox
You can add the NFS share as storage to Proxmox, in our case we use that share as storage for our other VMs.

Follow this to add the share:
1. In Proxmox select the datacenter and click on storage.
2. Click on add and select NFS.
3. Give it an ID, this will be the name for the storage (like you have local-zfs).
4. Add the IP-address of your TrueNAS server to the 'server' section and put the whole share path into the 'export' box. (you can copy the share path from the TrueNAS ui, under shares)
5. Select what content the share will be used for, in our case it's the default: disk images.

If you want to use this share as boot-drive for a VM or LXC when you create a new one you need to change the standard storage space in the 'disks' section from local-zfs to the share you just created.

If you want to add this share as external storage on a VM or LXC follow these steps:
1. Select your VM/LXC and go to the hardware tab.
2. Click on 'add' and choose 'hard disk'.
3. Select the NFS share in the storage dropdown menu.

**Note: please check if the share still has enough storage space before adding it to VMs or LXCs, when they start to use more storage then there's  available you wont have a great time =)**