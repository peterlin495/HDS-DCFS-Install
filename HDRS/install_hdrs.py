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
            wf.write('export %s=%s\n' % (k, bashrc_dict[k]))
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

def replace_stub_str(str):
    global stub_dict
    if stub_dict is None:
        with open('stub.json', 'r') as rf:
            stub_dict = json.load(rf)
    for stub_cls in stub_dict:
        for key in stub_dict[stub_cls]:
            str = str.replace(stub_dict[stub_cls][key], get_conf(stub_cls, key))
    return str

def replace_stub_file(filepath):
    str = None
    with open(filepath, 'r') as rf:
        str = rf.read()
    str = replace_stub_str(str)
    with open(filepath, 'w') as wf:
        wf.write(str)

def replace_stub_dir(rootdir):
    for root, subdirs, files in os.walk(rootdir):
        for file in files:
            replace_stub_file(root+'/'+file)

def replace_bashrc(bashrc_path):
    with open(bashrc_path, 'r') as rf:
        bashrc_dict = json.load(rf)
        for k in bashrc_dict:
            bashrc_dict[k] = replace_stub_str(bashrc_dict[k])
    return bashrc_dict
''' <<<<<<<<<<<<<<< Utils <<<<<<<<<<<<<<< '''


''' >>>>>>>>>>>>>>> maven >>>>>>>>>>>>>>> '''
def replace_maven_stub():
    add_to_bashrc(replace_bashrc('conf_files_template/apache-maven-3.8.6/bashrc.json'))

def install_maven():
    print('Installing Maven')
    ins_path = get_conf('maven', 'installDir')
    if os.path.exists(ins_path):
        print('Maven has been installed on `%s` before. Skipping.' % ins_path)
        return
    ex_path = str(Path(ins_path).parent.absolute())
    dir_name = Path(ins_path).name
    os.makedirs(ex_path, exist_ok=True)
    url = 'https://dlcdn.apache.org/maven/maven-3/3.8.6/binaries/apache-maven-3.8.6-bin.tar.gz'
    tar_path = 'downloads/apache-maven-3.8.6-bin.tar.gz'
    if not os.path.exists(tar_path):
        wget_file(url, tar_path)
    tar_xf_file(tar_path, ex_path)
    replace_maven_stub()
    os.rename(ex_path+'/apache-maven-3.8.6', ex_path+'/'+dir_name)

def remove_maven():
    print('Removing Maven...')
    ins_path = get_conf('maven', 'installDir')
    if os.path.exists(ins_path):
        shutil.rmtree(ins_path)
    print('Maven removed')
''' <<<<<<<<<<<<<<< maven <<<<<<<<<<<<<<< '''


''' >>>>>>>>>>>>>>> zookeeper >>>>>>>>>>>>>>> '''
def replace_zk_zoocfg(filepath):
    str = None
    with open(filepath, 'r') as rf:
        str = rf.read()
    master = get_conf('cluster', 'master')
    slaves = get_conf('cluster', 'slaves')
    server_list = 'server.%i=%s:2888:3888\n' % (1, master)
    idx = 2
    for slave in slaves:
        server_list += 'server.%i=%s:2888:3888\n' % (idx, slave)
        idx += 1
    str = str.replace('__ZK_SERVERS__', server_list)
    str = replace_stub_str(str)
    with open(filepath, 'w') as wf:
        wf.write(str)

def replace_zk_myid(filepath):
    myid = None
    hostname = get_conf('cluster', 'hostname')
    master = get_conf('cluster', 'master')
    if hostname == master:
        myid = 1
    else:
        slaves = get_conf('cluster', 'slaves')
        for (i, slave) in enumerate(slaves):
            if slave == hostname:
                myid = i+2
    if myid == None:
        print('Cannot match hostname to any master/slaves. Please check your `cluster` in conf.json')
        exit(1)
    with open(filepath, 'w') as wf:
        wf.write(str(myid))

