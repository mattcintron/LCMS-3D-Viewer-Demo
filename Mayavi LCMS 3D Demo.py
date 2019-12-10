from numpy import pi, sin, cos, mgrid
import numpy as np
from mayavi import mlab
import pandas as pd
from scipy.signal import argrelextrema
from scipy import interpolate
from scipy.interpolate import griddata
from sklearn.utils import resample
from scipy import signal


def scale_function(lcms_data):
    """
    Finds a scalar for each axis that will rescale the axis to a specific range.
    :param lcms_data: Full data
    :return: A rescaling scalar for each axis
    """
    a = lcms_data[:, 0]
    b = lcms_data[:, 1]
    c = lcms_data[:, 2]

    max_x = max(a)
    max_y = max(b)
    max_z = max(c)

    max_num_x = 30
    max_num_y = 35
    max_num_z = 20

    x_scaling = max_num_x / max_x
    # x_scaling = round(x_scaling, 2)

    y_scaling = max_y / max_num_y
    # y_scaling = round(y_scaling, 2)

    z_scaling = max_z / max_num_z
    # z_scaling = round(z_scaling, 2)

    return x_scaling, y_scaling, z_scaling


# process the data to arrays
data = pd.read_csv("HP_1a1.csv")
data = np.array(data)
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]

# Retrieve scaling scalars from scale function
x_scale, y_scale, z_scale = scale_function(data)

# full downsampling of data
xnew = []
ynew = []
znew = []

data_BucketX = []
data_BucketY = []
data_BucketZ = []


index = 0
for item in x:
    if index == 0:
        index += 1
        continue
    if item == x[index - 1]:
        data_BucketX.append(item)
        data_BucketY.append(y[index])
        data_BucketZ.append(z[index])
    else:
        if len(data_BucketX) < 100:
            index += 1
            continue
        xn = []
        yn = []
        zn = []
        sample = int(len(data_BucketX) / 1.2)
        xn.extend(signal.resample(data_BucketX, sample))
        yn.extend(signal.resample(data_BucketY, sample))
        zn.extend(signal.resample(data_BucketZ, sample))

        i = 0
        for foo in zn:
            xnew.append(xn[i] * x_scale)
            ynew.append(yn[i] / y_scale)
            znew.append(zn[i] / z_scale)
            i += 1

        data_BucketX.clear()
        data_BucketY.clear()
        data_BucketZ.clear()
    index += 1


foo = []

# set a max z-axis threshold
z_threshold = max(znew) * 0.01

for i in range(len(znew)):
    # append to a list the indices of z-axis values that are less than the threshold
    if znew[i] < z_threshold:
        foo.append(i)

# removes all corresponding elements from each array
xnew = np.delete(xnew, foo)
ynew = np.delete(ynew, foo)
znew = np.delete(znew, foo)


# Visualize the points
# pts = mlab.points3d(x_3d, y_3d, z_3d, z_3d, mode='point')
pts = mlab.points3d(xnew, ynew, znew, znew, mode='point')
# pts = mlab.points3d(xnew, ynew, znew, znew, mode='point', scale_factor=3.0)


# Create and visualize the mesh
mesh = mlab.pipeline.delaunay2d(pts)
surf = mlab.pipeline.surface(mesh)
pts.remove()


# Simple plot axis info rendering
mlab.xlabel("Retention")
mlab.ylabel("m/z")
mlab.zlabel("Intensity")
mlab.show()
