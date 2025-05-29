import pandas as pd

def load_2d_csv(path):
    df = pd.read_csv(path)
    return df["Points_0"], df["Points_2"]

def load_3d_csv(path):
    df = pd.read_csv(path)
    return df["Points_0"], df["Points_1"], df["Points_2"]
