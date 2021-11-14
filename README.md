# HDS-DCFS-Install
## clone project
```
git clone --recursive --depth 1 git@github.com:CW-B-W/HDS-DCFS-Install.git
```

# Install HDRS
See the `HDRS` directory  
**Need to edit `conf.json`**
```
cd HDRS
sh dependencies.sh
python3 install_hdrs.py install
cat conf_files/.bashrc >> ~/.bashrc
```

# Install Python requirements
See the `Py` directory
