# -*- coding: utf-8 -*-

# WARNING: This code WILL DELETE YOUR VIDEOS PERMANENTLY

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
# For this version we need youtube.force-ssl scope in order to get delete access to the videos

CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_video_details(service, VIDEO_ID):
    request = service.videos().list(
        part = 'id,snippet,statistics,contentDetails,status,fileDetails',
        id = VIDEO_ID
    )

    response = request.execute()
    video_metadata = response['items'][0]
    # raw_tags = response['items'][0]['snippet']['tags']
    raw_tags = 'blank'

    video_tags = '|'.join(raw_tags)
    video_category = video_metadata['snippet']['categoryId']
    video_duration = video_metadata['contentDetails']['duration']
    video_privacy_status = video_metadata['status']['privacyStatus']
    video_filename = video_metadata['fileDetails']['fileName']

    # get video statistics
    video_statistics_view_count = video_metadata['statistics']['viewCount']
    video_statistics_like_count = video_metadata['statistics']['likeCount']
    video_statistics_dislike_count = video_metadata['statistics']['dislikeCount']
    video_statistics_favorite_count = video_metadata['statistics']['favoriteCount']
    video_statistics_comment_count = video_metadata['statistics']['commentCount']

    video_data_row = {'video_tags':video_tags,
                      'video_category':video_category,
                      'video_duration':video_duration,
                      'video_privacy_status':video_privacy_status,
                      'video_filename':video_filename,
                      'video_statistics_view_count':video_statistics_view_count,
                      'video_statistics_like_count':video_statistics_like_count,
                      'video_statistics_dislike_count':video_statistics_dislike_count,
                      'video_statistics_favorite_count':video_statistics_favorite_count,
                      'video_statistics_comment_count':video_statistics_comment_count}
    
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
        video_episode = 0
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

# delete the videos

def delete_video(service, VIDEO_ID):
    request = service.videos().delete(
        id = VIDEO_ID
    )
    print('inside delete function for ', VIDEO_ID)
    response = request.execute()
    return(response)

def main():
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()

    for playlist_id in PLAYLISTS:
        playlist_videos = get_playlist_videos(service, playlist_id)

        video_list = get_video_list(playlist_videos)

        playlist_outfile = 'pre-deletion_metadata_' + playlist_id + '_metadata.csv'
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
                                'video_duration',
                                'video_privacy_status',
                                'video_filename',
                                'video_statistics_view_count',
                                'video_statistics_like_count',
                                'video_statistics_dislike_count',
                                'video_statistics_favorite_count',
                                'video_statistics_comment_count',
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
                print('Deleting video ', {video.get('video_id')})
                video_delete = delete_video(service, video.get('video_id'))
                print(video_delete)
                print('-----------')

    print(f'Program done!')

if __name__ == "__main__":
    main()