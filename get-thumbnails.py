# -*- coding: utf-8 -*-

import urllib
import pandas as pd

import argparse

parser = argparse.ArgumentParser(description='Update video metadata using a CSV.')
parser.add_argument('csv_file', type=str, help='CSV file with metadata')

args = parser.parse_args()

CSV_FILE = args.csv_file

def read_from_csv(csv_file):
    video_df = pd.read_csv(csv_file, encoding='utf-8')
    return video_df

def download_thumbnail(video_df):
    for row in video_df.itertuples(index=False, name='video_to_update'):
        video_id = getattr(row, 'video_id')
        print(f'Downloading {video_id}')
        video_playlist = getattr(row, 'video_playlist')
        video_episode = getattr(row, 'video_episode')
        url= f'http://i3.ytimg.com/vi/{video_id}/mqdefault.jpg'
        urllib.request.urlretrieve(url, f'thumbnails/{video_playlist}_{video_id}_{video_episode}.jpg')

def main():
    video_df = read_from_csv(CSV_FILE)
    download_thumbnail(video_df)

if __name__ == "__main__":
    main()