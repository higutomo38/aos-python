# --- import ---
import common
import json
import requests

l = common.blueprint()
token = l[0]
bp_id = l[1]
ahost = common.args[1]
probe_summary = ['Power Supply', 'System Memory', 'Counter Errors', 'Interface Flapping', 'Interface Queue Drops', 'Physical Interface', 'SFP', 'MLAG', 'OSPF Sessions', 'Fabric BGP Session', 'Percentage of BUM Packets Over', 'VXLAN Status']

bp_probes_get = common.bp_probes_get(token, bp_id)
bp_iba_widgets_get = common.bp_iba_widgets_get(token, bp_id)

def post_widgets():
    probe_label_id_dict = {i['label']:i['id'] for i in bp_probes_get['items']}
    for i in probe_summary:
        for j in list(probe_label_id_dict):
            if i.lower() in j.lower():
                probe_label_id_dict[i] = probe_label_id_dict[j]
                del probe_label_id_dict[j]
    for i in list(probe_label_id_dict):
        if 'EVPN IBA Telemetry' in i:
            probe_label_id_dict['EVPN'] = probe_label_id_dict[i]
            del probe_label_id_dict[i]
    # print (probe_label_id_dict)
    with open('iba_widgetes.json') as f: json_content = json.loads(f.read())
    for i in probe_label_id_dict.items():
        for j in json_content['items']:
            if i[0].lower() in j['label'].lower():
                j['probe_id'] = i[1]
                post_content = json.dumps(j)
                ep = 'https://' + ahost + '/api/blueprints/{blueprint_id}/iba/widgets'.format(blueprint_id = bp_id)
                resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=post_content, verify=False)

# def post_dashboard():



post_widgets()
# post_dashboard()
