import numpy as np

step = 10
maxcy, maxcx = 80,80
mincy, mincx = 0,0
z = 0.1
print("G1 F600 Z{}\nG1 F500\n".format(z), end='')
[print("G1 X{} Y{}\n".format(i, n), end='') for i in np.arange(mincx, maxcx, step) for n in np.arange(mincy, maxcy, step)]
print("G1 F600 X{} Y{} Z{}\nM2".format(mincx, mincy, z))
