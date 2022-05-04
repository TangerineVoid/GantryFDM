import sys
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import numpy as np
from threading import Thread
from queue import Queue
import time as t
import CSqlCOM as sql

def on_created(event):
    file = path + '\\' + str(event.src_path).split('\\')[-1]
    print("New file")
    convFile(file)


def convFile(file):
    t.sleep(0.2)
    print(file)
    with open(file) as file_name:
        array = np.genfromtxt(file_name, delimiter=',')[:, :-1]
    fname = 'D:/Users/sergio.salinas/Documents/Imager Data/data/' + 'data_' + '.txt'
    with open(fname, 'a') as f:
        #print('file opened')
        sarr = ' '.join(str(c) for r in array for c in r)
        query = """
        INSERT INTO tbtest (strtempsnap)
        VALUES (" {} ");
        """.format(sarr)
        sql.add_value(connection, str(query))
        #f.write(sarr + '\n')
        #f.write(sarr)


if __name__ == "__main__":
    connection = sql.create_connection("localhost", "root", "admin", "manuf_cell")
    path = r"D:\Users\sergio.salinas\Documents\Imager Data"
    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_created
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while observer.isAlive():
            observer.join(1)
    finally:
        print("Finished")
        observer.stop()
        observer.join()
