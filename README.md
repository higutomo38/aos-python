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
uname = 'admin'<br>
passw = 'hogefuga'<br>
ahost = 'aos_server.com'<br>
blue_name = 'bp_name'
```

## **Module list**

| Module | Catergory | Description | NOS |
| --- | --- | --- | --- |


### **System Setting**
get_hostname.py
get_nos_config.py
patch_label.py
patch_hostname.py

### **Operation**




