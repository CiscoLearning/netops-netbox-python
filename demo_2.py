import pynetbox
import os

# Connect to NetBox
netbox_url = os.getenv("NETBOX_ADDRESS")
netbox_token = os.getenv("NETBOX_API_TOKEN")

if netbox_url is None or netbox_token is None:
    print("No ENV VARS for NetBox found")
    exit(1)

# Connect to NetBox API
nb = pynetbox.api(netbox_url, token=netbox_token)

# Variables
device_type = 'Firepower 4110-ASA'         # The model of the device to filter
old_version = 'asa.9.12.3.9'               # Old platform version
new_version = 'asa.9.14.2.8'               # New platform version to upgrade to

# Find Firepower 4110 devices with the old platform version
devices_to_update = nb.dcim.devices.filter(
    device_type_id=nb.dcim.device_types.get(model=device_type).id,
    platform_id=nb.dcim.platforms.get(name=old_version).id
)

# Uncomment if you want to see the list of devices that needs to be updated.
# for device in devices_to_update:
#     print(f" {device.name} in {device.site.name} at {device.rack.name} with platform version {old_version}")

# Assume firmware updates are done here (outside the scope of NetBox and this script)

# Fetch the new platform object from NetBox
new_platform = nb.dcim.platforms.get(name=new_version)
if not new_platform:
    print(f"Error: The new platform '{new_version}' not found in NetBox.")
    exit()

# Update the platform in NetBox for each device
for device in devices_to_update:
    device.platform = new_platform.id
    device.save()
    print(f"Updated platform for {device.name} to '{new_version}'")