def replace_zk_stub():
    conf_prefix = 'conf_files/apache-zookeeper-3.6.2-bin'
    replace_zk_zoocfg(conf_prefix + '/conf/zoo.cfg')
    replace_zk_myid(conf_prefix + '/data/myid')
    add_to_bashrc(replace_bashrc('conf_files_template/apache-zookeeper-3.6.2-bin/bashrc.json'))

def install_zookeeper():
    print('Installing Zookeeper')
    ins_path = get_conf('zookeeper', 'installDir')
    if os.path.exists(ins_path):
        print('Zookeeper has been installed on `%s` before. Skipping.' % ins_path)
        return
    cp_dir('conf_files_template/apache-zookeeper-3.6.2-bin', 'conf_files/apache-zookeeper-3.6.2-bin')
    os.remove('conf_files/apache-zookeeper-3.6.2-bin/bashrc.json')
    ex_path = str(Path(ins_path).parent.absolute())
    dir_name = Path(ins_path).name
    os.makedirs(ex_path, exist_ok=True)
    url = 'https://archive.apache.org/dist/zookeeper/zookeeper-3.6.2/apache-zookeeper-3.6.2-bin.tar.gz'
    tar_path = 'downloads/apache-zookeeper-3.6.2-bin.tar.gz'
    if not os.path.exists(tar_path):
        wget_file(url, tar_path)
    tar_xf_file(tar_path, ex_path)
    replace_zk_stub()
    cp_dir('conf_files/apache-zookeeper-3.6.2-bin', ex_path)
    os.rename(ex_path+'/apache-zookeeper-3.6.2-bin', ex_path+'/'+dir_name)

def remove_zookeeper():
    print('Removing Zookeeper...')
    ins_path = get_conf('zookeeper', 'installDir')
    if os.path.exists(ins_path):
        shutil.rmtree(ins_path)
    print('Zookeeper removed')
''' <<<<<<<<<<<<<<< zookeeper <<<<<<<<<<<<<<< '''


''' >>>>>>>>>>>>>>> hadoop >>>>>>>>>>>>>>> '''
def replace_hadoop_stub():
    replace_stub_dir('conf_files/hadoop-3.2.2')
    add_to_bashrc(replace_bashrc('conf_files_template/hadoop-3.2.2/bashrc.json'))

def install_hadoop():
    print('Installing Hadoop')
    ins_path = get_conf('hadoop', 'installDir')
    if os.path.exists(ins_path):
        print('Hadoop has been installed on `%s` before. Skipping.' % ins_path)
        return
    cp_dir('conf_files_template/hadoop-3.2.2', 'conf_files/hadoop-3.2.2')
    os.remove('conf_files/hadoop-3.2.2/bashrc.json')
    ex_path = str(Path(ins_path).parent.absolute())
    dir_name = Path(ins_path).name
    os.makedirs(ex_path, exist_ok=True)
    url = 'https://archive.apache.org/dist/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz'
    tar_path = 'downloads/hadoop-3.2.2.tar.gz'
    if not os.path.exists(tar_path):
        wget_file(url, tar_path)
    tar_xf_file(tar_path, ex_path)
    replace_hadoop_stub()
    cp_dir('conf_files/hadoop-3.2.2', ex_path)
    os.rename(ex_path+'/hadoop-3.2.2', ex_path+'/'+dir_name)

def remove_hadoop():
    print('Removing Hadoop...')
    ins_path = get_conf('hadoop', 'installDir')
    if os.path.exists(ins_path):
        shutil.rmtree(ins_path)
    print('Hadoop removed')
''' <<<<<<<<<<<<<<< hadoop <<<<<<<<<<<<<<< '''


