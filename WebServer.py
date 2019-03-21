from TrivialFunctions import *
import threading
import sys, os, socket
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


def threadedSimpleServer():
    HOST = "0.0.0.0"
    PORT = 8080
    CWD = os.getcwd() + "\Primers"
    server = ThreadingSimpleServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)

    output(1, "step", "The HTTP server is exposing %s on %s:%d" % (CWD, HOST,PORT))
    try:
        webServerThread = threading.Thread(target=server.serve_forever)
        webServerThread.daemon = True
        webServerThread.start()
    except:
        output(1, "error", "There was an error starting the server, quitting...")