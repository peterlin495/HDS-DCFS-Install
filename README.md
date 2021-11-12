# HDS & DCFS Installer
## clone project
git clone --recursive git@github.com:CW-B-W/HDS-DCFS-Install.git

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
python3 install_hdrs.py install hadoop
python3 install_hdrs.py install hbase
```

## Remove all
```bash=
python3 install_hdrs.py remove
```

## Remove single module
```bash=
python3 install_hdrs.py hadoop
python3 install_hdrs.py hbase
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