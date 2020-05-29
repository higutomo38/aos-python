# --- import ---
import common
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
import json
import glob
import os
import time
from zipfile import ZipFile
import tarfile

ahost = common.args[1]
aos_dev_sdk = common.args[3]
l = common.blueprint()
token = l[0]
bp_id = l[1]

class Post_iba_probes:
    def __init__(self):
        self.packages_get = common.packages_get(token)
        self.system_agents_get = common.system_agents_get(token)
        self.telemetry_service_registry_get = common.telemetry_service_registry_get(token)
        self.iba_storage_schema_path = common.iba_storage_schema_path
        self.app_schema = {"service_name": "", "version": "", "storage_schema_path": "", "description": "", "application_schema":""}
    # Post Packages on AOS
    def post_package(self):
        # Unzip args[3]
        with ZipFile('./' + aos_dev_sdk) as myzip: myzip.extractall()
        # Upload whl
        file_list = [ os.path.basename(i) for i in glob.glob('./dist/aosstdcollectors_custom_*.whl') ]
        print ('##### Upload IBA Custom Collectors #####')
        for i in file_list:
            file = './dist/{0}'.format(i)
            data = open(file, 'rb').read()
            ep = 'https://' + ahost + '/api/packages?packagename={0}'.format(i)
            resp = requests.post(ep, data = data, headers={'AUTHTOKEN':token, 'Content-Type': 'application/octet-stream'}, verify=False)
            if str(resp.status_code) == '201': print ('----- Upload {0}'.format(i))
            else:
                print ('----- Error: HTTP request failed {0}'.format(i))
                sys.exit()
        print ('##### Done #####')
        time.sleep(1)

    # Install Packages to Agents
    def install_package(self):
        print ('##### Install Package to Agents #####')
        # Get package list uploaded on AOS
        package_list = [ i['name'] for i in self.packages_get['items']]
        # Patch packages to Agents
        agent_id_list = []
        for i in self.system_agents_get['items']:
            if i['status']['operation_mode'] == 'full_control':
                agent_id_list.append(i['id'])
                for j in package_list:
                    # e.g. 'eos' in 'aosstdcollectors-custom-eos'
                    if i['status']['platform'] in j:
                        list = []
                        list.append(j)
                        payload = {"packages":list, "operation_mode": "full_control" }
                        ep = 'https://' + ahost + '/api/system-agents/{agent_id}'.format(agent_id = i['id'])
                        resp = requests.patch(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False)
                        if str(resp.status_code) == '202': print ('----- Request has been accepted for processing on {0}'.format(i['device_facts']['hostname']))
                        else:
                            print ('----- Error: Request is not accepted on {0}'.format(i['device_facts']['hostname']))
                            sys.exit()
        print ('----- Please wait...Installing now')
        time.sleep(10)
        # Check package installed status
        while len(agent_id_list) != 0:
            system_agents_id_get = common.system_agents_id_get(token, agent_id_list[0])
            for i in system_agents_id_get['telemetry_ext_status']['packages_installed']:
                if 'aosstdcollectors-custom' in i:
                    agent_id_list.remove(agent_id_list[0])
                    print ('----- Package installed on {0}'.format(system_agents_id_get['device_facts']['hostname']))
                else:
                    print ('----- Not installed yet {0}'.format(system_agents_id_get['device_facts']['hostname']))
                    time.sleep(0.5)
        print ('##### Done #####')
        time.sleep(1)

    # Install Service Registry
    def install_service_registry(self):
        print ('##### Install Service Registry from json_schemas.postXXX #####')
        json_schemas = glob.glob('./dist/json_schemas.post*.tar.gz')[0]
        with tarfile.open(json_schemas, 'r') as tar: tar.extractall('./dist')
        # Create list of json files in 'dist'
        json_file_list = [ os.path.basename(i) for i in glob.glob('./dist/*.json') ]
        # Read content of .json, make payload and import service registry entry
        for i in json_file_list:
            with open('./dist/{0}'.format(i)) as f: json_content = f.read()
            self.app_schema['service_name'] = i.replace('.json', '')
            self.app_schema['application_schema'] = json.loads(json_content)
            for j in self.iba_storage_schema_path.items():
                if i.replace('.json', '') in j[1]:
                    self.app_schema['storage_schema_path'] = 'aos.sdk.telemetry.schemas.' + j[0]
                    break
            ep = 'https://' + ahost + '/api/telemetry-service-registry'
            resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(self.app_schema), verify=False)
            if resp.status_code == 422: print ('----- Error: No storage schema path {0}. Update common.py'.format(i.replace('.json', '')))
            elif resp.status_code == 409: print ('----- {0} is already installed'.format(i.replace('.json', '')))
            else: print ('----- Install Service Registry {0}'.format(i))
        print ('##### Done #####')
        time.sleep(1)

    # Create IBA Probes on BP
    def create_probe(self):
        print ('##### Create Probes #####')
        probe_files = glob.glob('./probes/*.json')
        for i in probe_files:
            with open(i) as f: json_content = f.read()
            ep = 'https://' + ahost + '/api/blueprints/{blueprint_id}/probes'.format(blueprint_id = bp_id)
            resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json_content, verify=False)
            if resp.status_code == 201: print ('----- Probe {0} Created'.format(i.replace('./probes/', '')))
            else: print ('----- Error: Probe {0} Install Failed'.format(i.replace('./probes/', '')))
        print ('##### Done #####')

Post_iba_probes().post_package()
Post_iba_probes().install_package()
Post_iba_probes().install_service_registry()
Post_iba_probes().create_probe()
