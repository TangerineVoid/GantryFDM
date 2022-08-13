#!/usr/bin/python
import time,z
import serial
import os
import json

st = 0.5

with serial.Serial(port="COM7", baudrate=115200, bytesize=8, stopbits=serial.STOPBITS_ONE) as sr:
    print('serial connected')
    #fname = 'D:/Users/sergio.salinas/Documents/Imager Data/' + 'data_' + str(
    #        datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")) + '.txt'
    fname = r"D:\Users\sergio.salinas\PycharmProjects\test\XDK.txt"
    with open(fname, 'a') as f:
        print('file opened')
        start = 0
        while 1:
            #s.sendall(b'ml,cmm,p,v,\r')
            data = sr.readline()
            datas = data.split(b' ')
            if datas[0] == b'\rx' and datas[2] == b'mg\n':
                sdate = str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S.%f")[:-2])
                f.write("data={'features': '{")
                dataf = datas[1].replace(b'=', b'')
                f.write('"Accx(mg)": ' + dataf.decode("ISO-8859-1") + ', ')
                start = 1
                data = sr.readline()
                datas = data.split(b' ')
            if datas[0] == b'\ry' and datas[2] == b'mg\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                f.write('"Accy(mg)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = sr.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rz' and datas[2] == b'mg\r\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                f.write('"Accz(mg)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = sr.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rh' and datas[2] == b'%rh\r\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                f.write('"Hum(%rh)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = sr.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rp' and datas[2] == b'Pa\r\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                f.write('"Press(pa)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = sr.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rt' and datas[2] == b'mDeg\r\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                f.write('"Temp(mDeg)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = sr.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rx' and datas[2] == b'microTesla\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                f.write('"Magx(microTesla)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = sr.readline()
                datas = data.split(b' ')
            if datas[0] == b'\ry' and datas[2] == b'microTesla\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                f.write('"Magy(microTesla)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = sr.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rz' and datas[2] == b'microTesla\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                f.write('"Magz(microTesla)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = sr.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rr' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                dataf = dataf.replace(b'\r\n', b'')
                f.write('"r": ' + dataf.decode("ISO-8859-1") + ', ')
                data = sr.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rx' and datas[2] == b'mDeg\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                f.write('"Gyx(mDeg)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = sr.readline()
                datas = data.split(b' ')
            if datas[0] == b'\ry' and datas[2] == b'mDeg\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                f.write('"Gyy(mDeg)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = sr.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rz' and datas[2] == b'mDeg\r\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                f.write('"Gyz(mDeg)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = sr.readline()
                datas = data.split(b' ')
            if datas[0] == b'Light' and start == 1:
                dataf = datas[6].replace(b':', b'')
                f.write('"Light(mlx)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = sr.readline()
                datas = data.split(b' ')
                edate = str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S.%f")[:-2])
            if datas[0] == b'Vrms' and start == 1:
                dataf = datas[2]
                f.write('"Noise(Vrms)": ' + dataf.decode("ISO-8859-1") + ', ')
                f.write('"Startdate": ' + sdate + ', ' + '"Enddate": ' + edate)
                start = 0
                f.write("}', 'state': 'ok'}) \n")
            #if data == "Accelerometer Converted data :":
            #print("read acc")
            #dataarr = literal_eval(data.decode("ISO-8859-1"))
            #if dataarr[0] != '0':
            #arr = bytes("!Snapshot\r\n", 'utf-8')
            #sr.write(arr)

            #        str(datetime.datetime.now()) + '\n')
            #time.sleep(st)