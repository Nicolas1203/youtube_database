import pandas as pd
import glob
import json
from pathlib import Path
from utils.utils import json_to_csv

ROOT = '/home/nicolas/Documents/thesis/youtube_database/data'
DATA_DIR_2020 = ROOT + "/videos_2020/"

json_to_csv(DATA_DIR_2020, "/home/nicolas/Documents/thesis/youtube_database/data/videos_2020/csv/", verbose=True)