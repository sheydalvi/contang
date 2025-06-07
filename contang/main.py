import pandas as pd
import numpy as np
from contang.data_loader import load_2d_csv, load_3d_csv, sq, plane_without_particle, rad
from contang.interpolation import interpolate_1d, interpolate_2d, fit_plane
from contang.geometry import select_contact_ring
from contang.angle_calc import fit_circle, compute_contact_angle


# input:    data file 2D xy slice, data file 3D xyz surface
# output:   origianl point positions, interpolated point positions both 2D and 3D
def load_and_interpolate_data(file_2d, file_3d):
    """
    loads the raw data, increases resolution in a 1D curve (2D grid) and 2D suraface (3D grid)
    """

    # 2D grid (just to visualize the importance and reliability of the resolution increase)
    x, y = load_2d_csv(file_2d)
    new_x = np.linspace(min(x), max(x), 1000)
    y_interp = interpolate_1d(x, y, new_x)

    # 3D grid
    x3, y3, z3 = load_3d_csv(file_3d)
    grid_x, grid_y, grid_z = interpolate_2d(x3, y3, z3)

    # save high resolution interface in a dataframe
    df = pd.DataFrame({'x': grid_x.flatten().tolist(), 'y': grid_y.flatten().tolist(), 'z': grid_z.flatten().tolist()})

    return x, y, new_x, y_interp, x3, y3, z3, grid_x, grid_y, grid_z ,df

# input:    interpolated interface, radius of the particle
# output:   parameters of the fitted plane
def fit_surface_plane(df, R):
    """
    fits a plane onto the non-deformed section of the interface 
    """
    tobe_fitted = plane_without_particle(df, R)
    xf, yf, zf = list(tobe_fitted['x']), list(tobe_fitted['y']), list(tobe_fitted['z'])
    fit_params = fit_plane(xf, yf, zf)
    return fit_params

# input:    interpolated interface, fitted plane parameters, radius of the particle, z-thickness of the ring as in lower and upper bound
# output:   top and bottom ring data points
def select_top_ring(df, fit_params, R, top_lower_bound, top_upper_bound, bot_lower_bound, bot_upper_bound):
    # remove interface points inside the particle
    df = df.loc[rad(df) > R**2].reset_index(drop=True)
    top_df = select_contact_ring(df, fit_params, top_lower_bound, top_upper_bound)
    bot_df = select_contact_ring(df, fit_params, bot_lower_bound, bot_upper_bound)

    # following part is to remove corners that are created because of spurious currents
    # the criterial 19 will be different for other particle sizes
    top_df = top_df.loc[sq(top_df) < 19**2].reset_index(drop=True)  # to be deleteed after the model enhancement
    return top_df, bot_df

# input:    top and bottom ring data points
# output:   angle
def calculate_angle_from_rings(top_df, bot_df):
    z_top, r_top = fit_circle(top_df)
    z_bot, r_bot = fit_circle(bot_df)

    angle = compute_contact_angle(z_top, r_top, z_bot, r_bot)
    return angle
