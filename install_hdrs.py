import sys
import os
import shutil
import subprocess
import json
from pathlib import Path

def check_old_versions():
    pass

''' >>>>>>>>>>>>>>> Utils >>>>>>>>>>>>>>> '''
def wget_file(url, dst):
    subprocess.run(['wget', '-O', dst, url])

def tar_xf_file(file, dir):
    subprocess.run(['tar', '-xf', file, '-C', dir])

def cp_dir(src, dst):
    subprocess.run(['cp', '-r', src, dst])

def add_to_bashrc(bashrc_dict):
    with open('conf_files/.bashrc', 'a') as wf:
        for k in bashrc_dict:
            wf.write("export %s=%s\n" % (k, bashrc_dict[k]))
        wf.write('\n')

conf_dict = None
def get_conf(cls, key):
    global conf_dict
    if conf_dict is None:
        with open('conf.json', 'r') as rf:
            conf_dict = json.load(rf)
        conf_dict['cluster']['slave_first'] = conf_dict['cluster']['slaves'][0]
        conf_dict['cluster']['slaves_str_comma'] = ','.join(conf_dict['cluster']['slaves'])
        conf_dict['cluster']['slaves_str_lines'] = '\n'.join(conf_dict['cluster']['slaves'])
        conf_dict['cluster']['servers_str_comma'] = conf_dict['cluster']['master'] + ',' + conf_dict['cluster']['slaves_str_comma']
    return conf_dict[cls][key]

stub_dict = None
def get_stub(stub_cls, key):
    global stub_dict
    if stub_dict is None:
        with open('stub.json', 'r') as rf:
            stub_dict = json.load(rf)
    return stub_dict[stub_cls][key]

def replace_stub_str(stub_cls, str):
    global stub_dict
    if stub_dict is None:
        with open('stub.json', 'r') as rf:
            stub_dict = json.load(rf)
    for key in stub_dict[stub_cls]:
        str = str.replace(stub_dict[stub_cls][key], get_conf(stub_cls, key))
    return str

def replace_stub_file(stub_cls, filepath):
    str = None
    with open(filepath, 'r') as rf:
        str = rf.read()
    str = replace_stub_str(stub_cls, str)
    with open(filepath, 'w') as wf:
        wf.write(str)

def replace_stub_dir(stub_cls, rootdir):
    for root, subdirs, files in os.walk(rootdir):
        for file in files:
            replace_stub_file(stub_cls, root+'/'+file)

def replace_bashrc(bashrc_path):
    with open(bashrc_path, 'r') as rf:
        bashrc_dict = json.load(rf)
        for k in bashrc_dict:
            bashrc_dict[k] = replace_stub_str('maven', bashrc_dict[k])
    return bashrc_dict
''' <<<<<<<<<<<<<<< Utils <<<<<<<<<<<<<<< '''


''' >>>>>>>>>>>>>>> maven >>>>>>>>>>>>>>> '''
def replace_maven_stub():
    add_to_bashrc(replace_bashrc('conf_files_template/apache-maven-3.8.3/bashrc.json'))

def install_maven():
    ins_path = get_conf('maven', 'installDir')
    if os.path.exists(ins_path):
        print("Maven has been installed on `%s` before. Skipping." % ins_path)
        return
    url = 'https://dlcdn.apache.org/maven/maven-3/3.8.3/binaries/apache-maven-3.8.3-bin.tar.gz'
    tar_path = 'downloads/apache-maven-3.8.3-bin.tar.gz'
    if not os.path.exists(tar_path):
        wget_file(url, tar_path)
    ex_path = Path(ins_path).parent.absolute()
    tar_xf_file(tar_path, ex_path)
    replace_maven_stub()

def remove_maven():
    ins_path = get_conf('maven', 'installDir')
    if os.path.exists(ins_path):
        print("Removing Maven...")
        shutil.rmtree(ins_path)
        print("Maven removed")
''' <<<<<<<<<<<<<<< maven <<<<<<<<<<<<<<< '''


''' >>>>>>>>>>>>>>> zookeeper >>>>>>>>>>>>>>> '''
def replace_zk_zoocfg(filepath):
    str = None
    with open(filepath, 'r') as rf:
        str = rf.read()
    master = get_conf("cluster", "master")
    slaves = get_conf("cluster", "slaves")
    server_list = 'server.%i=%s:2888:3888\n' % (1, master)
    idx = 2
    for slave in slaves:
        server_list += 'server.%i=%s:2888:3888\n' % (idx, slave)
        idx += 1
    str = str.replace("__ZK_SERVERS__", server_list)
    str = replace_stub_str("zookeeper", str)
    with open(filepath, 'w') as wf:
        wf.write(str)

def replace_zk_myid(filepath):
    myid = None
    hostname = get_conf("cluster", "hostname")
    master = get_conf("cluster", "master")
    if hostname == master:
        myid = 1
    else:
        slaves = get_conf("cluster", "slaves")
        for (i, slave) in enumerate(slaves):
            if slave == hostname:
                myid = i+2
    if myid == None:
        print("Cannot match hostname to any master/slaves. Please check your `cluster` in conf.json")
        exit(1)
    with open(filepath, 'w') as wf:
        wf.write(str(myid))

def replace_zk_stub():
    conf_prefix = 'conf_files/apache-zookeeper-3.6.2-bin'
    replace_zk_zoocfg(conf_prefix + '/conf/zoo.cfg')
    replace_zk_myid(conf_prefix + '/tmp/myid')
    add_to_bashrc(replace_bashrc('conf_files_template/apache-zookeeper-3.6.2-bin/bashrc.json'))

