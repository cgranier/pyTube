# -*- coding: utf-8 -*-

import os
import sys

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import config
import re
import json
import csv
import pandas as pd

# INPUT DATA
# Create a playlists.py file and add a list of all the playlists you wish to process
# e.g., PLAYLISTS = ['PLM21IsezPrtrQvZ__EbQ0C1Nj2i5KjHyk',]

import playlists

# OAUTH
# youtubepartner scope is needed in order to use onBehalfOfContentOwner

CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_playlist_videos(service, PLAYLIST_ID):
    playlistVideos = []
    next_page_token = 'FIRST'

    while next_page_token != '':
        if next_page_token == 'FIRST':
            next_page_token = ''
        request = service.playlistItems().list(
        part="id,snippet",
        onBehalfOfContentOwner=config.content_owner,
        playlistId=PLAYLIST_ID,
        maxResults=50,
        pageToken=next_page_token,
        )
        response = request.execute()
        try:
            next_page_token = response['nextPageToken']
        except Exception:
            next_page_token = ''
        for video in response['items']:
            playlistVideos.append(video)

    return(playlistVideos)

def get_video_list(playlist_videos):
    video_list = []

    for video in playlist_videos:
        playlist_item_id = video.get('id')
        video_id = video.get('snippet').get('resourceId').get('videoId')
        video_title = video.get('snippet').get('title')
        video_url = 'https://www.youtube.com/watch?v={0}'.format(video_id)
        video_position = int(video.get('snippet').get('position'))
        # Episode titles are in the form:
        # La Trepadora | Episodio 1 | Norkys Batista y Jean Paul Leroux | Telenovelas RCTV
        # This regex extracts the word 'Episodio' followed by a space into group(1)
        # Then extracts the digits into group(2)
        # Then extracts a space followed by a vertical character into group(3)
        # We then assign group(2) -the episode number- into video_episode.
        video_episode = int(re.search('(Episodio\s)(\d+)(\s\|)',video_title).group(2))

        data_row = {'playlist_item_id':playlist_item_id,'video_id':video_id,'video_title':video_title,'video_url':video_url, 'video_position':video_position, 'video_episode':video_episode}
        
        video_list.append(data_row)

    return(video_list)

def reorder_playlist_videos(service, **kwargs):
    results = service.playlistItems().update(
        **kwargs
    ).execute()

def main():
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()

    for playlist_id in PLAYLISTS:
        playlist_videos = get_playlist_videos(service, playlist_id)

        video_list = get_video_list(playlist_videos)

        video_df = pd.DataFrame(video_list).sort_values(by=['video_episode'])

        for row in video_df.itertuples(name='video_to_update'):
            reorder_playlist_videos(service,
                onBehalfOfContentOwner=config.content_owner,
                part="snippet",
                body={
                    "id": getattr(row, 'playlist_item_id'),
                    "snippet": {
                        "playlistId": playlist_id,
                        "position": getattr(row, 'video_episode') - 1,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": getattr(row, 'video_id')
                        }
                    }
                }
            )
            print_title = getattr(row, 'video_title')
            print(f'Successfuly ordered {print_title}')
        print(f'Successfuly ordered {playlist_id}')
    print(f'Program done!')

if __name__ == "__main__":
    main()