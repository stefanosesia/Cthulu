import socket


def client_send(target, port, message):
    target_host = target
    target_port = port

    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect the client
    client.connect((target_host, target_port))

    # send some data
    client.send(message)

    # receive data
    response = client.recv(4096)

    return response
