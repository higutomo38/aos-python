# --- import ---
import common
import csv

l = common.blueprint()
token = l[0]
bp_id = l[1]
bp_node_get_system = common.bp_node_get_system(token, bp_id)
systems_get = common.systems_get(token)

# Save Hostname to CSV (switch, server)
def get_hostname():
    d = {}
    with open('hostname_label.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['ID','Role','System_ID','Management_IP','Hostname','New Hostname or Label'])
        for i in systems_get['items']:
            if i['facts']['hw_model'] != '':d[i['device_key']] = i['facts']['mgmt_ipaddr']
        for i in bp_node_get_system['nodes'].values():
            if i['role'] == 'spine' or i['role'] == 'leaf':
                for j in d:
                    if j == i['system_id']:writer.writerow([i['id'],i['role'],i['system_id'],d[j],i['hostname']])
            elif i['system_type'] == 'server':writer.writerow([i['id'],i['role'],i['system_id'],'',i['hostname']])

get_hostname()
