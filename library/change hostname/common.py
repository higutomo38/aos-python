### Get common info: Token, BP ID, Node ID and EndPoint
#
# --- import ---
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import getpass
import socket

args = sys.argv

# --- exec ---
# aos login
def login():
  try:
    addr = socket.gethostbyname(args[1])
  except socket.error:
    print ('----- Error:FQDN failure -----')
    sys.exit()
  print('AOS Login')
  uname = input('ID:')
  passw = getpass.getpass()
  ep = 'https://' + args[1] + '/api/user/login'
  payload={"username":uname, "password":passw}
  resp = requests.post(ep, headers={'Content-Type':'application/json'}, data=json.dumps(payload), verify=False)
  # Check response code is 2XX
  if str(resp.status_code)[0] == '2': resp = resp.json()
  else:
    print ('----- Error:FQDN failure -----')
    sys.exit()
  if 'token' in resp: return resp['token']
  else:
    print ('----- Error:Authentication failure -----')
    sys.exit()

# get blueprint id
def blueprint():
  token = login()
  ep = 'https://' + args[1] + '/api/blueprints'
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  for i in resp['items']:
    if i['label'] == args[2]: return token, i['id']
  print ('----- Error:Blueprint name -----')
  sys.exit()

# get node list of system (switch, server)
def bp_node_list_system(token, bp_id):
  ep = 'https://' + args[1] + '/api/blueprints/{0}/nodes?node_type=system'.format(bp_id)
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  return resp["nodes"]

 # get systems
def systems_get(token):
  ep = 'https://' + args[1] + '/api/systems'
  resp = requests.get(ep, headers={'AUTHTOKEN':token, 'Content-Type':'application/json'}, verify=False).json()
  return resp
