import subprocess
import threading
import os
netMap = {}

def windowsPingThread(address):
    global netMap
    with open(os.devnull, 'w') as DEVNULL:
        res = subprocess.call(["ping", "-n", "1", "-w", "200", address], stdout=DEVNULL)
    if res == 0:
        netMap.update({address: []})

def unixPingThread(address):
    global netMap
    with open(os.devnull, 'w') as DEVNULL:
        res = subprocess.call(["ping", "-c", "1", address], stdout=DEVNULL)
    if res == 0:
        netMap.update({address: []})

def pingSweep(netMask, targetOS):
    pingThreads = []

    for ping in range(100,110):
        address = netMask + str(ping)
        if targetOS == "WIN":
            pingThreads.append(threading.Thread(target=windowsPingThread, args=(address,)))
        elif targetOS == "UNIX":
            pingThreads.append(threading.Thread(target=unixPingThread, args=(address,)))

    for thread in pingThreads:
        thread.start()

    for thread in pingThreads:
        thread.join()

    return netMap