''' >>>>>>>>>>>>>>> hbase >>>>>>>>>>>>>>> '''
def replace_hbase_stub():
    replace_stub_dir('conf_files/hbase-2.3.4')
    if get_conf('cluster', 'hostname') == get_conf('cluster', 'master'):
        os.rename('conf_files/hbase-2.3.4/conf/hbase-site-master.xml', 'conf_files/hbase-2.3.4/conf/hbase-site.xml')
    else:
        os.rename('conf_files/hbase-2.3.4/conf/hbase-site-slave.xml', 'conf_files/hbase-2.3.4/conf/hbase-site.xml')
    add_to_bashrc(replace_bashrc('conf_files_template/hbase-2.3.4/bashrc.json'))

def install_hbase():
    print('Installing HBase')
    ins_path = get_conf('hbase', 'installDir')
    if os.path.exists(ins_path):
        print('HBase has been installed on `%s` before. Skipping.' % ins_path)
        return
    cp_dir('conf_files_template/hbase-2.3.4', 'conf_files/hbase-2.3.4')
    os.remove('conf_files/hbase-2.3.4/bashrc.json')
    ex_path = str(Path(ins_path).parent.absolute())
    dir_name = Path(ins_path).name
    os.makedirs(ex_path, exist_ok=True)
    url = 'https://archive.apache.org/dist/hbase/2.3.4/hbase-2.3.4-bin.tar.gz'
    tar_path = 'downloads/hbase-2.3.4-bin.tar.gz'
    if not os.path.exists(tar_path):
        wget_file(url, tar_path)
    tar_xf_file(tar_path, ex_path)
    replace_hbase_stub()
    cp_dir('conf_files/hbase-2.3.4', ex_path)
    os.rename(ex_path+'/hbase-2.3.4', ex_path+'/'+dir_name)

def remove_hbase():
    print('Removing HBase...')
    ins_path = get_conf('hbase', 'installDir')
    if os.path.exists(ins_path):
        shutil.rmtree(ins_path)
    print('HBase removed')
''' <<<<<<<<<<<<<<< hbase <<<<<<<<<<<<<<< '''


''' >>>>>>>>>>>>>>> phoenix >>>>>>>>>>>>>>> '''
def install_phoenix():
    print('Installing Phoenix')
    ins_path = get_conf('phoenix', 'installDir')
    if os.path.exists(ins_path):
        print('Phoenix has been installed on `%s` before. Skipping.' % ins_path)
        return
    ex_path = str(Path(ins_path).parent.absolute())
    dir_name = Path(ins_path).name
    os.makedirs(ex_path, exist_ok=True)
    url = 'https://dlcdn.apache.org/phoenix/phoenix-5.1.2/phoenix-hbase-2.3-5.1.2-bin.tar.gz'
    tar_path = 'downloads/phoenix-hbase-2.3-5.1.2-bin.tar.gz'
    if not os.path.exists(tar_path):
        wget_file(url, tar_path)
    tar_xf_file(tar_path, ex_path)
    add_to_bashrc(replace_bashrc('conf_files_template/phoenix-hbase-2.3-5.1.2-bin/bashrc.json'))
    os.rename(ex_path+'/phoenix-hbase-2.3-5.1.2-bin', ex_path+'/'+dir_name)
    shutil.copyfile(
        get_conf('phoenix', 'installDir')+'/phoenix-server-hbase-2.3-5.1.2.jar', 
        get_conf('hbase', 'installDir')+'/lib'+'/phoenix-server-hbase-2.3-5.1.2.jar'
    )

def remove_phoenix():
    print('Removing Phoenix...')
    ins_path = get_conf('phoenix', 'installDir')
    if os.path.exists(ins_path):
        shutil.rmtree(ins_path)
    jar_path = get_conf('hbase', 'installDir')+'/lib'+'/phoenix-server-hbase-2.3-5.1.2.jar'
    if os.path.exists(jar_path):
        os.remove(jar_path)
    print('Phoenix removed')
''' <<<<<<<<<<<<<<< phoenix <<<<<<<<<<<<<<< '''


