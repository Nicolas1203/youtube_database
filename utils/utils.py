"""
Utils functions for data exploration
"""
import pandas as pd
import glob
import json
from pathlib import Path
from tqdm import tqdm


def json_to_df(data_dir: str, verbose: bool = False) -> pd.DataFrame:
    """
    Concatenate all json data files in the directory as a pandas dataframe.

    :param verbose:     Flag for logging  useful information
    :param data_dir:         Path to the directory containing every json files
    :return:            Dataframe of every json concatenated
    """
    json_files = glob.glob(str(Path(data_dir) / '*.json'))
    df_all = pd.DataFrame()

    # Loop over every file in directory
    # print("processing...")
    for file in tqdm(json_files):
        with open(file) as f:
            content = json.load(f)
            df = pd.DataFrame(content)
            if verbose:
                print(f"All columns size : {len(df_all.columns)}")
                print(f"New element columns size : {len(df.columns)}")
                print(f"Number of new columns added : {len(df.columns.difference(df_all.columns))}")
                print("New columns :")
                print(str(df.columns.difference(df_all.columns)))
            df_all = pd.concat([df_all, df], sort=True)

    return df_all
