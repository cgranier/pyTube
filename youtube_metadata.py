# -*- coding: utf-8 -*-

import os
import sys
import pprint

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

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

    for video in playlist_videos:

        # From playlist_videos we get:
        playlist_id = video.get('playlistId')
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
        for single_video in metadata['items']:
            channel_name = single_video.get('snippet').get('channelTitle')
            channel_id = single_video.get('snippet').get('channelId')
            video_title = single_video.get('snippet').get('title')
            video_description = single_video.get('snippet').get('description')
            video_tags = ('|'.join(single_video.get('snippet').get('tags')))
            
            video_published_at = single_video.get('snippet').get('publishedAt')
            video_default_language = single_video.get('snippet').get('defaultLanguage')
            video_default_audio_language = single_video.get('snippet').get('defaultAudioLanguage')
            video_duration = single_video.get('contentDetails').get('duration')
            video_privacy_status = single_video.get('status').get('privacyStatus')
            video_file_details = single_video.get('fileDetails').get('fileName')


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

    for playlist_id in PLAYLISTS:
        playlist_videos = get_playlist_videos(service, playlist_id)
        video_list = get_video_metadata(service, playlist_videos)
        video_df = pd.DataFrame(video_list)
        create_ordered_csv(playlist_id, video_df)

if __name__ == "__main__":
    main()