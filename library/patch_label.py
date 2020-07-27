import csv
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from common import LoginBlueprint

class PatchLabel(object):

    def __init__(self):
        """
        Import AOS Token, Blueprint ID, AOS Address.
        """
        self.token_bp_id_address = LoginBlueprint().blueprint()

    def patch_label(self):
        """
        Change label of spine, leaf and server by using CSV.
        """
        with open('hostname_label.csv', 'r') as file:
            writer = csv.writer(file)
            next(file)
            rows = csv.reader(file)
            for line in rows:
                requests.patch('https://' + self.token_bp_id_address[2] \
                               + '/api/blueprints/{blueprint_id}/nodes/{node_id}'\
                               .format(blueprint_id = self.token_bp_id_address[1], node_id = line[0]),
                               headers={'AUTHTOKEN': self.token_bp_id_address[0],
                                        'Content-Type': 'application/json'},
                               data=json.dumps({'label': line[4]}), verify=False)

if __name__ == '__main__':
    PatchLabel().patch_label()

