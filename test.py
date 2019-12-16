from cryptography.fernet import *
from lxml import etree 
import time
from SimpliVityClass import *
from datetime import datetime

if __name__ == "__main__":
    path = './'
    keyfile= path + 'svtinfrastructure.key'
    xmlfile=path + 'svtinfrastructure.xml'
    """ Parse XML File """
    tree = etree.parse(xmlfile)
    u2=(tree.find("user")).text
    p2=(tree.find("password")).text
    ovc=(tree.find("ovc")).text
    mintervall=int((tree.find("monitoringintervall")).text)
    mresolution=(tree.find("resolution")).text
    mrange=(tree.find("timerange")).text
    lfile=(tree.find("logfile")).text
    port=int((tree.find("port")).text)

    """ Read keyfile """
    f = open(keyfile, 'r')
    k2=f.readline()
    f.close()
    key2=k2.encode('ASCII')
    f = Fernet(key2)

    svtuser = f.decrypt(u2.encode('ASCII')).decode('ASCII')
    svtpassword = f.decrypt(p2.encode('ASCII')).decode('ASCII')
    url="https://"+ovc+"/api/"         
    svt = SimpliVity(url)

    while True:
        try:
            #vms = svt.GetVM()['virtual_machines']
            #print(len(vms))
            datastore = svt.GetDataStore()
        except SvtError as e:
                if e.status == 401:
                        try:
                                svt.connect(svtuser,svtpassword)
                        except SvtError as e:
                                print("Failed to open a conection to SimplVity")
                                print(str(e.expression))
                                print(str(e.status))
                                print(str(e.message))
                                print("close SimpliVity connection")
                                exit(-200)
                else:
                        print("Svt Error")
                        print(str(e.expression))
                        print(str(e.status))
                        print(str(e.message))
                        print("close SimpliVity connection")
                        exit(-200)
