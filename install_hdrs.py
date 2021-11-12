import sys
import os
import shutil

def check_old_versions():
    pass

def install_maven():
    pass

def install_zookeeper():
    pass

def install_hadoop():
    pass

def install_hbase():
    pass

def install_hdrs():
    pass

def clean():
    if os.path.exists("conf_files"):
        shutil.rmtree("conf_files")

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("Wront argument")
        exit(1)

    if sys.argv[1] == "clean":
        clean()
    elif sys.argv[1] == "install":
        check_old_versions()
        clean()
        os.mkdir("conf_files")
        install_maven()
    else:
        print("Wront argument")
        exit(1)