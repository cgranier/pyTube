# -*- coding: utf-8 -*-

import os
import sys
import pprint

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from tqdm import tqdm

import config
import re
import json
import csv
import pandas as pd

import playlists
PLAYLISTS = playlists.PLAYLISTS

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

def get_video_metadata(service,playlist_videos):
    video_list = []
    metadata = []

    for video in tqdm(playlist_videos):

        # From playlist_videos we get:
        playlist_id = video.get('snippet').get('playlistId')
        playlist_item_id = video.get('id')
        video_id = video.get('snippet').get('resourceId').get('videoId')
        video_position = int(video.get('snippet').get('position'))
        
        request = service.videos().list(
            part="id,snippet,contentDetails,status,fileDetails",
            onBehalfOfContentOwner=config.content_owner,
            id=video_id
        )
        metadata = request.execute()

        # From metadata we get:
        channel_name = metadata['items'][0]['snippet']['channelTitle']
        channel_id = metadata['items'][0]['snippet']['channelId']
        video_title = metadata['items'][0]['snippet']['title']
        video_description = metadata['items'][0]['snippet']['description']
        video_tags = ('|'.join(metadata['items'][0]['snippet']['tags']))
        video_published_at = metadata['items'][0]['snippet']['publishedAt']
        video_default_language = metadata['items'][0]['snippet']['defaultLanguage']
        video_default_audio_language = metadata['items'][0]['snippet']['defaultAudioLanguage']
        video_duration = metadata['items'][0]['contentDetails']['duration']
        video_privacy_status = metadata['items'][0]['status']['privacyStatus']
        video_file_details = metadata['items'][0]['fileDetails']['fileName']

        data_row = {'playlist_id':playlist_id,
                    'playlist_item_id':playlist_item_id,
                    'channel_id':channel_id,
                    'channel_name':channel_name,
                    'video_id':video_id,
                    'video_title':video_title,
                    'video_position':video_position,
                    'video_description':video_description,
                    'video_tags':video_tags,
                    'video_published_at':video_published_at,
                    'video_default_language':video_default_language,
                    'video_default_audio_language':video_default_audio_language,
                    'video_duration':video_duration,
                    'video_privacy_status':video_privacy_status,
                    'video_file_details':video_file_details
        }
        
        video_list.append(data_row)

    return(video_list)

def create_ordered_csv(playlist_id, video_df):
    csv_filename = 'youtube_playlist_metadata_{0}.csv'.format(playlist_id)
    video_df.to_csv(csv_filename, encoding='utf-8', header = True, index = None)
    print(f'Metadata for videos in playlist {playlist_id} saved to csv file {csv_filename}!')
    return

def main():
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()

    for playlist_id in tqdm(PLAYLISTS):
        playlist_videos = get_playlist_videos(service, playlist_id)
        print(f'Found all videos for playlist {playlist_id}.')
        video_list = get_video_metadata(service, playlist_videos)
        print(f'Retrieved all metadata for videos in playlist {playlist_id}.')
        video_df = pd.DataFrame(video_list)
        print(f'Creating CSV file for playlist {playlist_id}.')
        create_ordered_csv(playlist_id, video_df)
        print(f'Done with playlist {playlist_id}.')

if __name__ == "__main__":
    main()