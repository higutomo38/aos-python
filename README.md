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
| Blueprint | get_hostname.py | Create new CSV file hostname listed | All |
|  | patch_hostname.py |  | All |
|  | patch_label.py |  | All |
|  | get_nos_config.py |  | Cumulus, EOS |
| Closed-Loop | configlets_linkdown_linkflap.py |  | Cumulus |

### **Blueprint**


hostname_label.csv

### **Operation**




