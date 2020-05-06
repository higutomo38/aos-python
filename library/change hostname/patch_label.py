# --- import ---
import common
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import csv

ahost = common.args[1]
l = common.blueprint()
token = l[0]
bp_id = l[1]

# Patch Label from CSV (switch, server)
def patch_label():
  with open('hostname_label.csv','r') as f:
    next(f)
    r = csv.reader(f)
    for i in r:
      ep = 'https://' + ahost + '/api/blueprints/{0}/nodes/{1}'.format(bp_id, i[0])
      payload={'label':i[5]}
      requests.patch(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False)

patch_label()
