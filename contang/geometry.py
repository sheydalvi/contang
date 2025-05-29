import math
import pandas as pd

def distance_to_plane(x, y, z, a, b, d):
    """
    computes the perpendicular distance from (x, y, z) to the plane ax + by - z + d = 0
    """
    numerator = abs(a * x + b * y - z + d)
    denominator = math.sqrt(a**2 + b**2 + 1)
    return numerator / denominator

def select_contact_ring(df, fit_params, lower_bound, upper_bound):
    """
    selects points within a distance range from a plane
    - fit_params = (a, b, d) from the plane fit
    - lower_bound and upper_bound define the thickness of the ring
    returns a new filtered DataFrame
    """
    a, b, d = fit_params
    filtered_indices = []

    for i, row in df.iterrows():
        dist = distance_to_plane(row['x'], row['y'], row['z'], a, b, d)
        if lower_bound < dist < upper_bound:
            filtered_indices.append(i)

    return df.loc[filtered_indices].reset_index(drop=True)
