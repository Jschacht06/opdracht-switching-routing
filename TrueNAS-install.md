truneas install hoeft niet gedocumenteerd te worden, wel hoe de pool in elkaar zit met vdevs, de nfs share en hoe de drives passthrough werkt in proxmox

# TrueNAS
We installed TrueNAS with the default settings and chose to configure everything in the web-ui with the truenas_admin account. At the end of the installation we chose to shut down instead of reboot, because we then connected the PCI-card with the JBODs.

## JBOD passthrough
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

## TrueNAS pool/vdev creation
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