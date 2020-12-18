import getpass
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import socket
import sys

deploy_mode = ['deploy','undeploy','ready','drain']


class LoginBlueprint(object):

    def __init__(self):
        pass

    def aos_login(self):
        """ Get Login Token from AOS using ID/Password.
        :return: tuple: (AOS Login Token, AOS Address)
        """
        if ':' in sys.argv[1]:
            address = sys.argv[1].rsplit(':', 1)[0]
        else:
            address = sys.argv[1]
        try:
            socket.gethostbyname(address)
        except socket.error:
            print('----- Error: FQDN failure -----')
            sys.exit()
        print('AOS Login')
        username = input('ID:')
        password = getpass.getpass()
        url = 'https://' + sys.argv[1] + '/api/user/login'
        payload = {"username": username, "password": password}
        aos_response = requests.post(url,
                             headers = {'Content-Type': 'application/json'},
                             data = json.dumps(payload), verify = False,
                             timeout = 3)
        if str(aos_response.status_code)[0] == '2':
            aos_response = aos_response.json()
        else:
            print(
                '----- Error: HTTP Server/Client error or Authentication failure -----')
            sys.exit()
        if 'token' in aos_response:
            return aos_response['token']
        else:
            print('----- Error: Authentication failure -----')
            sys.exit()

    def blueprint(self):
        """ Get Login Token and Bluprint ID from Blueprint Name
        :return: tuple: (AOS Login Token, Blueprint ID, AOS Address)
        """
        token = self.aos_login()
        url = 'https://' + sys.argv[1] + '/api/blueprints'
        aos_response = requests.get(url,
                headers = {'AUTHTOKEN': token, 'Content-Type': 'application/json'},
                verify = False).json()
        if sys.argv[2] in [ bp['label'] for bp in aos_response['items']]:
            for bp in aos_response['items']:
                if bp['label'] == sys.argv[2]:
                    return token, bp['id'], sys.argv[1]
        else:
            print('----- Error:Blueprint name -----')
            sys.exit()


class AosApi(object):

    def __init__(self):
        pass

    def request_get_format(self, token, bp_id, address, api_path):
        """ Make request GET function
        :param: AOS Token, Blueprint ID, AOS Address, API Path
        :return: Request GET function for specific path.
        """
        if '{blueprint_id}' in api_path:
            return requests.get('https://' + address + api_path.format(blueprint_id = bp_id),
                                headers = {'AUTHTOKEN': token, 'Content-Type': 'application/json'},
                                verify = False).json()
        else:
            return requests.get('https://' + address + api_path,
                                headers = {'AUTHTOKEN': token, 'Content-Type': 'application/json'},
                                verify = False).json()

    def request_post_format(self, token, bp_id, address, api_path, payload):
        """ Make request POST function
        :param: AOS Token, Blueprint ID, AOS Address, API Path, Payload
        :return: Request POST function for specific path.
        """
        if '{blueprint_id}' in api_path:
            return requests.post('https://' + address + api_path.format(blueprint_id = bp_id),
                                 headers = {'AUTHTOKEN': token, 'Content-Type': 'application/json'},
                                 data = json.dumps(payload), verify = False).json()
        else:
            return requests.post('https://' + address + api_path,
                                 headers = {'AUTHTOKEN': token, 'Content-Type': 'application/json'},
                                 data = json.dumps(payload), verify = False).json()

    def bp_cabling_map_get(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address,
               '/api/blueprints/{blueprint_id}/cabling-map')

    def bp_configlets_get(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address,
               '/api/blueprints/{blueprint_id}/configlets')

    def bp_diff_get(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address, '/api/blueprints/{blueprint_id}/diff')

    def bp_node_get_system(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address, '/api/blueprints/{blueprint_id}/nodes?node_type=system')

    def bp_qe_post(self, token, bp_id, address, qe):
        return self.request_post_format \
            (token, bp_id, address, '/api/blueprints/{blueprint_id}/qe', {"query": qe})

    def bp_racks_get(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address, '/api/blueprints/{blueprint_id}/racks')

    def bp_security_zone_get(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address, '/api/blueprints/{blueprint_id}/security-zones')

    def packages_get(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address, '/api/packages')

    def systems_get(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address, '/api/systems')

    def system_agents_get(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address, '/api/system-agents')

    def system_agents_id_get(self, token, bp_id, address, agent_id):
        return self.request_get_format(token, bp_id, address, '/api/system-agents/' + agent_id)

    def telemetry_service_registry_get(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address, '/api/telemetry-service-registry')

