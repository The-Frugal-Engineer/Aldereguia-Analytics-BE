import pandas as pd

path = "./files/"


def write_panda_to_file(matrix, asset):
    matrix.to_csv(path + asset + ".csv")


def read_csv_to_panda(asset):
    df = pd.read_csv(path+asset+'.csv')
    return df

