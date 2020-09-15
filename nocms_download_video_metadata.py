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

# This version should work when you don't have access to a Content Owner (MCN) account
# INPUT DATA

import playlists
PLAYLISTS = playlists.PLAYLISTS

# OAUTH
# youtubepartner scope is needed in order to use onBehalfOfContentOwner

CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


def get_video_details(service, VIDEO_ID):
    request = service.videos().list(
        part = 'id,snippet,contentDetails,status,fileDetails',
        id = VIDEO_ID
    )
        # id, snippet, contentDetails, status, fileDetails, suggestions, 
        # suggestions.tagSuggestions[]
        # suggestions.editorSuggestions[]
    response = request.execute()
    video_metadata = response['items'][0]
    raw_tags = response['items'][0]['snippet']['tags']

    video_tags = '|'.join(raw_tags)
    video_category = video_metadata['snippet']['categoryId']
    video_default_language = video_metadata['snippet']['defaultLanguage']
    video_default_audio_language = video_metadata['snippet']['defaultAudioLanguage']
    video_duration = video_metadata['contentDetails']['duration']
    video_licensed_content = video_metadata['contentDetails']['licensedContent']
    video_custom_thumbnail = video_metadata['contentDetails']['hasCustomThumbnail']
    video_default_thumbnail = video_metadata['snippet']['thumbnails']['default']['url']
    video_maxres_thumbnail = video_metadata['snippet']['thumbnails']['maxres']['url']
    video_upload_status = video_metadata['status']['uploadStatus']
    video_privacy_status = video_metadata['status']['privacyStatus']
    video_filename = video_metadata['fileDetails']['fileName']

    video_data_row = {'video_tags':video_tags,
                      'video_category':video_category,
                      'video_default_language':video_default_language,
                      'video_default_audio_language':video_default_audio_language,
                      'video_duration':video_duration,
                      'video_licensed_content':video_licensed_content,
                      'video_custom_thumbnail':video_custom_thumbnail,
                      'video_default_thumbnail':video_default_thumbnail,
                      'video_maxres_thumbnail':video_maxres_thumbnail,
                      'video_upload_status':video_upload_status,
                      'video_privacy_status':video_privacy_status,
                      'video_filename':video_filename}
    
    return(video_data_row)


def get_playlist_videos(service, PLAYLIST_ID):
    playlistVideos = []
    next_page_token = 'FIRST'

    while next_page_token != '':
        if next_page_token == 'FIRST':
            next_page_token = ''
        request = service.playlistItems().list(
        part="id,snippet",
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
        video_description = video.get('snippet').get('description')
        video_position = int(video.get('snippet').get('position'))
        video_playlist = video.get('snippet').get('playlistId')
        # Episode titles are in the form:
        # La Trepadora | Episodio 1 | Norkys Batista y Jean Paul Leroux | Telenovelas RCTV
        # This regex extracts the word 'Episodio' followed by a space into group(1)
        # Then extracts the digits into group(2)
        # Then extracts a space followed by a vertical character into group(3)
        # We then assign group(2) -the episode number- into video_episode.
        video_episode = int(re.search('(Episodio\s)(\d+)(\s\|)',video_title).group(2))
        video_url = 'https://www.youtube.com/watch?v={0}'.format(video_id)

        data_row = {'video_id':video_id,
                    'video_title':video_title,
                    'video_description':video_description,
                    'video_playlist':video_playlist,
                    'playlist_item_id':playlist_item_id,
                    'video_position':video_position,
                    'video_episode':video_episode,
                    'video_url':video_url,
        }
        
        video_list.append(data_row)

    return(video_list)


def main():
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()

    for playlist_id in PLAYLISTS:
        playlist_videos = get_playlist_videos(service, playlist_id)

        video_list = get_video_list(playlist_videos)

        playlist_outfile = 'fullmetadata_' + playlist_id + '_metadata.csv'
        with open(playlist_outfile, 'w', newline='', encoding='utf-8') as new_file:
            out_file_headers = ['video_id',
                                'video_title',
                                'video_description',
                                'video_playlist',
                                'playlist_item_id',
                                'video_position',
                                'video_episode',
                                'video_url',
                                'video_tags',
                                'video_category',
                                'video_default_language',
                                'video_default_audio_language',
                                'video_duration',
                                'video_licensed_content',
                                'video_custom_thumbnail',
                                'video_default_thumbnail',
                                'video_maxres_thumbnail',
                                'video_upload_status',
                                'video_privacy_status',
                                'video_filename',
            ]
            out_writer = csv.DictWriter(new_file, fieldnames = out_file_headers)
            out_writer.writeheader()

            for video in video_list:
                video_metadata = get_video_details(service, video.get('video_id'))
                video_output = {}
                video_output.update(video)
                video_output.update(video_metadata)
                out_writer.writerow(video_output)
                print(video_output)

    print(f'Program done!')

if __name__ == "__main__":
    main()