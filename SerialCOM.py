#!/usr/bin/python
import socket
import time, datetime
import serial
import os

st = 0.5
HOST = "192.168.137.2"  # The server's hostname or IP address
PORT = 65433  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print('socket connected')
    s.connect((HOST, PORT))
    with serial.Serial(port="COM5", baudrate=115200, bytesize=8, stopbits=serial.STOPBITS_ONE) as sr:
        print('serial connected')
        with open('D:/Users/sergio.salinas/Documents/Imager Data/' + 'positions_' + str(
                datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")) + '.txt', 'a') as f:
            print('file opened')
            while 1:
                s.sendall(b'p\r')
                data = s.recv(1024)

                arr = bytes("!Snapshot\r\n", 'utf-8')
                sr.write(arr)

                f.write(data.decode("ISO-8859-1") + '@' + str(datetime.datetime.now()) + '\n')
                time.sleep(st)
                #print(f"Received", data)p
