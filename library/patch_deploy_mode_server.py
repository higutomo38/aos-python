# --- import ---
import common
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import sys

ahost = common.args[1]
l = common.blueprint()
token = l[0]
bp_id = l[1]
bp_qe_post_system_systemtype = common.bp_qe_post_system_systemtype(token, bp_id)
deploy_mode = common.deploy_mode

# Get node id list (server) and patch deploy mode
def patch_deploy_mode():
  # Create payload
  input_mode = input('deploy_mode:')
  if input_mode in deploy_mode:
    payload = {'nodes': {}}
    for i in bp_qe_post_system_systemtype['items']:
      payload['nodes'][i['system']['id']] = {'deploy_mode':input_mode}
  else:
    print ('Error: Wrong deploy mode')
    sys.exit()
  # Patch deploy mode
  ep = 'https://' + ahost + '/api/blueprints/{blueprint_id}'.format(blueprint_id = bp_id)
  requests.patch(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, data=json.dumps(payload), verify=False)

patch_deploy_mode()
