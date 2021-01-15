import csv
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from shared import AosApi
from shared import LoginBlueprint

token_bp_id_address = LoginBlueprint().blueprint()
token = token_bp_id_address[0]
bp_id = token_bp_id_address[1]
address = token_bp_id_address[2]


class PostVN(object):

    def __init__(self):
        pass

    def sec_zone_dict(self):
        """:input: get security zone.
          Make dict { security_zone_label: security_zone_id }.
        :return: above dict.
        """
        return { sec_zone['vrf_name']:sec_zone['id'] for sec_zone in \
                 AosApi().bp_security_zone_get(token, bp_id, address)['items'].values() }

    def leaf_dict(self):
        """:input: All leafs info from graph query.
          Make dict { leaf_hostname: id }.
            Redundancy group id overwrite the pair.
          Make set { link group label }
        :return: Touple ( dict, set )
        """
        sys_int_link = AosApi().bp_qe_post(token, bp_id, address,
                        "node('system', name='leaf', role='leaf')\
                         .out('hosted_interfaces')\
                         .node('interface', name='int', if_type='ethernet')\
                         .out('link')\
                         .node('link', name='link', role='leaf_l2_server')")
        all_leaf_dict = { node['leaf']['hostname']:node['leaf']['id'] \
                          for node in sys_int_link['items'] }
        all_group_label = set([ node['link']['group_label']
                            for node in sys_int_link['items'] ])
        for node in AosApi().bp_qe_post(token, bp_id, address,
                         "node('redundancy_group', name='rg', rg_type='esi')\
                         .out('composed_of_systems')\
                         .node('system', name='leaf', role='leaf')\
                         ")['items']:
            all_leaf_dict[node['leaf']['hostname']] = node['rg']['id']
        return all_leaf_dict, all_group_label

    def post_vn(self):
        """:input: func 'sec_zone_dict', 'leaf_dict' and local file 'post_vn.csv'.
          Make vn post payload.
        :return :Post virtual networks
        """
        dict_set = PostVN.leaf_dict(self)
        with open('./csv/post_vn.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for line in reader:
                vn_template = {
                    "l3_connectivity": "l3Enabled",
                    "label": line[0],
                    "vn_type": line[1],
                    "vn_id": line[2],
                    "ipv4_subnet": line[4],
                    "virtual_gateway_ipv4": line[5],
                    "dhcp_service": line[6],
                    "security_zone_id": PostVN.sec_zone_dict(self)[line[7]],
                }
                leaf_id_list = list(set([dict_set[0][hostname] \
                                         for hostname in line[8].split(',')]))
                vn_template["bound_to"] = [{"system_id": leaf_id, "vlan_id": int(line[3])} \
                                           for leaf_id in leaf_id_list]
                tag_type_dict = { group_label: line[9] for group_label in dict_set[1] }
                vn_template["default_endpoint_tag_types"] = tag_type_dict
                resp = AosApi().bp_vn_post(token, bp_id, address, vn_template)
                if 'id' in resp.keys(): print (line[0] + ' done')
                else: print (line[0] + ' ' + json.dumps(resp))

if __name__ == '__main__':
    PostVN().post_vn()