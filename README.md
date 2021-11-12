# HDS & DCFS Installer
## clone project
git clone --recursive --depth 1 git@github.com:CW-B-W/HDS-DCFS-Install.git

## requirements
* python3

# How to use

## Install all
```bash=
python3 install_hdrs.py install
```

## Install single module
```bash=
python3 install_hdrs.py install ...
```
e.g.
```bash=
python3 install_hdrs.py install maven
python3 install_hdrs.py install zookeeper
python3 install_hdrs.py install hadoop
python3 install_hdrs.py install hbase
python3 install_hdrs.py install phoenix
python3 install_hdrs.py install hdrs
```

## Remove all
```bash=
python3 install_hdrs.py remove
```

## Remove single module
```bash=
python3 install_hdrs.py remove maven
python3 install_hdrs.py remove zookeeper
python3 install_hdrs.py remove hadoop
python3 install_hdrs.py remove hbase
python3 install_hdrs.py remove phoenix
python3 install_hdrs.py remove hdrs
```

## Clean
### Remove temp files
```bash=
python3 install_hdrs.py clean
```
### Remove temp files & downloaded files
```bash=
python3 install_hdrs.py cleanall
```
