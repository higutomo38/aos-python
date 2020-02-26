# --- import ---
import common
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import os

ahost = common.ahost
l = common.blueprint()
token = l[0]
bp_id = l[1]

bp_node_id_hostname_list_system = common.bp_node_id_hostname_list_system(token, bp_id)

# get NOS rendering config
def nos_config():
  os.makedirs('./nos_config', exist_ok = True)
  for i, j in bp_node_id_hostname_list_system.items():
    ep = 'https://' + ahost + '/api/blueprints/{0}/nodes/{1}/config-rendering'.format(bp_id, i)
    resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
    with open('./nos_config/' + j + '.conf','w') as f:
      print((resp['config']), file = f)

nos_config()
