### Get common info: Token, BP ID, Node ID and etc
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
deploy_mode = ['deploy','undeploy','ready','drain']
iba_storage_schema_path = {
'iba_integer_data':['table_usage', 'sfp', 'power_supply', 'dot1x_hosts', 'evpn_vxlan_type5', 'resource_util', 'evpn_vxlan_type3', 'anycast_rp', 'vxlan_inf', 'mlag_domai', 'bgp_route', 'disk_util', 'sdwan_policy_rule'],
'generic':['device_info', 'vtep_counters', 'traceroute', 'acl_stats', 'interface_iba', 'mlag_domain', 'vlan', 'pim_rp', 'bgp_iba', 'vxlan_address_table', 'multicast_info', 'route_count', 'ping', 'bgp_vrf', 'multicast_groups', 'vrf', 'evpn_type5', 'vxlan_info', 'interface_buffer', 'lldp_details', 'evpn_type3', 'process_restart_time', 'interface_details', 'resource_usage', 'pim_neighbor_count', 'stp', 'site_device_group', 'site_device'],
'interface_counters':['interface_counters'],
'arp':['arp'],
'hostname':['hostname'],
'iba_string_data':['dot1x', 'ospf_state'],
'mlag':['mlag'],
'bgp':['bgp'],
'route':['route'],
'xcvr':['xcvr'],
'graph':['virtual_infra'],
'interface':['interface'],
'lldp':['lldp'],
'mac':['mac'],
'lag':['lag']
}

# --- exec ---
# aos login and get token
def login():
    if ':' in args[1]:
        addr = args[1].rsplit(':', 1)[0]
    else: addr = args[1]
    try:
        socket.gethostbyname(addr)
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



### Platform
## blueprints
# get diff
def bp_diff_get(token, bp_id):
    ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/diff'.format(blueprint_id = bp_id)
    resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
    return resp

# get node list of system (switch, server)
def bp_node_get_system(token, bp_id):
    ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/nodes?node_type=system'.format(blueprint_id = bp_id)
    resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
    return resp


## packages
# get packages
def packages_get(token):
    ep = 'https://' + args[1] + '/api/packages'
    resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
    return resp


    ## systems
    # get systems
def systems_get(token):
    ep = 'https://' + args[1] + '/api/systems'
    resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
    return resp


## system-agents
# get system-agents
def system_agents_get(token):
    ep = 'https://' + args[1] + '/api/system-agents'
    resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
    return resp

# get system-agents-id
def system_agents_id_get(token, agent_id):
    ep = 'https://' + args[1] + '/api/system-agents/{agent_id}'.format(agent_id = agent_id)
    resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
    return resp


# telemetry-service-registry
def telemetry_service_registry_get(token):
    ep = 'https://' + args[1] + '/api/telemetry-service-registry'
    resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
    return resp


## Graph
# post qe security_zone - virtual_network
def bp_qe_post_sec_vn(token, bp_id):
    ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
    payload={"query": "node('security_zone', name='vrf').out().node('virtual_network', name='virtual_network')"}
    resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
    return resp

# post qe system
def bp_qe_post_system(token, bp_id):
    ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
    payload={"query": "node('system', name='system')"}
    resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
    return resp

# post qe system (system_type='server')
def bp_qe_post_system_systemtype(token, bp_id):
    ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
    payload={"query": "node('system', name='system', system_type='server')"}
    resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
    return resp

# post qe system - sz_instnce - interface
def bp_qe_post_system_interface(token, bp_id):
    ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
    payload={"query": "node('system', name='system').out().node('interface', name='interface')"}
    resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
    return resp

# post qe system - interface - link - interface - system
def bp_qe_post_system_interface_link_pair(token, bp_id):
    ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
    payload={"query": "node('system', name='sys_one').out().node('interface', name='int_one').out().node('link').in_('link').node('interface', name='int_two').in_('hosted_interfaces').node('system', name='sys_two').ensure_different('int_one', 'int_two')"}
    resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
    return resp

# post qe system - interface_map
def bp_qe_post_system_interfacemap(token, bp_id):
    ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
    payload={"query": "node('system', name='system').out().node('interface_map', name='map')"}
    resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
    return resp

# post qe system - vn_instance - virtual_network - vn_instance - interface
def bp_qe_post_system_vni_vn_vni_interface(token, bp_id):
    ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
    payload={"query": "node('system',name='system').out().node('vn_instance',name='vn_instance').out().node('virtual_network', name='virtual_network').out().node('vn_instance',name='vn_instance').out().node('interface', name='interface')"}
    resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
    return resp

# post qe virtual_network
def bp_qe_post_vn(token, bp_id):
    ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
    payload={"query": "node('virtual_network', name='virtual_network')"}
    resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
    return resp



### Reference Designs
## two_stage_l3clos extension
# get cabling-map
def bp_cabling_map_get(token, bp_id):
    ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/cabling-map'.format(blueprint_id = bp_id)
    resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
    return resp

# get configlets
def bp_configlets_get(token, bp_id):
    ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/configlets'.format(blueprint_id = bp_id)
    resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
    return resp

# get racks
def bp_racks_get(token, bp_id):
    ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/racks'.format(blueprint_id = bp_id)
    resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
    return resp
