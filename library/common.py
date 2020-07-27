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
        if aos_response['items'][0]['label'] == sys.argv[2]:
            return token, aos_response['items'][0]['id'], sys.argv[1]
        else:
            print ('----- Error:Blueprint name -----')
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

    def bp_configlets_get(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address,
               '/api/blueprints/{blueprint_id}/configlets')

    def bp_diff_get(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address,
               '/api/blueprints/{blueprint_id}/diff')

    def bp_node_get_system(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address,
               '/api/blueprints/{blueprint_id}/nodes?node_type=system')

    def bp_qe_post_system_role_spineleaf(self, token, bp_id, address):
        return self.request_post_format\
                    (token, bp_id, address, '/api/blueprints/{blueprint_id}/qe',
                     {"query": "node('system', name='system', \
                                     role=is_in(['leaf', 'spine']))"})

    def bp_qe_post_system_role_spineleafl2l3server(self, token, bp_id, address):
        return self.request_post_format\
                    (token, bp_id, address, '/api/blueprints/{blueprint_id}/qe',
                     {"query": "node('system', name='system', \
                                     role=is_in(['leaf', 'spine', 'l2_server', 'l3_server']))"})

    def bp_qe_post_system_systemtype_server(self, token, bp_id, address):
        return self.request_post_format\
                    (token, bp_id, address, '/api/blueprints/{blueprint_id}/qe',
                     {"query": "node('system', name='system', "
                               "system_type='server')"})

    def packages_get(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address, '/api/packages')

    def system_agents_get(self, token, bp_id, address):
        return self.request_get_format(token, bp_id, address, '/api/system-agents')

    def system_agents_id_get(self, token, bp_id, address, agent_id):
        return self.request_get_format(token, bp_id, address,
               '/api/system-agents/{agent_id}'.format(agent_id = agent_id))

# def bp_node_system_get(self):
#     return self.request_get_format('https://' + self.token_bp_id_address[2] \
#                 + '/api/blueprints/{blueprint_id}/nodes?node_type=system'\
#                 .format(blueprint_id = self.token_bp_id_address[1]))
#
# def systems_get(self):
#
#     return self.request_get_format('https://' + self.token_bp_id_address[2] \
#                 + '/api/systems')

# ### Platform
# ## blueprints
# # get diff
# def bp_diff_get(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/diff'.format(blueprint_id = bp_id)
#     resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
#     return resp
#
# # get node list of system (switch, server)
# def bp_node_get_system(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/nodes?node_type=system'.format(blueprint_id = bp_id)
#     resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
#     return resp
#
# # get IBA widgets
# def bp_iba_widgets_get(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/iba/widgets'.format(blueprint_id = bp_id)
#     resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
#     return resp
#
# # get IBA dashboards
# def bp_iba_dashboards_get(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/iba/dashboards'.format(blueprint_id = bp_id)
#     resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
#     return resp
#
# # get IBA Probes
# def bp_probes_get(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/probes'.format(blueprint_id = bp_id)
#     resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
#     return resp
#
# ## packages
# # get packages
# def packages_get(token):
#     ep = 'https://' + args[1] + '/api/packages'
#     resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
#     return resp
#
#
#     ## systems
#     # get systems
# def systems_get(token):
#     ep = 'https://' + args[1] + '/api/systems'
#     resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
#     return resp
#
#
# ## system-agents
# # get system-agents
# def system_agents_get(token):
#     ep = 'https://' + args[1] + '/api/system-agents'
#     resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
#     return resp
#
# # get system-agents-id
# def system_agents_id_get(token, agent_id):
#     ep = 'https://' + args[1] + '/api/system-agents/{agent_id}'.format(agent_id = agent_id)
#     resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
#     return resp
#
#
# # telemetry-service-registry
# def telemetry_service_registry_get(token):
#     ep = 'https://' + args[1] + '/api/telemetry-service-registry'
#     resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
#     return resp
#
#
# ## Graph
# # post qe security_zone - virtual_network
# def bp_qe_post_sec_vn(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
#     payload={"query": "node('security_zone', name='vrf').out().node('virtual_network', name='virtual_network')"}
#     resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
#     return resp
#
# # post qe system
# def bp_qe_post_system(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
#     payload={"query": "node('system', name='system')"}
#     resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
#     return resp
#
# # post qe system (system_type='server')
# def bp_qe_post_system_systemtype(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
#     payload={"query": "node('system', name='system', system_type='server')"}
#     resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
#     return resp
#
# # post qe system - sz_instnce - interface
# def bp_qe_post_system_interface(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
#     payload={"query": "node('system', name='system').out().node('interface', name='interface')"}
#     resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
#     return resp
#
# # post qe system - interface - link - interface - system
# def bp_qe_post_system_interface_link_pair(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
#     payload={"query": "node('system', name='sys_one').out().node('interface', name='int_one').out().node('link').in_('link').node('interface', name='int_two').in_('hosted_interfaces').node('system', name='sys_two').ensure_different('int_one', 'int_two')"}
#     resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
#     return resp
#
# # post qe system - interface_map
# def bp_qe_post_system_interfacemap(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
#     payload={"query": "node('system', name='system').out().node('interface_map', name='map')"}
#     resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
#     return resp
#
# # post qe system - vn_instance - virtual_network - vn_instance - interface
# def bp_qe_post_system_vni_vn_vni_interface(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
#     payload={"query": "node('system',name='system').out().node('vn_instance',name='vn_instance').out().node('virtual_network', name='virtual_network').out().node('vn_instance',name='vn_instance').out().node('interface', name='interface')"}
#     resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
#     return resp
#
# # post qe virtual_network
# def bp_qe_post_vn(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/qe'.format(blueprint_id = bp_id)
#     payload={"query": "node('virtual_network', name='virtual_network')"}
#     resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False).json()
#     return resp
#
#
#
# ### Reference Designs
# ## two_stage_l3clos extension
# # get cabling-map
# def bp_cabling_map_get(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/cabling-map'.format(blueprint_id = bp_id)
#     resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
#     return resp
#
# # get configlets
# def bp_configlets_get(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/configlets'.format(blueprint_id = bp_id)
#     resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
#     return resp
#
# # get racks
# def bp_racks_get(token, bp_id):
#     ep = 'https://' + args[1] + '/api/blueprints/{blueprint_id}/racks'.format(blueprint_id = bp_id)
#     resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
#     return resp
