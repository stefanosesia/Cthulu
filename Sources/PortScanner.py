import threading
import socket
from Sources.PortList import *

openPorts = []


def portScanThread(target, port):
    global openPorts
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)#
    try:
        con = s.connect((target,port))
        openPorts.append(port)
        con.close()
    except:
        pass


def portScan(target):
    global openPorts
    portThreads = []
    for portTuple in ports:
        for portNumber, scope in portTuple.items():
            portThreads.append(threading.Thread(target=portScanThread, args=(target, int(portNumber))))

    for thread in portThreads:
        thread.start()

    for thread in portThreads:
        thread.join()

    return openPorts
