import datetime
import os
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import shutil

from shared import LoginBlueprint
from shared import AosApi

token_bp_id_address = LoginBlueprint().blueprint()
token = token_bp_id_address[0]
bp_id = token_bp_id_address[1]
address = token_bp_id_address[2]


class GetNosConfig(object):

    def __init__(self):
        pass

    def get_nos_config(self):
        """
        Save NOS configs of spine and leaf on local as zip file.
        """
        os.makedirs('./nos_config', exist_ok=True)
        for system in AosApi().bp_qe_post_system_role_spineleaf(token, bp_id, address)['items']:
            url = 'https://' + address \
                  + '/api/blueprints/{blueprint_id}/nodes/{node_id}/config-rendering'\
                  .format(blueprint_id = bp_id, node_id = system['system']['id'])
            with open('./nos_config/' + system['system']['hostname'] + '.conf', 'w') as config:
                print((requests.get(url, headers = {'AUTHTOKEN': token,
                                                    'Content-Type': 'application/json'},
                                    verify = False).json()['config']), file = config)
        now = re.sub('[ :]', '-', datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        shutil.make_archive(now, 'zip', 'nos_config')
        shutil.rmtree('./nos_config/')

if __name__ == '__main__':
    GetNosConfig().get_nos_config()

