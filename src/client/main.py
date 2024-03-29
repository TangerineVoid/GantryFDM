import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread
from sqlCOM import SqlCOM as sql
from readData import ReadData as rdata
from saveData import SaveData as sdata
from tensorflow.keras import layers
#import sys
#import logging
#from queue import Queue
#import time as t
#import numpy as np
#import datetime
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf

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
    time.sleep(1)

    # To save a .txt file
    #[data,dataxdk] = [readData.machinekit(con_machinekit), [readData.XDK(con_XDK)[13]]]
    #saveData.save_txtFile(data, fname, data2 = dataxdk)

    # To Process thermal image
    ts = time.time_ns()
    data = readData.machinekit(con_machinekit)
    print("read {}".format(time.time_ns() - ts))
    ts = time.time_ns()
    datan = saveData.process_server(data, fname)
    print("process {}".format(time.time_ns() - ts))
    ts = time.time_ns()
    datar = saveData.run_model(datan)
    print("run {}".format(time.time_ns() - ts))
    ts = time.time_ns()
    print("status es: ", datar)
    print("print {}".format(time.time_ns() - ts))

    #path = ''
    #pd.DataFrame( data ).to_csv( path + '/cdata.csv', index = False, header = False )
    #plt.imshow(data)
    #plt.show()

if __name__ == "__main__":
    # Variables definition
    path = r"D:\Users\sergio.salinas\Documents\Imager Data"
    st_tc = 0.5 #Sampling time for thermal csv acquisition
    st_xdk = 0.5  # Sampling time for XDK
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
    ts = time.time_ns()
    con_machinekit = readData.initialize_connection("machinekit")
    print("init machinekit")
    con_thermalcamera = readData.initialize_connection("TIM40", port="COM5")
    print("init thermal camera")
    con_XDK = readData.initialize_connection("XDK", port="COM7")
    print("init XDK")
    print("init {}".format(time.time_ns() - ts))
    #For the CNN
    ts = time.time_ns()
    saveData.classifier = saveData.discriminator_model()
    saveData.classifier.load_weights(r"D:\Users\sergio.salinas\PycharmProjects\SerialCOM\temp\GantryFDM\src\client\weights\cp-0034.ckpt")
    print("cnn {}".format(time.time_ns() - ts))

    # Initialize handlers and observers
    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_created
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    # Create threads to manage acquisition functions
    threads = []
    nthds = 2
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
