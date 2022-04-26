from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from threading import Thread
from time import sleep, perf_counter
import os

def uploadFile(x):
    # for upload_file in upload_file_list:
    # f = drive.CreateFile({'title': x})
    global numf
    f = drive.CreateFile({'parents': [
        {'kind': 'drive#fileLink', 'driveId': '0ANnhUPokrNvoUk9PVA', 'id': '1zkXkA3kHYUCW-mb1DvWiWLnZppcu1Kq7'}]})
    f['title'] = x
    f.SetContentFile(os.path.join(path, x))
    # f.SetContentFile(os.path.join(path, upload_file))
    while True:
        try:
            f.Upload(param={'supportsTeamDrives': True})
        except:
            continue
        break
    numf += 1

    # Due to a known bug in pydrive if we
    # don't empty the variable used to
    # upload the files to Google Drive the
    # file stays open in memory and causes a
    # memory leak, therefore preventing its
    # deletion
    f = None

# Below code does the authentication
# part of the code
gauth = GoogleAuth()

# Creates local webserver and auto
# handles authentication.
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# replace the value of this variable
# with the absolute path of the directory
path = r"D:\Users\sergio.salinas\Documents\Imager Data\subir"

# iterating thought all the files/folder
# of the desired directory
#upload_file_list = ['test.txt']
flist = os.listdir(path)
start_time = perf_counter()
# create and start 10 threads
threads = []
count = 0
ltend = 0
numf = 0
nthds = 7
for e, x in enumerate(flist):
    for n in range(0, nthds):
        if n+(count*nthds) <= len(flist) - 1:
            t = Thread(target=uploadFile, args=(flist[n+(count*nthds)],))
            threads.append(t)
            while True:
                try:
                    t.start()
                except:
                    continue
                break
        else:
            litend = 1
            break

    count += 1
    for t in threads:
        while True:
            try:
                t.join()
            except:
                continue
            break
    if ltend == 1:
        ltend = 0
        count = 0
        break
end_time = perf_counter()

print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')
print("Se subieron: ", numf)