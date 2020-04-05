# --- import ---
import common
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
import json
import glob

ahost = common.ahost
l = common.blueprint()
token = l[0]
bp_id = l[1]
dir_probe = './iba_probe/'

# Post Probe
def post_probe():
  files = glob.glob(dir_probe + '*')
  for i in files:
    f = open(i)
    cont = f.read()
    f.close()
    ep = 'https://' + ahost + '/api/blueprints/{0}/probes'.format(bp_id)
    resp = requests.post(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=cont, verify=False)
    if resp.status_code == 201: print ('Install ' + i.lstrip(dir_probe))
    else:
      print ('Failed to install ' + i.lstrip(dir_probe))
      sys.exit()

post_probe()
