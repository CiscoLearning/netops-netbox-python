import csv
import os
import pynetbox

# Connect to NetBox
netbox_url = os.getenv("NETBOX_ADDRESS")
netbox_token = os.getenv("NETBOX_API_TOKEN")

if netbox_url is None or netbox_token is None:
    print("No ENV VARS for NetBox found")
    exit(1)

# Connect to NetBox API
nb = pynetbox.api(netbox_url, token=netbox_token)

# Open the CSV file containing the new router details
with open('demo_1.csv', mode='r', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile) 
    
    for row in csvreader:
        try:
            # Create the devices in NetBox
            device = nb.dcim.devices.create(
                name=row['name'],
                status=row['status'],
                position=row['position'],
                face=row['face'],
                serial=row['serial'],
                device_type=nb.dcim.device_types.get(model=row['device_type']).id,
                device_role=nb.dcim.device_roles.get(name=row['device_role']).id,
                site=nb.dcim.sites.get(name=row['site']).id,
                rack=nb.dcim.racks.get(name=row['rack']).id
            )
            print(f"Device '{device.name}' created successfully.")
        except pynetbox.RequestError as e:
            print(f"Error creating device '{row['name']}': {e}")