def install_zookeeper():
    ins_path = get_conf('zookeeper', 'installDir')
    if os.path.exists(ins_path):
        print("Zookeeper has been installed on `%s` before. Skipping." % ins_path)
        return
    cp_dir('conf_files_template/apache-zookeeper-3.6.2-bin', 'conf_files/apache-zookeeper-3.6.2-bin')
    os.remove('conf_files/apache-zookeeper-3.6.2-bin/bashrc.json')
    url = 'https://archive.apache.org/dist/zookeeper/zookeeper-3.6.2/apache-zookeeper-3.6.2-bin.tar.gz'
    tar_path = 'downloads/apache-zookeeper-3.6.2-bin.tar.gz'
    if not os.path.exists(tar_path):
        wget_file(url, tar_path)
    ex_path = Path(ins_path).parent.absolute()
    tar_xf_file(tar_path, ex_path)
    replace_zk_stub()
    cp_dir('conf_files/apache-zookeeper-3.6.2-bin', ex_path)

def remove_zookeeper():
    ins_path = get_conf('zookeeper', 'installDir')
    if os.path.exists(ins_path):
        print("Removing Zookeeper...")
        shutil.rmtree(ins_path)
        print("Zookeeper removed")
''' <<<<<<<<<<<<<<< zookeeper <<<<<<<<<<<<<<< '''


''' >>>>>>>>>>>>>>> hadoop >>>>>>>>>>>>>>> '''

def replace_hadoop_stub():
    replace_stub_dir("cluster", "conf_files/hadoop-3.2.2")
    replace_stub_dir("jdk", "conf_files/hadoop-3.2.2")
    replace_stub_dir("hadoop", "conf_files/hadoop-3.2.2")
    replace_stub_dir("hbase", "conf_files/hadoop-3.2.2")
    replace_stub_dir("hdrs", "conf_files/hadoop-3.2.2")
    add_to_bashrc(replace_bashrc('conf_files_template/hadoop-3.2.2/bashrc.json'))
    pass
def install_hadoop():
    ins_path = get_conf('hadoop', 'installDir')
    if os.path.exists(ins_path):
        print("Hadoop has been installed on `%s` before. Skipping." % ins_path)
        return
    cp_dir('conf_files_template/hadoop-3.2.2', 'conf_files/hadoop-3.2.2')
    os.remove('conf_files/hadoop-3.2.2/bashrc.json')
    url = 'https://archive.apache.org/dist/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz'
    tar_path = 'downloads/hadoop-3.2.2.tar.gz'
    if not os.path.exists(tar_path):
        wget_file(url, tar_path)
    ex_path = Path(ins_path).parent.absolute()
    tar_xf_file(tar_path, ex_path)
    replace_hadoop_stub()
    cp_dir('conf_files/hadoop-3.2.2', ex_path)

def remove_hadoop():
    ins_path = get_conf('hadoop', 'installDir')
    if os.path.exists(ins_path):
        print("Removing Hadoop...")
        shutil.rmtree(ins_path)
        print("Hadoop removed")
''' <<<<<<<<<<<<<<< hadoop <<<<<<<<<<<<<<< '''


''' >>>>>>>>>>>>>>> hbase >>>>>>>>>>>>>>> '''
def install_hbase():
    pass
''' <<<<<<<<<<<<<<< hbase <<<<<<<<<<<<<<< '''


''' >>>>>>>>>>>>>>> phoenix >>>>>>>>>>>>>>> '''
def install_phoenix():
    pass
''' <<<<<<<<<<<<<<< phoenix <<<<<<<<<<<<<<< '''


''' >>>>>>>>>>>>>>> hdrs >>>>>>>>>>>>>>> '''
def install_hdrs():
    pass
''' <<<<<<<<<<<<<<< hdrs <<<<<<<<<<<<<<< '''

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Wrong argument')
        exit(1)

    if sys.argv[1] == 'clean':
        if os.path.exists('conf_files'):
            shutil.rmtree('conf_files')
    elif sys.argv[1] == 'cleanall':
        if os.path.exists('conf_files'):
            shutil.rmtree('conf_files')
        if os.path.exists('downloads'):
            shutil.rmtree('downloads')
    elif sys.argv[1] == 'install':
        check_old_versions()
        if os.path.exists('conf_files'):
            shutil.rmtree('conf_files')
        os.mkdir('conf_files')
        if not os.path.exists('downloads'):
            os.mkdir('downloads')
        if len(sys.argv) == 2:
            yes = input("Sure to install all? (Y/n)") == 'Y'
            if yes:
                install_maven()
                install_zookeeper()
                install_hadoop()
            else:
                print("Aborted")
        else:
            cls_name = "install_" + sys.argv[2]
            if cls_name in globals():
                globals()[cls_name]()
            else:
                print("Cannot find function " + cls_name)
    elif sys.argv[1] == 'remove':
        if len(sys.argv) == 2:
            yes = input("Sure to remove all? (Y/n)") == 'Y'
            if yes:
                remove_maven()
                remove_zookeeper()
                remove_hadoop()
            else:
                print("Aborted")
        else:
            cls_name = "remove_" + sys.argv[2]
            if cls_name in globals():
                globals()[cls_name]()
            else:
                print("Cannot find function " + cls_name)
    else:
        print('Wrong argument')
        exit(1)