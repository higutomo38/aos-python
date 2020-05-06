### Get common info: Token, BP ID, Node ID and EndPoint
#
# --- import ---
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import getpass
import socket

args = sys.argv

# --- exec ---
# aos login
def login():
  try:
    addr = socket.gethostbyname(args[1])
  except socket.error:
    print ('----- Error:FQDN failure -----')
    sys.exit()
  print('AOS Login')
  uname = input('ID:')
  passw = getpass.getpass()
  ep = 'https://' + args[1] + '/api/user/login'
  payload={"username":uname, "password":passw}
  resp = requests.post(ep, headers={'Content-Type':'application/json'}, data=json.dumps(payload), verify=False, timeout=3)
  # Check response code is 2XX
  if str(resp.status_code)[0] == '2': resp = resp.json()
  else:
    print ('----- Error: HTTP Server/Client error or Authentication failure -----')
    sys.exit()
  if 'token' in resp: return resp['token']
  else:
    print ('----- Error:Authentication failure -----')
    sys.exit()

# get blueprint id
def blueprint():
  token = login()
  ep = 'https://' + args[1] + '/api/blueprints'
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  for i in resp['items']:
    if i['label'] == args[2]: return token, i['id']
  print ('----- Error:Blueprint name -----')
  sys.exit()

