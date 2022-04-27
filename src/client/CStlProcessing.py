#!/usr/bin/python
import numpy as np
from stl import mesh
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d

path = r"D:\Users\sergio.salinas\Downloads\ScanCR1.stl"
my_mesh = mesh.Mesh.from_file(path)

#****GRAPH 3D MODEL****
# Create a new plot
figure = plt.figure()
axes = mplot3d.Axes3D(figure, auto_add_to_figure=False)
figure.add_axes(axes)

#Move 3D Model to Origin
midPosRel = (my_mesh.max_ - my_mesh.min_)/2
my_mesh.x = my_mesh.x - (midPosRel[0] + my_mesh.min_[0])
my_mesh.y = my_mesh.y - (midPosRel[1] + my_mesh.min_[1])
my_mesh.z = my_mesh.z - (midPosRel[2] + my_mesh.min_[2])
# Load the STL files and add the vectors to the plot
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vectors))

# Auto scale to the mesh size
scale = my_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)


#****CHANGE PERSPECTIVE****:
# Create a new plot
figure = plt.figure()
axes = mplot3d.Axes3D(figure, auto_add_to_figure=False)
figure.add_axes(axes)

# Load the STL files and add the vectors to the plot
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vectors))
axes.view_init(90,270) # top view

# Auto scale to the mesh size
axes.autoscale_view()
scale = my_mesh.points.flatten('F') #C, F, A, or K
axes.auto_scale_xyz(scale, scale, scale)

#****OBTAIN AND GRAPH DATA CLOUD****:
# Adquire data
stl_data = mesh.Mesh.from_file(path)
# Reshape data to a 3dimensional array, x,y,z
points = stl_data.points.reshape([-1, 3])
# Many points coordinates are the same, since the points are vertices shared by several triangular mesh faces,
# thus to avoid graphing duplicate points
point_list = np.unique(points, axis=0)

# Create a new plot
figure = plt.figure()
axes = mplot3d.Axes3D(figure, auto_add_to_figure=False)
figure.add_axes(axes)
axes.scatter3D(point_list[:,0], point_list[:,1], point_list[:,2]);

plt.show()
