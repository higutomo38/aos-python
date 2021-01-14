from glob import glob
import json
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from shared import LoginBlueprint

token_bp_id_address = LoginBlueprint().blueprint()
token = token_bp_id_address[0]
bp_id = token_bp_id_address[1]
address = token_bp_id_address[2]

token_bp_id_address = LoginBlueprint()

class PostConfiglets(object):

    def __init__(self):
        pass

    def post_property_sets(self):
        """
        Read json contents from directory 'property_set'.
        Post property_set to global catalog.
        """
        for file in glob('property_set/*.json'):
            with open(file, 'r') as f:
                requests.post('https://' + address + '/api/property-sets',
                              headers = {'AUTHTOKEN': token,
                                         'Content-Type': 'application/json'},
                              data = f.read(), verify=False)

    def post_configlets(self):
        """
        Get filename, contents from directory 'configlets'.
        Make configlet template text.
        Post configlet to global catalog.
        """
        for file in glob('configlets/*.json'):
            with open(file, 'r') as f:
                requests.post('https://' + address + '/api/design/configlets',
                              headers = {'AUTHTOKEN': token,
                                         'Content-Type': 'application/json'},
                              verify=False,
                              data = json.dumps(
                                       {
                                         "display_name": os.path.split(file)[1].rstrip('.json'),
                                         "generators": [
                                         {
                                            "config_style": "junos",
                                            "section": "system",
                                            "template_text": f.read(),
                                            "negation_template_text": "",
                                            "filename": ""
                                         }
                                         ],
                                         "ref_archs": [
                                            "two_stage_l3clos"
                                         ]}))

if __name__ == '__main__':
    PostConfiglets().post_property_sets()
    PostConfiglets().post_configlets()

