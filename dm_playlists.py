# -*- coding: utf-8 -*-

import json
import re
import config

import csv
import pandas as pd
import dailymotion

import playlists
# PLAYLISTS = playlists.DAILYMOTION
PLAYLISTS = ['x6f0b9']

# First version - no functions, etc.

# SETUP

d = dailymotion.Dailymotion()

api_key = config.CLIENT_ID
api_secret = config.CLIENT_SECRET
api_username = config.USERNAME
api_password = config.PASSWORD
api_url = config.BASE_URL

d.set_grant_type('password', api_key, api_secret,
    scope=['userinfo'], info={'username': api_username, 'password': api_password})
    
# Get a list of videos in a Playlist
# this one reorders the playlist [https://stackoverflow.com/questions/59040674/how-to-reorder-a-playlist]
# d.post('/playlist/{PLAYLIST_ID}/videos', {'ids' : '{VIDEO_ID},...,{VIDEO_ID}'})

# playlist_id = 'x6f0b9'
# videos = d.get('/playlist/x6f0b9/videos', {'fields': 'id,title,url'})
# print(json.dumps(videos))

dm_get_playlist_API = '/playlist/{0}/videos'
# dm_get_playlist_fields = {'fields': 'id,title,url', 'page'}

def get_playlist_videos(PLAYLIST_ID):
    playlist_videos = []
    page = 1
    limit = 100
    has_more = True

    while has_more:
        response = d.get(dm_get_playlist_API.format(PLAYLIST_ID), { 'fields': 'id,title,url', 'page': page, 'limit': limit})
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
        if 'Episodio' in video_title:
            video_episode = int(re.search('(Episodio\s)(\d+)(\s\|)',video_title).group(2))
        elif 'Episode' in video_title:
            video_episode = int(re.search('(Episode\s)(\d+)(\s\|)',video_title).group(2))
        else:
            sys.exit('Non-standard title format - reorder by hand.')
        
        data_row = {'video_id':video_id,'video_title':video_title,'video_url':video_url,'video_episode':video_episode}
        video_list.append(data_row)

    return video_list

def main():
    for playlist in PLAYLISTS:
        playlist_videos = get_playlist_videos(playlist)
        for video in playlist_videos:
            video_id = video.get('id')
            video_title = video.get('title')
            video_url = video.get('url')
            print(f'Video id: {video_id} * Video title: {video_title} * Video url: {video_url}')

if __name__ == "__main__":
    main()