# get node id of system (switch, server)
def bp_node_id_system(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{0}/nodes?node_type=system'.format(bp_id)
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  dict = resp["nodes"]
  for i in dict.values():
    if i['hostname'] == hostname: return i['id']
  print ('----- Error:Hostname -----')
  sys.exit()

# get node id list of system (switch)
def bp_node_id_list_system(token, bp_id):
  list = []
  ep = 'https://' + args[1] + '/api/blueprints/{0}/nodes?node_type=system'.format(bp_id)
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  for i in resp["nodes"].values():
    if i["role"] == "spine" or i["role"] == "leaf": list.append(i["id"])
  return list

# get node id + hostname of system (switch)
def bp_node_id_hostname_list_system(token, bp_id):
  dict = {}
  ep = 'https://' + args[1] + '/api/blueprints/{0}/nodes?node_type=system'.format(bp_id)
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  for i in resp["nodes"].values():
    if i["role"] == "spine" or i["role"] == "leaf": dict[i["id"]] = i['hostname']
  return dict

# get node list of system (switch, server)
def bp_node_list_system(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{0}/nodes?node_type=system'.format(bp_id)
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  return resp["nodes"]

# get diff
def bp_diff(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{0}/diff'.format(bp_id)
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  return resp

# get configlets
def bp_configlets(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{0}/configlets'.format(bp_id)
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  return resp

# get graph system - sz_instnce - interface - link(switch, server, er)
def bp_graph_system_interface(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{0}/qe'.format(bp_id)
  payload={"query": "node('system', name='system').out('hosted_interfaces').node('interface', name='interface')"}
  resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
  return resp

# get graph system - interface - link - pair(switch, server, er)
def bp_graph_system_interface_link_pair(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{0}/qe'.format(bp_id)
  payload={"query": "node('system', name='sys_one').out('hosted_interfaces').node('interface', name='int_one').out('link').node('link').in_('link').node('interface', name='int_two').in_('hosted_interfaces').node('system', name='sys_two').ensure_different('int_one', 'int_two')"}
  resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
  return resp

# get graph security_zone - virtual_network - vn_instance - interface
def bp_graph_sec_vn(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{0}/qe'.format(bp_id)
  payload={"query": "node('security_zone', name='vrf').out().node('virtual_network', name='virtual_network')"}
  resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
  return resp

# get graph system - vn_instance - virtual_network - vn_instance - interface
def bp_graph_system_vnins_vn_vnins_interface(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{0}/qe'.format(bp_id)
  payload={"query": "node('system',name='system').out('hosted_vn_instances').node('vn_instance',name='vn_instance').out('instantiates').node('virtual_network', name='virtual_network').out('instantiated_by').node('vn_instance',name='vn_instance').out('member_interfaces').node('interface', name='interface')"}
  resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
  return resp

# get graph system - interface_map
def bp_graph_system_interfacemap(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{0}/qe'.format(bp_id)
  payload={"query": "node('system', name='system').out('interface_map').node('interface_map', name='map')"}
  resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
  return resp

# get graph system
def bp_graph_system(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{0}/qe'.format(bp_id)
  payload={"query": "node('system', name='system')"}
  resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
  return resp

# get graph virtual network
def bp_graph_vn(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{0}/qe'.format(bp_id)
  payload={"query": "node('virtual_network', name='virtual_network')"}
  resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
  return resp

# get racks
def bp_racks_get(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/racks'.format(blueprint_id = bp_id)
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  return resp

# get cabling-map
def bp_cabling_map_get(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/cabling-map'.format(blueprint_id = bp_id)
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  return resp

 # get nodes interface
def bp_nodes_interface_get(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/nodes?node_type=interface'.format(blueprint_id = bp_id)
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  return resp

 # get nodes
def bp_nodes_system_get(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/nodes?node_type=system'.format(blueprint_id = bp_id)
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  return resp

 # get agents
def system_agents_get(token):
  ep = 'https://' + args[1] + '/api/system-agents'
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  return resp

 # get systems
def systems_get(token):
  ep = 'https://' + args[1] + '/api/systems'
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  return resp

# get node id of system (switch, server)
# ex.3590eec3-0b56-4b2f-90d6-e428d5d499e9

# get node id list of system (switch)
#['2d67fb09-cba3-4768-b069-8e9de1bdb536', '418025bd-1d88-47bb-9dc8-e850708f27fa', '5242d03f-8418-44e9-b0d5-2ebd49dc2ba0', '20e82f60-85d2-4864-8c53-8068b5445ce5', '8041cfc6-9b8f-4137-b291-88bc5d0d24d4', '3590eec3-0b56-4b2f-90d6-e428d5d499e9']

# get node id + hostname of system (switch)
#{'2d67fb09-cba3-4768-b069-8e9de1bdb536': 'switch-leaf3', '418025bd-1d88-47bb-9dc8-e850708f27fa': 'switch-spine1', '5242d03f-8418-44e9-b0d5-2ebd49dc2ba0': 'switch-leaf4', '20e82f60-85d2-4864-8c53-8068b5445ce5': 'switch-spine2', '8041cfc6-9b8f-4137-b291-88bc5d0d24d4': 'switch-leaf1', '3590eec3-0b56-4b2f-90d6-e428d5d499e9': 'switch-leaf2'}

# get node list of system (switch, server)
# ex.{'2d67fb09-cba3-4768-b069-8e9de1bdb536': {'tags': None, 'position_data': None, 'property_set': None, 'hostname': 'leaf3-001', 'group_label': 'leaf', 'label': 'leaf-003', 'role': 'leaf', 'system_type': 'switch', 'deploy_mode': 'deploy', 'system_id': '2CC260994301', 'type': 'system', 'id': '2d67fb09-cba3-4768-b069-8e9de1bdb536'}, '418025bd-1d88-47bb-9dc8-e850708f27fa': {'tags': None, 'position_data': {'position': 0, 'region': 0, 'plane': 0, 'pod': 0}, 'property_set': None, 'hostname': 'spine-001', 'group_label': None, 'label': 'spine-001', 'role': 'spine', 'system_type': 'switch', 'deploy_mode': 'deploy', 'system_id': '2CC260993101', 'type': 'system', 'id': '418025bd-1d88-47bb-9dc8-e850708f27fa'}, '5242d03f-8418-44e9-b0d5-2ebd49dc2ba0': {'tags': None, 'position_data': None, 'property_set': None, 'hostname': 'leaf4-001', 'group_label': 'leaf', 'label': 'leaf-004', 'role': 'leaf', 'system_type': 'switch', 'deploy_mode': 'deploy', 'system_id': '2CC260994401', 'type': 'system', 'id': '5242d03f-8418-44e9-b0d5-2ebd49dc2ba0'}, '353d79f9-9e63-4337-82a6-31030a49b836': {'tags': None, 'position_data': None, 'property_set': None, 'hostname': 'server-001', 'group_label': 'server', 'label': 'server-001', 'role': 'l2_server', 'system_type': 'server', 'deploy_mode': None, 'system_id': None, 'type': 'system', 'id': '353d79f9-9e63-4337-82a6-31030a49b836'}, '4040f623-53dd-40df-b800-f1dc8d661347': {'tags': None, 'position_data': None, 'property_set': None, 'hostname': 'server-003', 'group_label': 'server', 'label': 'server-003', 'role': 'l2_server', 'system_type': 'server', 'deploy_mode': None, 'system_id': None, 'type': 'system', 'id': '4040f623-53dd-40df-b800-f1dc8d661347'}, '3023e821-9139-4240-9517-ce9485d76a02': {'tags': None, 'position_data': None, 'property_set': None, 'hostname': 'server-002', 'group_label': 'server', 'label': 'server-002', 'role': 'l2_server', 'system_type': 'server', 'deploy_mode': None, 'system_id': None, 'type': 'system', 'id': '3023e821-9139-4240-9517-ce9485d76a02'}, 'b3566f9b-0ae6-4065-846f-80b97892ac49': {'tags': None, 'position_data': None, 'property_set': None, 'hostname': None, 'group_label': None, 'label': 'Demo-ER', 'role': 'external_router', 'system_type': 'switch', 'deploy_mode': None, 'system_id': None, 'type': 'system', 'id': 'b3566f9b-0ae6-4065-846f-80b97892ac49'}, '20e82f60-85d2-4864-8c53-8068b5445ce5': {'tags': None, 'position_data': {'position': 1, 'region': 0, 'plane': 0, 'pod': 0}, 'property_set': None, 'hostname': 'spine-002', 'group_label': None, 'label': 'spine-002', 'role': 'spine', 'system_type': 'switch', 'deploy_mode': 'deploy', 'system_id': '2CC260993201', 'type': 'system', 'id': '20e82f60-85d2-4864-8c53-8068b5445ce5'}, '8041cfc6-9b8f-4137-b291-88bc5d0d24d4': {'tags': None, 'position_data': None, 'property_set': None, 'hostname': 'leaf1-001', 'group_label': 'leaf', 'label': 'leaf-001', 'role': 'leaf', 'system_type': 'switch', 'deploy_mode': 'deploy', 'system_id': '2CC260994101', 'type': 'system', 'id': '8041cfc6-9b8f-4137-b291-88bc5d0d24d4'}, '73715f15-9b11-4762-a522-3769f6c3695f': {'tags': None, 'position_data': None, 'property_set': None, 'hostname': 'server-004', 'group_label': 'server', 'label': 'server-004', 'role': 'l2_server', 'system_type': 'server', 'deploy_mode': None, 'system_id': None, 'type': 'system', 'id': '73715f15-9b11-4762-a522-3769f6c3695f'}, '3590eec3-0b56-4b2f-90d6-e428d5d499e9': {'tags': None, 'position_data': None, 'property_set': None, 'hostname': 'leaf2-001', 'group_label': 'leaf', 'label': 'leaf-002', 'role': 'leaf', 'system_type': 'switch', 'deploy_mode': 'deploy', 'system_id': '2CC260994201', 'type': 'system', 'id': '3590eec3-0b56-4b2f-90d6-e428d5d499e9'}}

# get diff
#{u'external_endpoint': None, u'internal_endpoint': None, u'external_endpoints_group': None, u'enforcement_points_group': None, u'internal_endpoints_group': None, u'configlet': {u'removed': {}, u'added': {u'acb6bc1c-01fa-4795-a2e5-829926774933': {u'label': u'Interface DownUP'}}, u'changed': {}}, u'security_zone': None, u'policy': None, u'virtual_network': None, u'virtual_infra': None, u'digest': {u'node': {u'removed': 0, u'added': 1, u'changed': 0}, u'relationship': {u'removed': 0, u'added': 0, u'changed': 0}}}

# get configlets
#{u'items': [{u'configlet': {u'generators': [{u'config_style': u'cumulus', u'section': u'interface', u'section_condition': u'name in ["swp5"]', u'filename': u'', u'template_text': u'link down', u'negation_template_text': u''}], u'display_name': u'Cumulus Linkdown'}, u'id': u'52791a4a-82d7-4f79-b661-29bae191c544', u'condition': u'id in ["c2cb6cd7-ed3d-47c7-889b-903ff1698e64"]', u'label': u'Cumulus Linkdown'}]}

# get graphqe relationship (switch, server, er)
