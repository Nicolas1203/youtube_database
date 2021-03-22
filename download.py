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

TODO
* Move video / thumbnails downloaded
* Convert webp images to jpg
* Rename thumbnails

"""
import youtube_dl as yt
import pandas as pd
import time
import glob
import os
import sys
import argparse
from pathlib import Path
from tqdm import tqdm
from PIL import Image
from utils.utils import train_test_split


parser = argparse.ArgumentParser(description='Youtube video download code.')
parser.add_argument('--test-url', help='Youtube video url to test',
                    default='https://www.youtube.com/watch?v=M0r9gRrzFMQ')
parser.add_argument('-t', '--test', action='store_true', help='Run script in test mode.')
parser.add_argument('--base-url', help='Root youtube url without video id.',
                    default='https://www.youtube.com/watch?v=')
parser.add_argument('--data-path', help='Path/to/csv/folder',
                    default='./data_wizdeo/')
parser.add_argument('--csv-name', help='Name of the csv containing the data.',
                    default='data_all.csv')
parser.add_argument('-n', '--nb-vids', type=int, help="Number of videos to download.",
                    default=5000)
parser.add_argument('--shuffle', action='store_true', help="Download data in shuffled order.")
parser.add_argument('--seed', type=int, default=1, help="Random seed for data shuffling.")
parser.add_argument('-p', '--out-path', default='./thumbnails/', help='/Path/to/folder/for/storage/')
parser.add_argument('--split-only', action='store_true', 
                    help="Splits the data in a folder in 2 separate train/test folders.")
parser.add_argument('--skip', type=int, default=0, help="Skip the first N videos for download.")
parser.add_argument('--reconvert', action='store_true', help="Reconvert all images in case of loading errors")

args = parser.parse_args()

# Define YTDL options
opts = {
    "format": '18',
    # "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitleslangs": {
        "fr",
    },
    # "writethumbnail": 2,
    "skip_download": True
}


def main():
    if args.reconvert:
        reconvert()
        sys.exit(0)
    if args.split_only:
        train_test_split(args.out_path, 0.8)
        sys.exit(0)

    ytdl = yt.YoutubeDL(opts)

    if args.test:
        ytdl.download([args.test_url])
    else:
        df = pd.read_csv(str(Path(args.data_path) / args.csv_name))
        if args.shuffle:
            df = df.sample(frac=1, random_state=args.seed).reset_index(drop=True)
        url_list = df['yt_id'] \
                    .apply(lambda x: args.base_url + str(x)) \
                    .iloc[args.skip:args.skip + args.nb_vids].tolist()
        nb_unavailable = 0
        time_start = time.time()
        for idx, url in tqdm(enumerate(url_list)):
            try:    
                ytdl.download([url])
            except Exception:
                print(f"{url} video is unavailable, skipping it")
                nb_unavailable += 1
            if not idx % 1000:
                rename_and_move()
                convert_to_jpg()
        print(f"Number of skipped videos : {nb_unavailable}")
        print(f"Processing time {time.time() - time_start}")


def convert_to_jpg():
    """Convert every webp in the output folder to jpg.
    Webp format is not supported by most librairies, especially not DL libraires.
    """
    to_convert_webp = glob.glob(str(Path(args.out_path) / '*.webp'))
    for thumbnail in to_convert_webp:
        img = Image.open(thumbnail).convert('RGB')
        img.save(thumbnail[:-4] + 'jpg', 'jpeg')
        os.remove(thumbnail)


def reconvert():
    """Loads and convert again to JPG every image in the output directory. 
    This should be used only when there is unexpected loading errors.
    """
    to_convert = glob.glob(str(Path(args.out_path) / '*jpg'))
    for thumbnail in tqdm(to_convert):
        img = Image.open(thumbnail).convert('RGB')
        img.save(thumbnail[:22] + ".jpg", 'jpeg')


def rename_and_move():
    """Youtube DL  has no output directory parameters in the download method.
    I need ot manually move file in the desired folder.
    This function list, move, and at the ame time rename every image in the folder.
    The renaming pattern in <youtube_id>.jpg
    """
    to_rename_jpg = glob.glob("./*.jpg")
    for thumbnail in to_rename_jpg:
        new_vid_name = thumbnail[-15:]
        os.rename(thumbnail, str(Path(args.out_path) / new_vid_name))
    to_rename_webp = glob.glob("./*.webp")
    for thumbnail in to_rename_webp:
        new_vid_name = thumbnail[-16:]
        os.rename(thumbnail, str(Path(args.out_path) / new_vid_name))


if __name__ == '__main__':
    main()