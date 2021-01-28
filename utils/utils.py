"""
Utils functions for data exploration
"""
import pandas as pd
import glob
import json
from pathlib import Path
from tqdm import tqdm
import time
import datetime as dt
import matplotlib.pyplot as plt



def json_to_df(data_dir: str, verbose: bool=False) -> pd.DataFrame:
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
    for i, file in enumerate(json_files):
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


def json_to_csv(data_dir: str, out_dir:str, verbose: bool=False) -> None:
    json_files = glob.glob(str(Path(data_dir) / '*.json'))
    df_all = pd.DataFrame()
    for i, file in enumerate(json_files):
        with open(file) as f:
            content = json.load(f)
            for yt_id in content:
                # print(content)
                df = pd.DataFrame([content[yt_id]])
                # if verbose:
                #     print(f"All columns size : {len(df_all.columns)}")
                #     print(f"New element columns size : {len(df.columns)}")
                #     print(f"Number of new columns added : {len(df.columns.difference(df_all.columns))}")
                #     print("New columns :")
                #     print(str(df.columns.difference(df_all.columns)))
                df_all = pd.concat([df_all, df], sort=True)
                if verbose:
                    print(f"Iteration {i}", f"Number of vids {len(df_all)}")
            if not i%5 and i>0:
                if verbose:
                    print("Writing DataFrame to csv...")
                    print(df_all)
                df_all.to_csv(out_dir + "batch" + str(i) + ".csv", index=False)
                # print(df_all)
                df_all = pd.DataFrame()


def plot_graphs(
    input_data: pd.DataFrame, 
    save_graph: bool=False,
    close_graph: bool=False,
    graph_dir: str="./data/graphs/", 
    graph_name: str=None,
    figsize=(20, 20),
    title: str=None
    ):

    # Convert to datetime
    input_data['uploaded'] = input_data['uploaded'].apply(lambda x: dt.datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))

    # Select valid columns
    input_data_cols = input_data.columns
    input_data_cols = input_data_cols[input_data_cols.values != 'channel_id']
    input_data_cols = input_data_cols[input_data_cols.values != 'uploaded']

    input_data.plot(x='uploaded', y=input_data_cols.tolist(), figsize=figsize, subplots=True, title=title)

    if graph_name is None:
        graph_name = int(dt.datetime.now().timestamp())
    
    if save_graph:
        plt.savefig(graph_dir + str(graph_name) + ".png")

    if close_graph:
        plt.close()


def load_data_2020(csv_dir: str, verbose: bool=False):
    csv_files = glob.glob(str(Path(csv_dir) / '*.csv'))
    df_all = pd.DataFrame()

    for file in csv_files:
        print(file)
        df_temp = pd.read_csv(file, lineterminator='\n')
        if verbose:
            print(f"All columns size : {len(df_all.columns)}")
            print(f"New element columns size : {len(df_temp.columns)}")
            print(f"Number of new columns added : {len(df_temp.columns.difference(df_all.columns))}")
            print("New columns :")
            print(str(df_temp.columns.difference(df_all.columns)))

        df_all = pd.concat([df_all, df_temp], sort=True)

    return df_all
