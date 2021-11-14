sudo apt update
# install pip3
sudo apt -y install python3-pip
# install for phoenixdb
sudo apt-get -y install gcc libkrb5-dev
# install for oracleDB
sudo apt -y install alien libaio1
wget -O /tmp/oracle-instantclient-basic-21.4.0.0.0-1.x86_64.rpm https://download.oracle.com/otn_software/linux/instantclient/214000/oracle-instantclient-basic-21.4.0.0.0-1.x86_64.rpm
sudo alien -i /tmp/oracle-instantclient-basic-21.4.0.0.0-1.x86_64.rpm
# install for mssql
sudo apt-get -y install freetds-dev freetds-bin  
sudo apt-get -y install python-dev python-pip