''' >>>>>>>>>>>>>>> hdrs >>>>>>>>>>>>>>> '''
def install_hdrs():
    print('Installing HDRS')
    ins_path = get_conf('hdrs', 'installDir')
    tar_path = '../hds-2021/hdrs-assembly/target/hdrs-1.1.0-without-cdh-bin.tar.gz'
    if not os.path.exists(tar_path):
        # `mvn clean package` to compile hdrs
        print('Compiling HDRS')
        subprocess.run([get_conf('maven', 'installDir')+'/bin/mvn', 'clean', 'package'], cwd='../hds-2021')
    ex_path = str(Path(ins_path).parent.absolute())
    dir_name = Path(ins_path).name
    os.makedirs(ex_path, exist_ok=True)
    tar_xf_file(tar_path, ex_path)
    os.rename(ex_path+'/hdrs-1.1.0-without-cdh', ex_path+'/'+dir_name)

def remove_hdrs():
    print('Removing HDRS...')
    ins_path = get_conf('hdrs', 'installDir')
    if os.path.exists(ins_path):
        shutil.rmtree(ins_path)
    print('HDRS removed')
''' <<<<<<<<<<<<<<< hdrs <<<<<<<<<<<<<<< '''


''' >>>>>>>>>>>>>>> PhoenixQS >>>>>>>>>>>>>>> '''
def install_phoenixqs():
    print('Installing PhoenixQueryServer')
    ins_path = get_conf('phoenixqs', 'installDir')
    if os.path.exists(ins_path):
        print('PhoenixQueryServer has been installed on `%s` before. Skipping.' % ins_path)
        return
    ex_path = str(Path(ins_path).parent.absolute())
    dir_name = Path(ins_path).name
    os.makedirs(ex_path, exist_ok=True)
    url = 'https://dlcdn.apache.org/phoenix/phoenix-queryserver-6.0.0/phoenix-queryserver-6.0.0-bin.tar.gz'
    tar_path = 'downloads/phoenix-queryserver-6.0.0-bin.tar.gz'
    if not os.path.exists(tar_path):
        wget_file(url, tar_path)
    tar_xf_file(tar_path, ex_path)
    add_to_bashrc(replace_bashrc('conf_files_template/phoenix-queryserver-6.0.0/bashrc.json'))
    os.rename(ex_path+'/phoenix-queryserver-6.0.0', ex_path+'/'+dir_name)
    shutil.copyfile(
        get_conf('phoenix', 'installDir')+'/phoenix-client-hbase-2.3-5.1.2.jar', 
        get_conf('phoenixqs', 'installDir')+'/phoenix-client-hbase-2.3-5.1.2.jar'
    )

def remove_phoenixqs():
    print('Removing PhoenixQueryServer...')
    ins_path = get_conf('phoenixqs', 'installDir')
    if os.path.exists(ins_path):
        shutil.rmtree(ins_path)
    print('PhoenixQueryServer removed')
''' <<<<<<<<<<<<<<< PhoenixQS <<<<<<<<<<<<<<< '''

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
            yes = input('Sure to install all? (Y/n)') == 'Y'
            if yes:
                install_maven()
                install_zookeeper()
                install_hadoop()
                install_hbase()
                install_phoenix()
                install_hdrs()
                install_phoenixqs()
            else:
                print('Aborted')
        else:
            cls_name = 'install_' + sys.argv[2]
            if cls_name in globals():
                globals()[cls_name]()
            else:
                print('Cannot find function ' + cls_name)
    elif sys.argv[1] == 'remove':
        if len(sys.argv) == 2:
            yes = input('Sure to remove all? (Y/n)') == 'Y'
            if yes:
                remove_maven()
                remove_zookeeper()
                remove_hadoop()
                remove_hbase()
                remove_phoenix()
                remove_hdrs()
                remove_phoenixqs()
            else:
                print('Aborted')
        else:
            cls_name = 'remove_' + sys.argv[2]
            if cls_name in globals():
                globals()[cls_name]()
            else:
                print('Cannot find function ' + cls_name)
    else:
        print('Wrong argument')
        exit(1)
