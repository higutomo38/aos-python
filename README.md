# **AOS Python Module**

AOS python modules for demonstration here are packaged as dockerhub repository "higutomo38/aos-python". Dockerhub builds the image automatically after github repo here goes updated.

AOS 3.3.0

## **Installation**

Run the docker repo.

```
docker run --name aos-python -it -w /tmp/aos-python/library higutomo38/aos-python:latest /bin/bash
```

Get latest AOS SDK from Apstra client portal and copy it to the container path "/tmp/aos-python/library"<br>
(Note: Skip this step if you don't use 'post_iba_probe.py')

```
docker cp ./aos-dev-sdk-462.zip aos-python:/tmp/aos-python/library
```

Run python file using AOS server FQDN / IP address, blueprint name and AOS SDK.<br>
```
python get_hostname.py 192.168.1.1 blueprint_name
```
Add aos-dev-sdk for 'post_iba_probe.py'
```
python post_iba_probe.py 192.168.1.1 blueprint_name aos-dev-sdk-462.zip
```

Use single quotation if blueprint name includes blank.<br>
e.g. python get_hostname.py 192.168.1.1 'blue print'

## **Modules**

| Category | Module | Description | NOS |
| --- | --- | --- | --- |
| Blueprint | get_hostname.py | Create new CSV file lists hostnames | All |
|  | get_nos_config.py | Save NOS configuration on local | All |
|  | patch_hostname.py | Change hostnames listed in CSV | All |
|  | patch_label.py | Change labels listed in CSV | All |
|  | patch_deploy_mode_server.py | Change deploy mode | Server |
|  | post_vn_based_server_name.py | Post virtual network based on server hostname. Switch ports go selecting automatically. | All |
| Configlets | post_configlets.py | Samples of configlets with Jinja and Property-set | Junos |
| IBA | post_iba_probe.py | Create all probes without AOS-CLI | Except Junos |

## **Blueprint**
### **Change Hostname (Spine, Leaf and Server)**
First of all you get current hostname list as CSV. 

```
$ python get_hostname.py 192.168.1.1 blueprint_name
```

You can see 'hostname_label.csv' on same directory you run the script.

ex.'hostname_label.csv'<br>
<img src="https://user-images.githubusercontent.com/21299310/75221479-48479700-57e5-11ea-8af9-2b167fc1815d.png" width="640px">

Add new hostnames in column 'new_hostname or label' and save the CSV.

ex.'hostname_label.csv'<br>
<img src="https://user-images.githubusercontent.com/21299310/75225362-cf990880-57ed-11ea-9849-f71f4fea706e.png" width="640px">

```
$ python patch_hostname.py 192.168.1.1 blueprint_name
```

Check 'Physical Diff' tab in 'uncommited' on AOS and then push 'commit'.<br> 


### **Change label (Spine, Leaf and Server)**
The procedure is same as hostname. Add new labels in culumn 'new_hostname or label' and save the CSV.<br> 

```
$ python patch_label.py 192.168.1.1 blueprint_name
```

### **Change deploy mode (Server)**
You can monitor Leaf interfaces up/down facing server without aos agent when turn deploy mode of servers on.<br> 

```
$ python patch_deploy_mode_server.py
```

### **Save NOS configs on local (Spine and Leaf)**
All rendered NOS configs got saved on local. The script create 'nos_config' directory and zip it up.<br> 

```
$ python get_nos_config.py 192.168.1.1 blueprint_name
```

### **Post virtual network based on server hostname**
Switch ports go selecting automatically based server hostname when add virtual network.

```
$ python post_vn_based_server_name.py 192.168.1.1 blueprint_name
AOS Login
ID:
Password:
Virtual Network Name: vn131
VLAN_ID: 131
VNI: 10131
Security Zone: finance
IPv4 Subnet: 10.1.1.0/24
Virtual_Gateway_IPv4: 10.1.1.1
[?] DHCP Service ? (Y/n): y
Enter Server Hostname or "No": evpn-mlag-001-server001
Enter Server Hostname or "No": evpn-mlag-001-server002
Enter Server Hostname or "No": evpn-mlag-001-server003
Enter Server Hostname or "No": no
--- Target Server List: ['evpn-mlag-001-server001', 'evpn-mlag-001-server002', 'evpn-mlag-001-server003']
```
## **Configlets**
### **Sample Configlets and Property-Set for Junos**
```
$ python post_configlets.py 192.168.1.1 blueprint_name
```
You should edit both contents 'vrf name', 'prefix', 'ntp server' and so on after running the script.

## **IBA**
### **Create all probes without AOS-CLI**
We usually use WebUI and command line interface tool AOS-CLI to create custom IBA probe. 

WebUI<br>
・Upload Custom Collector Package<br>
・Install Custom Collector to Agent<br>
AOS-CLI<br>
・Import service registry<br>
・Create probes<br>

This python script execute batch of above using API.

Download latest AOS SDK e.g.'aos-dev-sdk-XXX.zip' from here.<br>
https://portal.apstra.com/downloads/ <br>

Copy the zip into directory same as 'shared.py', 'post_iba_probe.py' and 'Probes'. <br>
Run 'post_iba_probe.py' putting the zip file name behind blueprint.<br>

e.g.<br>
```
python post_iba_probe.py 192.168.1.1 'tomo pod1' aos-dev-sdk-462.zip
AOS Login
ID:admin
Password:
```

All probes are created with temporary input Ex.'Match expected os version by OS family.json' use NOS 'cumulus' and version '3.7.12' as default. You can edit them on WebUI Analytics in BP - Probes - Push Edit - Select processor you want to change.<br>
