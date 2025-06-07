import pandas as pd

def load_2d_csv(path):
    df = pd.read_csv(path)
    return df["Points_0"], df["Points_2"]

def load_3d_csv(path):
    df = pd.read_csv(path)
    
    return df["Points_0"], df["Points_1"], df["Points_2"]


# returns a column of data containing the positioing of the interface points
def rad(df):
    return df.iloc[:, 0]**2 +  df.iloc[:, 1]**2 + df.iloc[:, 2]**2

# returns a column of data containing the positioing of the interface points mapped on xy plane
def sq(df):
    return df.iloc[:, 0]**2 +  df.iloc[:, 1]**2

# returns the part of neutral interface 
def plane_without_particle(df, R):
    return  df.loc[sq(df) > (2*R)**2]
