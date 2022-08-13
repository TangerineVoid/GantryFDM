import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread
from sqlCOM import SqlCOM as sql
from readData import ReadData as rdata
from saveData import SaveData as sdata
#import sys
#import logging
#from queue import Queue
#import time as t
#import numpy as np
#import datetime
import matplotlib.pyplot as plt

def on_created(event):
    file = path + '\\' + str(event.src_path).split('\\')[-1]
    print("New file")
    saveData.file = file
    acquire_machinekit()
    #saveData.save_sql("thermal_camera", "sql", sqlConnection1)

def acquire_thermalData():
    while 1:
        #data_machinekit = readData.machinekit(con_machinekit)
        #if data_machinekit[0] != 0:
        readData.TIM40(con_thermalcamera)
        time.sleep(st_tc)

#def acquire_XDK():
#    while 1:
#        saveData.save_sql("XDK", "sql", sqlConnection2, readData.XDK(con_XDK))
#        time.sleep(st_xdk)


def acquire_machinekit():
    fname = 'D:/Users/sergio.salinas/Documents/' + 'data_'
    #print(data_machinekit[0])
    time.sleep(2)
    data = readData.machinekit(con_machinekit)
    plt.imshow(saveData.process_server(data, fname))

if __name__ == "__main__":
    # Variables definition
    path = r"D:\Users\sergio.salinas\Documents\Imager Data"
    st_tc = 0.5 #Sampling time for thermal csv acquisition
    #st_xdk = 3  # Sampling time for thermal csv acquisition
    #st_mkt = 5  # Sampling time for thermal csv acquisition

    # Initialize communication objects
    #sqlConnection1 = sql("localhost", "root", "admin", "manuf_cell")
    #sqlConnection1.create_connection()
    #sqlConnection2 = sql("localhost", "root", "admin", "manuf_cell")
    #sqlConnection2.create_connection()
    #sqlConnection3 = sql("localhost", "root", "admin", "manuf_cell")
    #sqlConnection3.create_connection()
    readData = rdata()
    saveData = sdata()
    con_machinekit = readData.initialize_connection("machinekit")
    print("init machinekit")
    con_thermalcamera = readData.initialize_connection("TIM40", port="COM5")
    print("init thermal camera")
    #con_XDK = readData.initialize_connection("XDK", port="COM7")
    #print("init XDK")

    # Initialize handlers and observers
    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_created
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    # Create threads to manage acquisition functions
    threads = []
    nthds = 1
    t = Thread(target=acquire_thermalData)
    t.start()
    threads.append(t)
    #t = Thread(target=acquire_XDK)
    #t.start()
    #threads.append(t)
    #t = Thread(target=acquire_machinekit)
    #t.start()
    #threads.append(t)
    for t in threads:
        while True:
            try:
                t.join()
            except:
                continue
            break

    #
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        print("Finished")
        #con_XDK.close()
        con_thermalcamera.close()
        con_machinekit.close()
        observer.stop()
        observer.join()
