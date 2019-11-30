# -*- coding: utf-8 -*-

import json
import re
import config

import csv
import pandas as pd
import dailymotion

import playlists
PLAYLISTS = playlists.DAILYMOTION
# PLAYLISTS = ['_']

# SETUP

d = dailymotion.Dailymotion()

api_key = config.CLIENT_ID
api_secret = config.CLIENT_SECRET
api_username = config.USERNAME
api_password = config.PASSWORD
api_url = config.BASE_URL

d.set_grant_type('password', api_key, api_secret,
    scope=['userinfo'], info={'username': api_username, 'password': api_password})

dm_playlist_API = '/playlist/{0}/videos'

def get_playlist_videos(PLAYLIST_ID):
    playlist_videos = []
    page = 1
    limit = 100
    has_more = True

    while has_more:
        response = d.get(dm_playlist_API.format(PLAYLIST_ID), {'fields': 'id,title,url,description', 'page': page, 'limit': limit})
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
        if 'Episodio' in video_title:
            video_episode = int(re.search('(Episodio\s)(\d+)(\s\|)',video_title).group(2))
        elif 'Episode' in video_title:
            video_episode = int(re.search('(Episode\s)(\d+)(\s\|)',video_title).group(2))
        else:
            sys.exit('Non-standard title format - reorder by hand.')
        
        data_row = {'video_id':video_id,'video_title':video_title,'video_url':video_url,'video_episode':video_episode,'video_description':video_description}
        video_list.append(data_row)

    return video_list

def reorder_videos(playlist_id, video_ids):
    # Thanks to Reddit user https://www.reddit.com/user/semicolonator/
    # for his help with this code to create the API call
    videos_in_order = {'ids': ",".join(["%s" % i for i in video_ids])}
    order_api = d.post(dm_playlist_API.format(playlist_id), videos_in_order)
    print(f'Playlist {playlist_id} ordered!')
    return

def create_ordered_csv(playlist_id, video_df):
    csv_filename = 'dm_playlist_{0}.csv'.format(playlist_id)
    video_df.to_csv(csv_filename, encoding='utf-8', header = True, index = None)
    print(f'Ordered playlist {playlist_id} saved to csv file {csv_filename}!')
    return

def main():
    for playlist in PLAYLISTS:
        playlist_videos = get_playlist_videos(playlist)
        video_list = get_video_list(playlist_videos)
        video_df = pd.DataFrame(video_list).sort_values(by=['video_episode'])
        video_ids = video_df['video_id'].tolist()
        reorder_videos(playlist, video_ids)
        create_ordered_csv(playlist, video_df)

if __name__ == "__main__":
    main()