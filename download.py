"""
Try to download youtube videos
"""
import youtube_dl as yt
import pandas as pd
import time

csv_path = './data/data_all.csv'
base_url = 'https://www.youtube.com/watch?v='

test_url = ['https://www.youtube.com/watch?v=IjbpENW5_G8']

ytdl = yt.YoutubeDL()

df = pd.read_csv(csv_path)
url_list = df['yt_id'].apply(lambda x: base_url + str(x)).iloc[0:5000].tolist()
nb_unavailable = 0
time_start = time.time()
for url in url_list:
    try:
        ytdl.download([url])
    except Exception as e:
        print(f"{url} video is unavailable, skipping it")
        nb_unavailable += 1
print(f"Number of skipped videos : {nb_unavailable}")
print(f"Processing time {time.time() - time_start}")
