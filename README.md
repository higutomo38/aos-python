# **AOS Python Library**

Python library used to interact with Apstra AOS.

## **Installation**

Clone repo into your aos project.

```
git clone https://github.com/higutomo38/aos.git
```

Install Python 3.X on you local. Need some python modules in addition to default.
```
pip install requests urllib3
```

Modify 'common.py' according to your env and save the file.

uname: AOS login username<br>
passw: AOS login password<br>
ahost: AOS IP address or Name<br>
blue_name: Blueprint Name

e.g.<br>
```
#--- entry ---
uname = 'admin'
passw = 'hogefuga'
ahost = 'aos_server.com'
blue_name = 'bp_name'
```

## **Module list**

| Category | Module | Description | NOS |
| --- | --- | --- | --- |
| Blueprint | get_hostname.py | Create new CSV file hostnames listed | All |
|  | patch_hostname.py | Change hostnames listed in CSV | All |
|  | patch_label.py | Change labels listed in CSV | All |
|  | get_nos_config.py | Save all NOS configurations on local | Cumulus, EOS |
| Closed-Loop | configlets_intdown_flap.py | Push ifdown configlets triggered by IBA interface flap anomaly | Cumulus |

## **Blueprint**
### **Change Hostname (Spine, Leaf and Server)**
Before hostnames modified, you need to get current hostname list as CSV. Run 'get_hostname.py' and then you can see 'hostname_label.csv' on same directory you executed the script.

ex.'hostname_label.csv'<br>
<img src="https://user-images.githubusercontent.com/21299310/75221479-48479700-57e5-11ea-8af9-2b167fc1815d.png" width="640px">

Add new hostnames in 'new_hostname or label' row and save the CSV.

ex.'hostname_label.csv'<br>
<img src="https://user-images.githubusercontent.com/21299310/75225362-cf990880-57ed-11ea-9849-f71f4fea706e.png" width="640px">

Run 'patch_hostname.py'.<br> 
Check 'Physical Diff' tab in 'uncommited' on AOS and then push 'commit'.<br> 


### **Change label (Spine, Leaf and Server)**
The procedure is same as hostname. Add new labels in 'new_hostname or label' row and save the CSV.<br> 
Run 'patch_label.py'<br> 

### **Save all NOS configs on local (Spine and Leaf)**
All rendered NOS configuration got saved on local. Create 'nos_config' directory automatically and the configs are in it.<br> 
Run 'get_nos_config.py'<br>

## **Closed-Loop**
### **Push ifdown configlets triggered by IBA interface flap anomaly**

#### **AOS Setting**
1. Set IBA Interface Flapping with raising anomaly on 'device interface flappinng' processor.
2. Create syslog config and turn on 'Forward Anomalies'.

#### **Syslog Server Setting**<br>
1. Install python and libraries as above.
2. Turn on syslog service.<br>
3. Copy three files.<br>
   - common.py
   - configlets.json
   - configlets_intdown_flap.py<br>
     Note: Comment out two lines here if you use Apstra Cloudlab as syslog server.<br>
     ```
     #from requests.packages.urllib3.exceptions import InsecureRequestWarning
     #requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
     ```
4. Set crontab to run 'configlets_intdown_flap.py' periodically. The script search the flap anomaly in syslog file and then push interface down configlets to the node/interface are identical with the log.<br>
   ex. <br>
   ```
   cp /etc/crontab /etc/cron.d/test_cron
   Add new line here.
   * *     * * *   root    for i in `seq 0 20 59`;do (sleep ${i}; python /home/admin/configlets_intdown_flap.py) & done;
   service cron restart
   ```
   
