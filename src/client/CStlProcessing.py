#!/usr/bin/python
import numpy as np
from stl import mesh
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm

path = r"D:\Users\sergio.salinas\Downloads\ScanCR1.stl"
my_mesh = mesh.Mesh.from_file(path)

# # Create a new plot
# figure = plt.figure()
# axes = mplot3d.Axes3D(figure)
#
# # Load the STL files and add the vectors to the plot
# axes.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vectors))
#
# # Auto scale to the mesh size
# scale = my_mesh.points.flatten()
# axes.auto_scale_xyz(scale, scale, scale)
#
# # Show the plot to the screen
# #plt.show()
#
# #       change perspective:
# figure = plt.figure()
# axes = mplot3d.Axes3D(figure)
#
# axes.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vectors))
# axes.view_init(90,270) # top view
# scale = my_mesh.points.flatten('F') #C, F, A, or K
# axes.auto_scale_xyz(scale, scale, scale)
#
# #plt.show()

# Obtain data cloud
stl_data = mesh.Mesh.from_file(path)
points = stl_data.points.reshape([-1, 3])
point_list = np.unique(points, axis=0)

figure = plt.figure()

axes = mplot3d.Axes3D(figure, auto_add_to_figure=False)
figure.add_axes(axes)
#axes = plt.axes(projection ="3d")
my_cmap = plt.get_cmap('hsv')
axes.scatter3D(point_list[:,0], point_list[:,1], point_list[:,2]);
scale = my_mesh.points.flatten()
print(scale)
scalex = [min(point_list):max(point_list)]
scaley = (max(point_list[:,1]) - min(point_list[:,1]))/2
scalez = (max(point_list[:,2]) - min(point_list[:,2]))/2
print(scalex)
print(scaley)
print(scalez)
#axes.set_box_aspect(aspect = (1,1,1))
axes.auto_scale_xyz(scalex,scaley,scalez)

plt.show()
