import ast
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys

from common import LoginBlueprint
from common import AosApi

token_bp_id_address = LoginBlueprint().blueprint()
token = token_bp_id_address[0]
bp_id = token_bp_id_address[1]
address = token_bp_id_address[2]


class PostConfigletsIntDown(object):

    def __init__(self):
        pass

    def check_syslog(self):
        """
        Check if there is interface flapping anomary on local '/var/log/syslog'.
        :return: [system_id, interface_number]
        """
        with open('/var/log/syslog', 'r') as f:
            syslogs = f.readlines()
        sys_int_list = []
        for syslog in syslogs:
            if 'if_status_flapping' in syslog:
                for contents in ast.literal_eval(syslog.split('msg=')[1])['alert']['probe_alert']['key_value_pairs']:
                    if contents['key'] == 'system_id':
                        sys_int_list.insert(0, contents['value'].replace('"',''))
                    elif contents['key'] == 'key':
                        sys_int_list.append(contents['value'].replace('"',''))
                return sys_int_list
                sys.exit()

    def post_intdown_configlets(self):
        """
        If there is IBA interface flapping anomaly on 'check_syslog()', shutdown the interface using configlet.
        If configlet 'Cumulus Linkdown' is already installed, stop running this script.
        We should translate system_id to node_id as syslog doesn't include node_id.
        """
        format = {
            "configlet": {
                "display_name": "Cumulus Linkdown",
                "generators": [
                    {
                        "config_style": "cumulus",
                        "section": "system",
                        "section_condition": "",
                        "filename": "",
                        "template_text": "ifdown x --admin-state",
                        "negation_template_text": "ifup x"
                    }
                ]
            },
            "condition": "",
            "label": "Cumulus Linkdown"
        }
        sys_int_list = PostConfigletsIntDown().check_syslog()
        for node in AosApi().bp_node_get_system(token, bp_id, address)['nodes'].values():
            if node['system_id'] == sys_int_list[0]:
                for configlets in AosApi().bp_configlets_get(token, bp_id, address)['items']:
                    if configlets['configlet']['display_name'] == 'Cumulus Linkdown':
                        sys.exit()
                if AosApi().bp_diff_get(token, bp_id, address)['configlet'] == None:
                    format['configlet']['generators'][0]['template_text'] \
                        = format['configlet']['generators'][0]['template_text'].replace('x',sys_int_list[1])
                    format['configlet']['generators'][0]['negation_template_text'] \
                        = format['configlet']['generators'][0]['negation_template_text'].replace('x', sys_int_list[1])
                    format['condition'] = "id in [\"" + node['id'] + "\"]"
                    print (format)
                    requests.post ('https://' + address + '/api/blueprints/' + bp_id + '/configlets',
                                   headers={'AUTHTOKEN':token, 'Content-Type':'application/json'},
                                   data=json.dumps(format), verify=False)
                sys.exit()


if __name__ == '__main__':
    PostConfigletsIntDown().post_intdown_configlets()

