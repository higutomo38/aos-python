# **AOS Python Module**

These modules are AOS API Python scripts for demonstration.

AOS 3.2.0

## **Installation**

Clone repo into your aos project.

```
git clone https://github.com/higutomo38/aos.git
```

Install Python 3.X on you local. Need some python modules in addition to default.
```
pip install requests urllib3 openpyxl netaddr
```

Run python file with AOS server FQDN or IP Address and Blueprint Name.<br>

e.g.<br>
```
python get_hostname.py 192.168.1.1 blueprint
AOS Login
ID:admin
Password:
```

## **Module list**

| Category | Module | Description | NOS |
| --- | --- | --- | --- |
| Blueprint | get_hostname.py | Create new CSV file lists hostnames | All |
|  | patch_hostname.py | Change hostnames listed in CSV | All |
|  | patch_label.py | Change labels listed in CSV | All |
|  | get_nos_config.py | Save NOS configuration on local | Cumulus, EOS |
|  | get_ip_sheet.py | Save AOS database sheet tie to device IP | Cumulus, EOS |
| Closed-Loop | configlets_intdown_flap.py | Push interface down configlets triggered by IBA interface flap anomaly | Cumulus |


All modules should be same directory as 'common.py' otherwise you can't login to AOS.

## **Blueprint**
### **Change Hostname (Spine, Leaf and Server)**
First of all you need to get current hostname list as CSV. Run 'get_hostname.py' and then you can see 'hostname_label.csv' on same directory you executed the script.

ex.'hostname_label.csv'<br>
<img src="https://user-images.githubusercontent.com/21299310/75221479-48479700-57e5-11ea-8af9-2b167fc1815d.png" width="640px">

Add new hostnames in column 'new_hostname or label' and save the CSV.

ex.'hostname_label.csv'<br>
<img src="https://user-images.githubusercontent.com/21299310/75225362-cf990880-57ed-11ea-9849-f71f4fea706e.png" width="640px">

Run 'patch_hostname.py'.<br> 
Check 'Physical Diff' tab in 'uncommited' on AOS and then push 'commit'.<br> 


### **Change label (Spine, Leaf and Server)**
The procedure is same as hostname. Add new labels in culumn 'new_hostname or label' and save the CSV.<br> 
Run 'patch_label.py'<br> 

### **Save NOS configs on local (Spine and Leaf)**
All rendered NOS configs got saved on local. The script create 'nos_config' directory automatically and put .conf into it.<br> 
Run 'get_nos_config.py'<br>

### **Save AOS database sheet tie to device IP**
You get AOS database related network device IP as xlsx file.

1. Device
2. Cabling
3. Underlay 
4. Overlay 

Run 'get_ip_sheet.py'<br>

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
 
if your test env is on Apstra Cloudlab<br>
  - ahost='172.16.90.3' in 'common.py'<br>
  - Disable urllib3 in 'common.py' and 'configlets_intdown_flap.py'<br>
     ```
     #from requests.packages.urllib3.exceptions import InsecureRequestWarning
     #requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
     ```

4. Set crontab to run 'configlets_intdown_flap.py' periodically. The script search the flap anomaly in syslog file and then push interface down configlets to the node/interface are identical with the log.<br>
   ex. <br>
   ```
   cp /etc/crontab /etc/cron.d/test_cron
   #/etc/cron.d/test_cron
   #Add new line here.
   * *     * * *   root    for i in `seq 0 20 59`;do (sleep ${i}; python /home/admin/configlets_intdown_flap.py) & done;
   service cron restart
   ```
5. Check 'Logical Diff' tab in 'uncommited' on AOS and then push 'commit'.
