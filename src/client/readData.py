import serial
import socket
import datetime
from ast import literal_eval
import zlib
import base64

class ReadData:
    # instance attributes

    def __init__(self):
        # Serial comm parameters
        self.port = "COM5"
        self.baudrate = 115200
        self.bytesize = 8
        self.stopbits = serial.STOPBITS_ONE
        # Socket TCP/IP comm parameters
        self.host = "192.168.137.2"  # The server's hostname or IP address
        self.socket_port = 65433  # The port used by the server

    def initialize_connection(self, parent, host=None, port=None, baudrate=None, bytesize=None, stopbits=None):
        if parent == "machinekit":
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('socket connected')
            host = host=host or self.host
            port = port or self.socket_port
            try:
                s.connect((host, port))
            except Exception as e:
                print(f"Error initializing machinekit. The error '{e}' occurred")
            return s
        elif parent == "TIM40":
            s = serial.Serial(port=port or self.port, baudrate=baudrate or self.baudrate,
                          bytesize=bytesize or self.bytesize, stopbits=stopbits or self.stopbits)
            print('serial connected')
            return s
        elif parent == "XDK":
            try:
                s = serial.Serial(port=port or self.port, baudrate=baudrate or self.baudrate,
                              bytesize=bytesize or self.bytesize, stopbits=stopbits or self.stopbits)
                print('serial connected')
                return s
            except Exception as e:
                print(f"Error initializing machinekit. The error '{e}' occurred")

    def machinekit(self, s):
        try:
            s.sendall(b'ml,cmm,p,v,f,\r')
            data = s.recv(1024)
            data_arr = literal_eval(data.decode("ISO-8859-1"))
            return data_arr
        except Exception as e:
            print(f"Error reading machinekit. The error '{e}' occurred")

    def TIM40(self, s):
        try:
            arr = bytes("!Snapshot\r\n", 'utf-8')
            s.write(arr)
            #No return
        except Exception as e:
            print(f"Error reading TIM40. The error '{e}' occurred")

    def XDK(self, s, port=None, baudrate=None, bytesize=None, stopbits=None):
        datarr = []
        start = 0
        while 1:
            data = s.readline()
            datas = data.split(b' ')
            if datas[0] == b'\rx' and datas[2] == b'mg\n':
                sdate = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-2])
                dataf = datas[1].replace(b'=', b'')
                datarr.append(dataf)
                #f.write('"Accx(mg)": ' + dataf.decode("ISO-8859-1") + ', ')
                start = 1
                data = s.readline()
                datas = data.split(b' ')
            if datas[0] == b'\ry' and datas[2] == b'mg\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                datarr.append(dataf)
                #f.write('"Accy(mg)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = s.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rz' and datas[2] == b'mg\r\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                datarr.append(dataf)
                #f.write('"Accz(mg)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = s.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rh' and datas[2] == b'%rh\r\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                datarr.append(dataf)
                #f.write('"Hum(%rh)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = s.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rp' and datas[2] == b'Pa\r\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                datarr.append(dataf)
                #f.write('"Press(pa)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = s.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rt' and datas[2] == b'mDeg\r\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                datarr.append(dataf)
                #f.write('"Temp(mDeg)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = s.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rx' and datas[2] == b'microTesla\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                datarr.append(dataf)
                #f.write('"Magx(microTesla)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = s.readline()
                datas = data.split(b' ')
            if datas[0] == b'\ry' and datas[2] == b'microTesla\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                datarr.append(dataf)
                #f.write('"Magy(microTesla)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = s.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rz' and datas[2] == b'microTesla\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                datarr.append(dataf)
                #f.write('"Magz(microTesla)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = s.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rr' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                dataf = dataf.replace(b'\r\n', b'')
                datarr.append(dataf)
                #f.write('"r": ' + dataf.decode("ISO-8859-1") + ', ')
                data = s.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rx' and datas[2] == b'mDeg\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                datarr.append(dataf)
                #f.write('"Gyx(mDeg)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = s.readline()
                datas = data.split(b' ')
            if datas[0] == b'\ry' and datas[2] == b'mDeg\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                datarr.append(dataf)
                #f.write('"Gyy(mDeg)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = s.readline()
                datas = data.split(b' ')
            if datas[0] == b'\rz' and datas[2] == b'mDeg\r\n' and start == 1:
                dataf = datas[1].replace(b'=', b'')
                datarr.append(dataf)
                #f.write('"Gyz(mDeg)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = s.readline()
                datas = data.split(b' ')
            if datas[0] == b'Light' and start == 1:
                dataf = datas[6].replace(b':', b'')
                datarr.append(dataf)
                #f.write('"Light(mlx)": ' + dataf.decode("ISO-8859-1") + ', ')
                data = s.readline()
                datas = data.split(b' ')
                edate = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-2])
            if datas[0] == b'Vrms' and start == 1:
                dataf = datas[2]
                datarr.append(dataf)
                datarr.append(sdate)
                #f.write('"Noise(Vrms)": ' + dataf.decode("ISO-8859-1") + ', ')
                #f.write('"Startdate": ' + sdate + ', ' + '"Enddate": ' + edate)
                start = 0
                break
        return datarr

    def decompressData(self, data):
        #print(len(data))
        data = (zlib.decompress(base64.b64decode(data))).decode("ISO-8859-1")
        #data = base64.b64encode(data)
        #data = data.decode("ISO-8859-1")
        #print(len(data))
        return data