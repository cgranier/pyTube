# -*- coding: utf-8 -*-

import json
import re
import config

import csv
import pandas as pd
import dailymotion

import playlists

# First version - no functions, etc.

# SETUP

d = dailymotion.Dailymotion()

api_key = config.CLIENT_ID
api_secret = config.CLIENT_SECRET
api_username = config.USERNAME
api_password = config.PASSWORD
api_url = 'https://api.dailymotion.com/'
d.set_grant_type('password', api_key, api_secret,
    scope=['userinfo'], info={'username': api_username, 'password': api_password})
    
# Get a list of videos in a Playlist
# this one reorders the playlist [https://stackoverflow.com/questions/59040674/how-to-reorder-a-playlist]
# d.post('/playlist/{PLAYLIST_ID}/videos', {'ids' : '{VIDEO_ID},...,{VIDEO_ID}'})

playlist_id = 'x6f0b9'
videos = d.get('/playlist/x6f0b9/videos', {'fields': 'id,title,url'})

print(json.dumps(videos))