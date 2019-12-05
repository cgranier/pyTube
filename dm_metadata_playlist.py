# -*- coding: utf-8 -*-

import json
import re
import config

import csv
import pandas as pd
import dailymotion

import argparse

parser = argparse.ArgumentParser(description='Download metadata from one playlist to CSV.')
parser.add_argument('playlist_id', type=str, help='Dailymotion Playlist ID to download')

args = parser.parse_args()

PLAYLIST_ID = args.playlist_id
DEST_PATH = ''
DM_PLAYLIST_API = '/playlist/{0}/videos'

d = dailymotion.Dailymotion()

api_key = config.CLIENT_ID
api_secret = config.CLIENT_SECRET
api_username = config.USERNAME
api_password = config.PASSWORD
api_url = config.BASE_URL

d.set_grant_type('password', api_key, api_secret,
    scope=['userinfo'], info={'username': api_username, 'password': api_password})

def get_playlist_videos(PLAYLIST_ID):
    playlist_videos = []
    page = 1
    limit = 100
    has_more = True

    while has_more:
        response = d.get(DM_PLAYLIST_API.format(PLAYLIST_ID), {'fields': 'id,title,url,description', 'page': page, 'limit': limit})
        for video in response['list']:
            playlist_videos.append(video)
        page += 1
        has_more = response['has_more']

    return playlist_videos

def get_video_list(playlist_videos):
    video_list = []

    for video in playlist_videos:
        video_id = video.get('id')
        video_title = video.get('title')
        video_url = video.get('url')
        video_description = video.get('description')
        video_episode = 0
        
        data_row = {'video_id':video_id,'video_title':video_title,'video_url':video_url,'video_episode':video_episode,'video_description':video_description}
        video_list.append(data_row)

    return video_list

def create_ordered_csv(playlist_id, video_df):
    csv_filename = f'dm_playlist_{playlist_id}_metadata.csv'
    video_df.to_csv(csv_filename, encoding='utf-8', header = True, index = None)
    print(f'Ordered playlist {playlist_id} saved to csv file {csv_filename}!')
    return

def main():
    playlist_videos = get_playlist_videos(PLAYLIST_ID)
    video_list = get_video_list(playlist_videos)
    video_df = pd.DataFrame(video_list)
    create_ordered_csv(PLAYLIST_ID, video_df)

if __name__ == "__main__":
    main()