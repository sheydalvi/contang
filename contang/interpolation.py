import numpy as np
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

