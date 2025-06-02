import numpy as np
import math

def fit_circle(df):
    """
    estimates the radius and height (z) of a contact circle
    """
    z_mean = df['z'].mean()
    r_mean = math.sqrt(np.mean(df['x']**2 + df['y']**2))
    return z_mean, r_mean

def compute_contact_angle(z_top, r_top, z_bot, r_bot):
    """
    computes the contact angle in degrees using top and bottom circle fits.
    """
    zp = abs(z_bot - z_top)
    rp = abs(r_bot - r_top)

    gammap = abs(np.arctan(r_bot / z_bot))
    alphap = np.arctan(rp / zp)

    angle_radians = np.pi - gammap - alphap
    return angle_radians * 180 / np.pi
