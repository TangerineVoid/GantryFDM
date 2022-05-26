#!/usr/bin/python
import socket
import time, datetime
import serial
from ast import literal_eval
import numpy as np
import os

st = 0.5
HOST = "192.168.137.2"  # The server's hostname or IP address
PORT = 65433  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print('socket connected')
    s.connect((HOST, PORT))
    with serial.Serial(port="COM5", baudrate=115200, bytesize=8, stopbits=serial.STOPBITS_ONE) as sr:
        print('serial connected')
        fname = 'D:/Users/sergio.salinas/Documents/Imager Data/' + 'data_' + str(
                datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")) + '.txt'
        with open(fname, 'a') as f:
            print('file opened')
            while 1:
                s.sendall(b'ml,cmm,p,v,\r')
                data = s.recv(1024)
                dataarr = literal_eval(data.decode("ISO-8859-1"))
                if dataarr[0] != '0':
                    arr = bytes("!Snapshot\r\n", 'utf-8')
                    sr.write(arr)

                    f.write(data.decode("ISO-8859-1") + '@' +
                            str(datetime.datetime.now()) + '\n')
                    time.sleep(st)