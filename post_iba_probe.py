import json
import glob
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
import tarfile
import time
from zipfile import ZipFile

from shared import LoginBlueprint
from shared import AosApi

token_bp_id_address = LoginBlueprint().blueprint()
token = token_bp_id_address[0]
bp_id = token_bp_id_address[1]
address = token_bp_id_address[2]


class PostIbaProbes(object):

    def __init__(self):
        pass

    def post_package(self):
        """
        Unzip AosDev SDK, upload whl_file to AOS one by one.
        """
        with ZipFile('./' + sys.argv[3]) as myzip: myzip.extractall()
        whl_file_list = [os.path.basename(whl_file) for whl_file in \
                         glob.glob('./dist/aosstdcollectors_custom_*.whl')]
        print ('##### Upload IBA Custom Collectors #####')
        for whl_file in whl_file_list:
            resp = requests.post(url = 'https://' + address + '/api/packages?packagename=' + whl_file,
                                 data = open('./dist/' + whl_file, 'rb').read(),
                                 headers={'AUTHTOKEN' : token, 'Content-Type': \
                                          'application/octet-stream'}, verify=False)
            if str(resp.status_code) == '201':
                print ('----- Upload ' + whl_file)
            else:
                print ('----- Error: HTTP request failed ' + whl_file)
                sys.exit()
        print ('##### Done #####')
        time.sleep(1)

    def install_package(self):
        """
        Install IBA collector package under the following condition
            'job state' == 'success'
            'operation mode' == 'full_control'
        """
        print('##### Install Package to Agents #####')
        agent_id_list = []
        package_list = [package['name'] for package in AosApi().packages_get(token, bp_id, address)['items']]
        for agent in AosApi().system_agents_get(token, bp_id, address)['items']:
            if agent['running_config']['agent_type'] == 'onbox':

            elif agent['running_config']['agent_type'] == 'offbox':
            if (agent['status']['operation_mode'] == 'full_control' and agent['status']['state'] == 'success') \
                or (agent['status']['operation_mode'] == 'full_control' and agent['status']['connection_state'] == 'connected'):
                for package in package_list:
                    if agent['status']['platform'] in package:
                        payload = {'packages': package.split(), 'operation_mode': 'full_control'}
                        resp = requests.patch('https://' + address + '/api/system-agents/' + agent['id'],
                                              headers={'AUTHTOKEN': token, 'Content-Type': 'application/json'},
                                              data=json.dumps(payload), verify=False)
                        if str(resp.status_code) == '202':
                            print('----- Request has been accepted for processing on '
                                  + agent['device_facts']['hostname'])
                        else:
                            print ('----- Error: Request is not accepted on '
                                   + agent['device_facts']['hostname'])
                            sys.exit()
            agent_id_list.append(agent['id'])
        time.sleep(5)
        """
        Check package installed status
        """
        while len(agent_id_list) != 0:
            system_agents = AosApi().system_agents_id_get(token, bp_id, address, agent_id_list[0])
            for package in system_agents['telemetry_ext_status']['packages_installed']:
                if 'aosstdcollectors-custom' in package:
                    agent_id_list.remove(agent_id_list[0])
                    print ('----- Package installed on ' + system_agents['device_facts']['hostname'])
                else:
                    print ('----- Not installed yet ' + system_agents['device_facts']['hostname'])
                    time.sleep(1)
        print ('##### Done #####')
        time.sleep(1)

    def install_service_registry(self):
        """
        Install service registry from json_schemas.postXXX unziped as 'dist' directory.
        :payload: post data for '/api/telemetry-service-registry'
        :iba_storage_schema_path: Confirm the key i.e.'generic' from original json file.
        """
        payload = {"service_name": "",
                   "version": "",
                   "storage_schema_path": "",
                   "description": "",
                   "application_schema": ""}
        iba_storage_schema_path = {
            'generic': ['table_usage', 'device_info', 'sfp', 'multiagent_detector',
                     'vtep_counters', 'power_supply', 'traceroute', 'acl_stats',
                     'interface_iba', 'mlag_domain', 'vlan', 'pim_rp',
                     'bgp_iba', 'vxlan_address_table', 'anycast_rp',
                     'multicast_info', 'route_count', 'ping', 'bgp_vrf',
                     'multicast_groups', 'vrf', 'evpn_type5', 'vxlan_info',
                     'interface_buffer', 'lldp_details', 'evpn_type3',
                     'process_restart_time', 'interface_details',
                     'resource_usage', 'pim_neighbor_count', 'stp'],
            'interface_counters': ['interface_counters'], 'arp': ['arp'],
            'iba_integer_data': ['dot1x_hosts', 'evpn_vxlan_type5',
                              'vxlan_floodlist', 'resource_util',
                              'evpn_vxlan_type3', 'bgp_route', 'disk_util',
                              'sdwan_policy_rule'], 'hostname': ['hostname'],
            'iba_string_data': ['dot1x', 'ospf_state', 'site_device',
                             'site_device_group', 'site', 'evpn_vxlan_type4',
                             'evpn_vxlan_type1'], 'mlag': ['mlag'],
            'bgp': ['bgp'], 'route': ['route'], 'xcvr': ['xcvr'],
            'graph': ['virtual_infra'], 'interface': ['interface'],
            'lldp': ['lldp'], 'mac': ['mac'], 'lag': ['lag']
        }
        print ('##### Install Service Registry from json_schemas.postXXX #####')
        json_schemas = glob.glob('./dist/json_schemas.post*.tar.gz')[0]
        with tarfile.open(json_schemas, 'r') as tar: tar.extractall('./dist')
        for json_file in [ os.path.basename(json_file) for json_file in glob.glob('./dist/*.json') ]:
            with open('./dist/' + json_file) as f: json_content = f.read()
            payload['service_name'] = json_file.replace('.json', '')
            payload['application_schema'] = json.loads(json_content)
            for schema_path in iba_storage_schema_path.items():
                if json_file.replace('.json', '') in schema_path[1]:
                    payload['storage_schema_path'] = 'aos.sdk.telemetry.schemas.' + schema_path[0]
                    # break
                    resp = requests.post('https://' + address + '/api/telemetry-service-registry',
                                         headers={'AUTHTOKEN': token,
                                                  'Content-Type': 'application/json'},
                                         data=json.dumps(payload), verify=False)
                    if resp.status_code == 422:
                        print ('----- Error: No storage schema path ' + json_file.replace('.json', '')
                               + '. Update iba_storage_schema_path')
                    elif resp.status_code == 409:
                        print ('----- ' + json_file.replace('.json', '') + ' is already installed.')
                    else:
                        print ('----- Install Service Registry ' + json_file)
        print ('##### Done #####')
        time.sleep(1)

    def create_probe(self):
        """
        Install all probes in 'probes' directory.
        :return:
        """
        print ('##### Create Probes #####')
        for probe_file in glob.glob('./probes/*.json'):
            with open(probe_file) as f: json_content = f.read()
            resp = requests.post('https://' + address + '/api/blueprints/' + bp_id + '/probes',
                                 headers={'AUTHTOKEN':token, 'Content-Type':'application/json'},
                                 data=json_content, verify=False)
            if resp.status_code == 201:
                print ('----- Probe ' + probe_file.replace('./probes/', '') + ' Created.')
            else:
                print ('----- Error: Probe ' + probe_file.replace('./probes/', '')
                       + ' Install Failed.')
        print ('##### Done #####')


if __name__ == '__main__':
    # PostIbaProbes().post_package()
    PostIbaProbes().install_package()
    # PostIbaProbes().install_service_registry()
    # PostIbaProbes().create_probe()

