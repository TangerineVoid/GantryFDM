#!/usr/bin/env python
# echo-server.py
import sys,os
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

    while True:
        print "Connected by ",addr
        data = conn.recv(1024)
        if not data:
            break
        if data == b'p\r':
            blockPrint()
            m = linuxcnc.stat() # create a connection to the status channel
            m.poll() # get current values
            val = getattr(m,'position')
            val = ''.join(str(val))
            enablePrint()
            print val
            conn.sendall(bytes(val))
finally:
    s.close()
