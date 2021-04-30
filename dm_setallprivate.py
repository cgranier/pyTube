# -*- coding: utf-8 -*-

# This script authenticates and sets all channel videos as PRIVATE.

import json
import re
import config

import csv
import dailymotion

# SETUP

d = dailymotion.Dailymotion()

api_key = config.CLIENT_ID
api_secret = config.CLIENT_SECRET
api_username = config.USERNAME
api_password = config.PASSWORD
api_url = config.BASE_URL

d.set_grant_type('password', api_key, api_secret,
    scope=['userinfo'], info={'username': api_username, 'password': api_password})

def get_videos():
    page = 1
    limit = 100
    videos = 0
    has_more = True

    while has_more:
        # GET https://api.dailymotion.com/videos?fields=id&limit=100
        response = d.get("/videos", {'fields': 'id', 'owners': 'rctv', 'page': page, 'limit': limit, 'private': 'false'})
        for video in response['list']:
            # POST https://api.dailymotion.com/video/x80zn8m?private=true
            print(video['id'])
            privatize = d.post("/video/{0}".format(video['id']), {'private': 'true', 'fields': 'private'})
            print(privatize)
            videos += 1
        page += 1
        print('page: ', page)
        print('videos: ', videos)
        has_more = response['has_more']

    return

def main():
    get_videos()

if __name__ == "__main__":
    main()