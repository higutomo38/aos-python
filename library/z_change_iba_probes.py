
import json
import glob
import sys

# Probe Categories
Capacity_Planning = ['usage']
Compliance = ['Hostname compliance','Match expected os version by OS family']
Data_Plane = ['ECMP','counter','Counter','Flapping','LAG Imbalance','Analyze round-trip time on servers','Physical interface status','Monitor packet loss on servers','Spine TX-RX Discrepancy','Sustained packet discards','Interface queue drops']
Device_Health = ['memory','restart','Power Supply']
Fault_Tolerance = ['fault tolerance']
Layer1 = ['QSFP','SFP']
Layer2 = ['MLAG','STP']
Layer3 = ['default gateway','BGP','OSPF','External routes']
Maintenance = ['Drain traffic anomaly']
Multicast = ['PIM','Multicast','Anycast','VRFs missing RPs']
Overlay = ['EVPN','VTEP','VxLAN','vtep','VXLAN']
Security = ['ACL','802.1x']
Traffic_Patterns = ['Bandwidth utilization history', 'East\/West']
Virtual_Infra = ['Virtual', 'Hypervisor']
dict_probes = {'Capacity_Planning':Capacity_Planning,'Compliance':Compliance,'Data_Plane':Data_Plane,'Device_Health':Device_Health,'Fault_Tolerance ':Fault_Tolerance,'Layer1':Layer1,'Layer2':Layer2,'Layer3':Layer3,'Multicast':Multicast,'Overlay':Overlay,'Security':Security,'Traffic_Patterns':Traffic_Patterns,'Virtual_Infra':Virtual_Infra}
vendor = ['Arista','arista','Cisco','cisco','Cumulus','cumulus','Juniper','juniper']

def rename_probe():
    probe_files = glob.glob('./probes/*.json')
    for probe_path in probe_files:
        probe_name = probe_path.replace('./probes/', '').replace('.json', '')
        for i in dict_probes.items():
            for j in i[1]:
                if j in probe_name:
                    new_probe_name = i[0] + ' - ' + probe_name
                else: continue
                if 'anomalies' in new_probe_name:
                    new_probe_name = new_probe_name.replace('anomalies','')
                elif 'anomaly' in new_probe_name:
                    new_probe_name = new_probe_name.replace('anomaly','')
                elif 'Anomalies' in new_probe_name:
                    new_probe_name = new_probe_name.replace('Anomalies','')
                for k in vendor:
                    if k in new_probe_name:
                        new_probe_name = new_probe_name.replace(k,'')
                with open(probe_path) as f: json_content = json.loads(f.read())
                json_content['label'] = new_probe_name
                json_content = json.dumps(json_content)
                with open(probe_path, mode='w') as f: f.write(json_content)

def probe_default_disable():
    probe_files = glob.glob('./probes/*.json')
    for i in probe_files:
        with open(i) as f: json_content = json.loads(f.read())
        if 'disabled' in json_content.keys():
            print ('\'disabled\' is exist')
            sys.exit()
        else:
            json_content['disabled'] = 'true'
            json_content = json.dumps(json_content)
            json_content = json_content.replace("\"disabled\": \"true\"", "\"disabled\": true")
        with open(i, mode='w') as f: f.write(json_content)

rename_probe()
probe_default_disable()
