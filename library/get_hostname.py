# --- import ---
import common
import csv

l = common.blueprint()
token = l[0]
bp_id = l[1]
bp_node_list_system = common.bp_node_list_system(token, bp_id)

# Save Hostname to CSV (switch, server)
def get_hostname():
  with open('hostname_label.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(['id','role','hostname','new_hostname or label'])
    for i in bp_node_list_system.values():
      if i['role'] == 'spine' or i['role'] == 'leaf' or i['system_type'] == 'server':
        writer.writerow([i['id'],i['role'],i['hostname']])

get_hostname()
