# --- import ---
import common
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import ast

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
        if j['key'] == 'system_id': list.insert(0,j['value'].replace('"',''))
        elif j['key'] == 'key': list.append(j['value'].replace('"',''))
      return list # [system id, interface number]
      sys.exit()
  sys.exit()

list = check_syslog()

ahost = common.args[1]
l = common.blueprint()
token = l[0]
bp_id = l[1]
bp_node_list_system = common.bp_node_list_system(token, bp_id)
bp_diff = common.bp_diff(token, bp_id)
configlets_dic = common.bp_configlets(token, bp_id)

# get node id from system id
def node_id_from_system_id():
  for i in bp_node_list_system.values():
    if i["system_id"] == list[0]: return i["id"], list[1] # (node id, interface number)

# post configlets
def configlets():
  tupl = node_id_from_system_id()
  # Check whether adding configlets already exist in current BP or not.
  for i in configlets_dic['items']:
    if tupl[0] in i['condition'] and tupl[1] in i['configlet']['generators'][0]['section_condition']: sys.exit()
  d = open('configlets.json','r')
  f = json.load(d)
  d.close()
  # Check whether uncommited configlets is in BP.
  if bp_diff['configlet'] == None:
    f['configlet']['generators'][0]['template_text'] = f['configlet']['generators'][0]['template_text'].replace('x',tupl[1])
    f['configlet']['generators'][0]['negation_template_text'] = f['configlet']['generators'][0]['negation_template_text'].replace('x',tupl[1])
    f['condition'] = "id in [\"" + tupl[0] + "\"]"
    ep = 'https://' + ahost + '/api/blueprints/{0}/configlets'.format(bp_id)
    requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(f), verify=False)
  else:
    sys.exit()

configlets()
