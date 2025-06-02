import pandas as pd
import numpy as np
from contang.data_loader import load_2d_csv, load_3d_csv, sq, plane_without_particle
from contang.interpolation import interpolate_1d, interpolate_2d, fit_plane
from contang.geometry import select_contact_ring
from contang.angle_calc import fit_circle, compute_contact_angle

def main():
    # radius of the particle 
    R = 16
    # load sample data
    x, y = load_2d_csv('data/sample_2d.csv')
    x3, y3, z3 = load_3d_csv('data/sample_3d.csv')

    # build the 3D dataframe
    df = pd.DataFrame({'x': x3, 'y': y3, 'z': z3})

    # finding plane fit parameters
    tobe_fitted = plane_without_particle(df, R)
    xf, yf, zf = list (tobe_fitted['x']), list (tobe_fitted['y']), list (tobe_fitted['z'])
    fit_params = fit_plane(xf, yf, zf)

    # select top and bottom rings
    top_df = select_contact_ring(df, fit_params, 0.5, 0.75)
    bot_df = select_contact_ring(df, fit_params, 1.5, 1.75)

    # optional: filter out very large radius points
    top_df = top_df.loc[sq(top_df) < 19**2].reset_index(drop=True)

    # fit circles
    z_top, r_top = fit_circle(top_df)
    z_bot, r_bot = fit_circle(bot_df)

    # compute contact angle
    angle = compute_contact_angle(z_top, r_top, z_bot, r_bot)

    print(f"Estimated wetting/contact angle: {angle:.2f} degrees")

if __name__ == "__main__":
    main()

