"""
Try to download youtube videos

Youtube download format options

format code  extension  resolution note
249          webm       audio only tiny   47k , opus @ 47k (48000Hz), 8.55MiB
250          webm       audio only tiny   59k , opus @ 59k (48000Hz), 10.67MiB
251          webm       audio only tiny  106k , opus @106k (48000Hz), 19.17MiB
140          m4a        audio only tiny  129k , mp4a.40.2@129k (44100Hz), 23.21MiB
394          mp4        256x144    144p   74k , av01.0.00M.08@  74k, 25fps, video only, 13.36MiB
160          mp4        256x144    144p   84k , avc1.4d400c@  84k, 25fps, video only, 15.13MiB
278          webm       256x144    144p   89k , vp9@  89k, 25fps, video only, 16.09MiB
395          mp4        426x240    240p  153k , av01.0.00M.08@ 153k, 25fps, video only, 27.44MiB
133          mp4        426x240    240p  168k , avc1.4d4015@ 168k, 25fps, video only, 30.20MiB
242          webm       426x240    240p  169k , vp9@ 169k, 25fps, video only, 30.42MiB
396          mp4        640x360    360p  273k , av01.0.01M.08@ 273k, 25fps, video only, 48.94MiB
243          webm       640x360    360p  290k , vp9@ 290k, 25fps, video only, 52.04MiB
134          mp4        640x360    360p  315k , avc1.4d401e@ 315k, 25fps, video only, 56.54MiB
244          webm       854x480    480p  435k , vp9@ 435k, 25fps, video only, 78.14MiB
135          mp4        854x480    480p  450k , avc1.4d401e@ 450k, 25fps, video only, 80.83MiB
397          mp4        854x480    480p  471k , av01.0.04M.08@ 471k, 25fps, video only, 84.44MiB
136          mp4        1280x720   720p  662k , avc1.4d401f@ 662k, 25fps, video only, 118.75MiB
247          webm       1280x720   720p  718k , vp9@ 718k, 25fps, video only, 128.80MiB
398          mp4        1280x720   720p  936k , av01.0.05M.08@ 936k, 25fps, video only, 167.94MiB
399          mp4        1920x1080  1080p 1634k , av01.0.08M.08@1634k, 25fps, video only, 293.02MiB
248          webm       1920x1080  1080p 1867k , vp9@1867k, 25fps, video only, 334.78MiB
137          mp4        1920x1080  1080p 2034k , avc1.640028@2034k, 25fps, video only, 364.67MiB
18           mp4        640x360    360p  610k , avc1.42001E, 25fps, mp4a.40.2 (44100Hz), 109.46MiB
22           mp4        1280x720   720p  791k , avc1.64001F, 25fps, mp4a.40.2 (44100Hz) (best)

"""
import youtube_dl as yt
import pandas as pd
import time
import argparse
from pathlib import Path
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Youtube video download code.')
parser.add_argument('--test-url', help='Youtube video url to test',
                    default='https://www.youtube.com/watch?v=M0r9gRrzFMQ')
parser.add_argument('-t', '--test', action='store_true', help='Run script in test mode.')
parser.add_argument('--base-url', help='Root youtube url without video id.',
                    default='https://www.youtube.com/watch?v=')
parser.add_argument('--data-path', help='Path/to/data/folder',
                    default='./data_wizdeo/')
parser.add_argument('--csv-name', help='Name of the csv containing the data.',
                    default='data_all.csv')
parser.add_argument('-n', '--nb-vids', type=int, help="Number of videos to download.",
                    default=5000)

args = parser.parse_args()

# Define YTDL options
opts = {
    "format": '18',
    "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitleslangs": {
        "fr",
    }
}

ytdl = yt.YoutubeDL(opts)

if args.test:
    ytdl.download([args.test_url])
else:
    df = pd.read_csv(str(Path(args.data_path) / args.csv_name))
    url_list = df['yt_id'].apply(lambda x: args.base_url + str(x)).iloc[0:args.nb_vids].tolist()
    nb_unavailable = 0
    time_start = time.time()
    for url in tqdm(url_list):
        try:
            ytdl.download([url])
        except Exception as e:
            print(f"{url} video is unavailable, skipping it")
            nb_unavailable += 1
    print(f"Number of skipped videos : {nb_unavailable}")
    print(f"Processing time {time.time() - time_start}")
