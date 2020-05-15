# --- import ---
import common
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import os
import re
import shutil
import datetime

ahost = common.args[1]
l = common.blueprint()
token = l[0]
bp_id = l[1]

bp_node_get_system = common.bp_node_get_system(token, bp_id)

# get NOS rendering config
def nos_config():
  dict = {}
  for i in bp_node_get_system["nodes"].values():
    if i["role"] == "spine" or i["role"] == "leaf": dict[i["id"]] = i['hostname']
  os.makedirs('./nos_config', exist_ok = True)
  for i, j in dict.items():
    ep = 'https://' + ahost + '/api/blueprints/{0}/nodes/{1}/config-rendering'.format(bp_id, i)
    resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
    with open('./nos_config/' + j + '.conf','w') as f:
      print((resp['config']), file = f)
  now = re.sub('[ :]','-', datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
  shutil.make_archive(now, 'zip', 'nos_config')

nos_config()
