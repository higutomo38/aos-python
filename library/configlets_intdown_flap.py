# --- import ---
import common
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import ast

ahost = common.ahost
l = common.blueprint()
token = l[0]
bp_id = l[1]
bp_node_list_system = common.bp_node_list_system(token, bp_id)
bp_diff = common.bp_diff(token, bp_id)

# Check syslog messages of IBA interface flapping
def check_syslog():
  f = open('/var/log/syslog','r')
  line = f.readlines()
  f.close()
  list = []
  # Check only one message
  for i in line:
    if 'if_status_flapping' in i:
      # Divide the message into two
      i = ast.literal_eval(i.split('msg=')[1])
      i = i['alert']['probe_alert']['key_value_pairs']
      for j in i:
        # Create list ['system_id','interface number']
        if j['key'] == 'system_id':
          list.insert(0,j['value'].replace('"',''))
        elif j['key'] == 'key':
          list.append(j['value'].replace('"',''))
      return list
      sys.exit()
  sys.exit()

# get node id from system id
def node_id_from_system_id():
  list = check_syslog()
  for i in bp_node_list_system.values():
    if i["system_id"] == list[0]:
      return i["id"], list[1]

# post configlets
def configlets():
  list = node_id_from_system_id()
  d = open('/home/admin/configlets.json','r')
  f = json.load(d)
  d.close()
  if bp_diff['configlet'] == None:
    f['configlet']['generators'][0]['section_condition'] = "name in [\"" + list[1] + "\"]"
    f['condition'] = "id in [\"" + list[0] + "\"]"
    ep = 'https://' + ahost + '/api/blueprints/{0}/configlets'.format(bp_id)
    requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(f), verify=False)
  else:
    sys.exit()

configlets()
