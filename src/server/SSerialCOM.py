#!/usr/bin/env python
# echo-server.py
import sys, os
import linuxcnc
import socket


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


HOST = "192.168.137.2"  # Standard loopback interface address (localhost)
PORT = 65433  # Port to listen on (non-privileged ports are > 1023)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORT))
    s.listen(5)
    conn, addr = s.accept()
    print "Connected by ", addr

    while True:
        data = conn.recv(1024)
        if not data:
            break
        else:
            blockPrint()
            m = linuxcnc.stat()  # create a connection to the status channel
            m.poll()  # get current values
            vout = []
            enablePrint()
            for x in data.split(","):
                if x == "ml":
                    val = getattr(m, 'motion_line')
                    val = ''.join(str(val))
                    vout.append(val)
                elif x == "cmm":
                    val = getattr(m, 'command')
                    val = ''.join(str(val))
                    vout.append(val)
                elif x == "p":
                    val = getattr(m, 'position')
                    val = ''.join(str(val))
                    vout.append(val)
                elif x == "v":
                    val = getattr(m, 'current_vel')
                    val = ''.join(str(val))
                    vout.append(val)
                elif x == "f":
                    val = getattr(m, 'file')
                    val = ''.join(str(val))
                    vout.append(val)
            enablePrint()
            conn.sendall(bytes(''.join(str(vout))))
finally:
    s.close()