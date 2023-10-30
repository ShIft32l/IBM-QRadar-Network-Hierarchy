#!/usr/bin/python3
# IBM QRadar Network Hierarchy
# Writer: shift321
# References: github/chmedinap/Qradar-Manage_Network_Hierarchy
# Date: 26-10-2023

import json
import requests
import pandas as pd
from pandas import json_normalize
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.filterwarnings("ignore")
import logging

#create a log
logging.basicConfig(filename='network-hierarchy.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.info('The script has started')

#authentication
SEC_TOKEN = 'import your sec token'
URL_base = 'https://domain/api'

header = {
    'SEC':SEC_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

#save the current configuration of the network hierarchy as a backup
URL_suffix='/config/network_hierarchy/staged_networks'
URL_Networks = URL_base + URL_suffix
def get_networks():
    try:
        response = requests.get(URL_Networks, verify=False, headers=header)
        if response.status_code == 200:
            logging.info('The networks were obtained successfully')
            networks = response.text
            return networks
        else:
            logging.error('The networks were not obtained')
            return None
    except Exception as e:
        logging.error('The networks were not obtained')
        logging.error(e)
        return None
    
#save the current configuration of the network hierarchy
networks = get_networks()
#save the response in text format
with open('networks.txt', 'w') as f:
    f.write(networks)
logging.info('The current configuration of the network hierarchy was saved')

#obtain the domains id created in Qradar
URL_suffix='/config/domain_management/domains'
URL_Domains = URL_base + URL_suffix
def get_domains():
    try:
        response = requests.get(URL_Domains, verify=False, headers=header)
        if response.status_code == 200:
            logging.info('The domains were obtained successfully')
            #create a DF with the domains
            domains = pd.DataFrame(response.json())
            #select the columns that we need
            domains = domains[['id','name','deleted']]
            return domains
        else:
            logging.error('The domains were not obtained')
            return None
    except Exception as e:
        logging.error('The domains were not obtained')
        logging.error(e)
        return None
    
#obtain the domains id
domains = get_domains()

#obtain the networks id in networks
df_networks=json.loads(networks)
df_networks = pd.DataFrame(df_networks)
#obtain the max id in networks
max_id = df_networks['id'].max()

print('The max id in networks is: ',max_id)
logging.info('The max id in networks is: ' + str(max_id))
print('The domains were obtained successfully, you need to keep this in mind for the next step')
logging.info('The domains were obtained and printed successfully')
print(domains)

#read the csv file with the new networks to insert
df_new_networks = pd.read_csv('new-networks.csv')
logging.info('The new networks were read successfully')
df_new_networks
#print(df_new_networks)

#Define a custom function to filter NaN values CSV file when converting to JSON
def custom_json_records(dataframe):
    records = []
    for index, row in dataframe.iterrows():
        record = row.dropna().to_dict()
        records.append(record)
    return records

#transform the df_new_networks to json centered in the index but without the index in the json
new_networks = json.dumps(custom_json_records(df_new_networks))
#print(new_networks)

#concatenate the new networks with the current networks
networks = networks[:-1] + ',' + new_networks[1:]
logging.info('The new networks were concatenated successfully')
#transform string type to list type in python
json_object = json.loads(networks)
print(networks)

#put the new networks in the network hierarchy in Qradar
URL_suffix='/config/network_hierarchy/staged_networks'
URL_Domains = URL_base + URL_suffix
def put_networks(networks):
    try:
        response = requests.put(URL_Domains, verify=False, headers=header, data=json.dumps(json_object))
        if response.status_code == 200:
            logging.info('The networks were inserted successfully')
            return True
        else:
            logging.error('The networks were not inserted')
            print(response.text)
            return False
    except Exception as e:
        logging.error('The networks were not inserted')
        logging.error(e)
        return False
    
#insert the new networks
put_networks(networks)
logging.info('end of the script')