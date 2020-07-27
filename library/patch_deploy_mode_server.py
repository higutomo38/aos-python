import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys

import common
from common import LoginBlueprint
from common import AosApi

token_bp_id_address = LoginBlueprint().blueprint()
token = token_bp_id_address[0]
bp_id = token_bp_id_address[1]
address = token_bp_id_address[2]


class PatchDeployMode(object):

    def __init__(self):
        pass

    def patch_deploy_mode(self):
        """
        Change server deploy mode.
        """
        input_mode = input('deploy_mode:')
        if input_mode in common.deploy_mode:
            payload = {'nodes': {}}
            for system in AosApi().bp_qe_post_system_systemtype_server(token, bp_id, address)['items']:
                payload['nodes'][system['system']['id']] = {'deploy_mode': input_mode}
            requests.patch('https://' + address + '/api/blueprints/{blueprint_id}'\
                           .format(blueprint_id = bp_id),
                           headers = {'AUTHTOKEN': token, 'Content-Type': 'application/json'},
                           data=json.dumps(payload), verify=False)
        else:
            print ('Error: Wrong deploy mode')
            sys.exit()

if __name__ == '__main__':
    PatchDeployMode().patch_deploy_mode()

