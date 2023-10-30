# IBM-QRadar-Network-Hierarchy
Python script to import Network Hierarchy info into IBM QRadar.

In this repository, you will find a script allowing you to back up or update the network hierarchy in Qradar using the API. The current way to update the network hierarchy is through the GUI, but if you have a large number of networks this is a nightmare.

Ref: github.com/chmedinap/Qradar-Manage_Network_Hierarchy

I customized the code in some places to adapt to my needs.

## How it works

- Step 1: The script will get the current network hierarchy as a backup. JSON format.
- Step 2: The script will get the domains because we need the domain_id to create the network hierarchy. 
- Step 3: You need to manually create a CSV file with the new networks like this:
```csv
id,group,name,description,cidr,domain_id,country_code
10,Group_1,Test_Name,Test_Desc,192.168.10.0/24,6,
```
 **Notes:**
  The script will get the max ID of the current network hierarchy. So the new IDs will be the max ID in networks **+1, +2, +3**, etc.


- Step 4: As the API is designed to **REPLACE** the current network hierarchy, we need to merge the CSV file with the 
current network hierarchy.
- Step 5: Send the new network hierarchy to Qradar.
- Step 6: Check the new network hierarchy in the Qradar console.
- Step 7: Deploy config on Qradar.

## API Reference:

These are the API endpoints that are used in the script.

#### GET network_hierarchy: Retrieves the staged network hierarchy.

```https
   GET - /config/network_hierarchy/staged_networks
```
Response Description

Network Hierarchy - A JSON string that contains network_hierarchy objects.

#### PUT network_hierarchy/staged_networks: Replaces the current network hierarchy with the input that is provided.

```https
   PUT - /config/network_hierarchy/staged_networks
```

Network Hierarchy - A JSON string that contains network_hierarchy objects. this is an example of the JSON that is required to update the network hierarchy.

```json
[
{
"id": 4,
"group": "DMZ",
"name": "External",
"description": "network description",
"cidr": "0.0.0.1/32",
"domain_id": 0,
"location": {"type": "Point", "coordinates": [-75.69805556, 45.41111111]},
"country_code": "CA"
},
{
"id": 5,
"group": "DMZ",
"name": "External",
"description": "network description",
"cidr": "0.0.0.2/32",
"domain_id": 0,
"location": {"type": "Point", "coordinates": [-66.646332, 45.964993]},
"country_code": "CA"
}
]
```
#### GET domains: Retrieves the list of domains.

```https
   GET - /config/domain_management/domains
```
