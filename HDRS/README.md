# HDS Installer

## requirements
* jdk8
* python3

# How to use

## First to install dependencies
```
sh dependencies.sh
```

## Edit conf.json
**need to set `cluster.hostname` for each node**
**need to specify `jdk.javaHome`**
```json=
{
    "cluster": {
        "hostname": "Brad-HDS-Master",
        "master": "Brad-HDS-Master",
        "slaves": [
            "Brad-HDS-Slave1",
            "Brad-HDS-Slave2"
        ]
    },
    "jdk": {
        "javaHome": "/usr/lib/jvm/jdk1.8.0_231"
    },
    "maven": {
        "installDir": "/home/brad/HDS-DCFS-Install/apache-maven-3.8.4"
    },
    "zookeeper": {
        "installDir": "/home/brad/HDS-DCFS-Install/apache-zookeeper-3.6.2-bin"
    },
    "hadoop": {
        "installDir": "/home/brad/HDS-DCFS-Install/hadoop-3.2.2"
    },
    "hbase": {
        "installDir": "/home/brad/HDS-DCFS-Install/hbase-2.3.4"
    },
    "phoenix": {
        "installDir": "/home/brad/HDS-DCFS-Install/phoenix-hbase-2.3-5.1.2-bin"
    },
    "hdrs": {
        "installDir": "/home/brad/HDS-DCFS-Install/hdrs-1.1.0-without-cdh"
    }
}
```

## Install all
NOTICE: **need to add the generated `conf_files/.bashrc` to `~/.bashrc` on your own**  
NOTICE: **It will compile HDRS for your. If you already have the HDRS package, please place the `hdrs-1.1.0-without-cdh-bin.tar.gz` on `hds-2021/hdrs-assembly/target` to avoid compiling**
```bash=
python3 install_hdrs.py install
```
```bash=
cat conf_files/.bashrc >> ~/.bashrc
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
python3 install_hdrs.py install phoenixqs
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
python3 install_hdrs.py remove phoenixqs
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
