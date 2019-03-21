import subprocess
import json
from Cypher import *
import random
import string

def executeCommand(command):
    try:
        subprocess.run(command)
        return True
    except:
        return False

def output(level, type, message):
    headers = {
        "error" : "[!]",
        "success" : "[+]",
        "warning" : "[?]",
        "info" : "[i]",
        "progress" : "[*]",
        "step" : "[#]"
    }
    print("\t" * level + headers[type] + " " + message)

def readFromFile(path):
    with open(path) as f:
        data = json.load(f)
    return(data)

def writeToFile(path, text):
    with open(path, 'w') as outfile:
        json.dump(text, outfile)

def writePlaybook(path, text):
    with open(path, 'w') as outfile:
        outfile.write(text)

def writePrimerHeader(key):
    headerContent = "key = \"" + str(key) + "\"\norigin =\"" + "localhost" + "\""
    output(0, "step", "Writing secrets to the primer headers")
    try:
        with open("Sources/Comms.py","w") as header:
            header.write(headerContent)
        output(1, "success", "The header was generated successfully")
        return True
    except:
        output(1, "error", "The header could not be generated")
        return False

def generateRandomKey():
    return(''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(64)))
