# import numpy as np
# path = r"D:\Users\sergio.salinas\Documents\Imager Data\subir"
# file = path + "\Record_2022-04-27_15-18-33.csv"
# with open(file) as file_name:
#     array = np.genfromtxt(file_name, delimiter=',')[:,:-1]
#
# print(array)
# fname = 'D:/Users/sergio.salinas/Documents/Imager Data/' + 'data_' + '.txt'
# with open(fname, 'a') as f:
#     print('file opened')
#     sarr = ' '.join(str(c) for r in array for c in r)
#     f.write(sarr)
#     #f.write(sarr + '\r\n')

# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
#
# class MyHandler(FileSystemEventHandler):
#     def on_any_event(self, event):
#         print(event.event_type, event.src_path)
#
#     def on_created(self, event):
#         print("on_created", event.src_path)
#         print(event.src_path.strip())
#         if((event.src_path).strip() == ".\test.xml"):
#             print("Execute your logic here!")
#
# event_handler = MyHandler()
# observer = Observer()
# observer.schedule(event_handler, path='.', recursive=False)
# observer.start()
#
# while True:
#     try:
#         pass
#     except KeyboardInterrupt:
#         observer.stop()

import sys
import logging
from watchdog.observers import Observer
#from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

def on_created(event):
    print('created')

if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO,
    #                    format='%(asctime)s - %(message)s',
    #                    datefmt='%Y-%m-%d %H:%M:%S')
    #path = sys.argv[1] if len(sys.argv) > 1 else '.'
    path = 'D:/Users/sergio.salinas/Documents/Imager Data/'
    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_created
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while observer.isAlive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()