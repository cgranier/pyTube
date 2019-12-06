# -*- coding: utf-8 -*-

import json
import re
import config

import csv
import pandas as pd
import dailymotion

import argparse

        # d.post('/videos', {'url' : url,
        #                     'title' : 'my_test_upload_%s' % time.strftime("%c"),
        #                     'published' : 'true',
        #                     'channel' : 'news'
        #                 })

parser = argparse.ArgumentParser(description='Update video metadata using a CSV.')
parser.add_argument('csv_file', type=str, help='CSV file with metadata')

args = parser.parse_args()

CSV_FILE = args.csv_file
DEST_PATH = ''
DM_PLAYLIST_API = '/video/{0}'

d = dailymotion.Dailymotion()

api_key = config.CLIENT_ID
api_secret = config.CLIENT_SECRET
api_username = config.USERNAME
api_password = config.PASSWORD
api_url = config.BASE_URL

d.set_grant_type('password', api_key, api_secret,
    scope=['userinfo'], info={'username': api_username, 'password': api_password})

def read_from_csv(csv_file):
    video_df = pd.read_csv(csv_file, encoding='utf-8')
    return video_df

def main():
    video_df = read_from_csv(CSV_FILE)
    print(video_df)

if __name__ == "__main__":
    main()
