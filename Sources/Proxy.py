import socket
import threading
from Sources.Client import *

def proxy(bindPort, targetHost, targetPort):
    bind_ip = "0.0.0.0"
    bind_port = bindPort

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((bind_ip, bind_port))

    server.listen(5)

    print("[*] Listening on %s:%d" % (bind_ip, bind_port))


    def handle_client(client_socket):
        # print out what the client sends
        request = client_socket.recv(1024)

        print("[*] Reveived: %s" % request)
        response = client_send(targetHost, targetPort, request)

        # send back a packet
        client_socket.send(response)

        client_socket.close()


    while True:
        client, addr = server.accept()

        print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

        # spin up our client thread to handle incoming data
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


proxy(6899, "localhost", 1337)
