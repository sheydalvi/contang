import pandas as pd
import numpy as np
from numpy import linalg as LA
from scipy.interpolate import interp1d, griddata

def interpolate_1d(x, y, new_x):
    """
    performs 1D linear interpolation with extrapolation
    """
    f = interp1d(x, y, fill_value="extrapolate")
    return f(new_x)

def interpolate_2d(x, y, z, resolution=1000):
    """
    performs 2D interpolation on irregularly spaced data using griddata
    returns: grid_x, grid_y, grid_z
    """
    grid_x, grid_y = np.meshgrid(
        np.linspace(min(x), max(x), resolution),
        np.linspace(min(y), max(y), resolution)
    )
    data_points = np.column_stack((x, y))
    grid_z = griddata(data_points, z, (grid_x, grid_y), method='linear')
    return grid_x, grid_y, grid_z

def fit_plane(x, y, z):
    """
    fits a plane to the given 3D points (x, y, z) using normal equations
    returns: fitp: (a, b, c) where z = a*x + b*y + c
    """
    interpolate_2d(x, y, z, resolution=1000)

    tmp_A = []
    tmp_b = []
    
    for i in range(len(x)):
        tmp_A.append([x[i], y[i], 1])
        tmp_b.append(z[i])
    
    b = np.matrix(tmp_b).T 
    A = np.matrix(tmp_A)   

    # least squares 
    fitp = (A.T * A).I * A.T * b

    return fitp
