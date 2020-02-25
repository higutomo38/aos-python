# **AOS Python Modules**

Python modules used to interact with Apstra AOS.

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
--- entry ---<br>
uname = 'admin'
passw = 'hogefuga'
ahost = 'aos_server.com'
blue_name = 'bp_name'
```

## **Module list**

| Category | Module | Description | NOS |
| --- | --- | --- | --- |
| Blueprint | get_hostname.py | Create new CSV file hostnames listed | All |
|  | patch_hostname.py | Change all hostnames listed in CSV | All |
|  | patch_label.py | Change all labels listed in CSV | All |
|  | get_nos_config.py | Save all NOS configurations on local | Cumulus, EOS |
| Closed-Loop | configlets_linkdown_linkflap.py | Push ifdown configlets triggered by linkflap IBA anomaly | Cumulus |

## **Blueprint**
### **Change all Hostnames (Spine, Leaf and server)**
Before hostnames modified, you need to get current hostname list as CSV. Run 'get_hostname.py' and then you can see 'hostname_label.csv' on same directory you executed the script.

ex.'hostname_label.csv'<br>
<img src="https://user-images.githubusercontent.com/21299310/75221479-48479700-57e5-11ea-8af9-2b167fc1815d.png" width="640px">

Add new hostnames in 'new_hostname or label' row and save the CSV.

ex.'hostname_label.csv'<br>
<img src="https://user-images.githubusercontent.com/21299310/75225362-cf990880-57ed-11ea-9849-f71f4fea706e.png" width="640px">

Run 'patch_hostname.py'. 
Check 'Physical Diff' tab in 'uncommited' on AOS and then push 'commit'.


### **Change all labels (Spine, Leaf and server)**



## **Closed-Loop**




