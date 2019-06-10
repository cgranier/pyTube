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

PLAYLISTS = ['PLM21IsezPrtpUGmOv_qYTWESf8jLPJ4bN',
            'PLM21IsezPrtqj0G_yBNnFXM8-XbdWwn0L',
            'PLM21IsezPrto27mG0ytAH8CGPxW_JmcwL',
            'PLM21IsezPrtrqzOfnhkC_DCo2WOaE9NNj',
            'PLM21IsezPrtolOathl8qDBG_q7JgxjZCr',
            'PLM21IsezPrtrBBSaclwpXsD-SSZfruRFY',
            'PLM21IsezPrtoMJEnYB7kzOm3TktWpzspK',
            'PLM21IsezPrtpIIoEnPf_Qj5pTB_Pwujvr',
            'PLM21IsezPrto5uyYNsnqjiiPRwwLppIMa',
            'PLM21IsezPrtqeOf5pBJ-DhblJgFjG-zLx',
            'PLM21IsezPrtrVQF825CaZNojRjqAgZTNB',
            'PLM21IsezPrtqJD1i2QMeHcBNxX-Wxnw7v',
            'PLM21IsezPrtpzA0jHb9SDdV_l01UQMskx',
            'PLM21IsezPrtrV3UyHPlsVs-7ON_NB-R0F',
            'PLM21IsezPrtqrmVV2zweRviD4s0Dp2lEi',
            'PLM21IsezPrtqxwqtRpWPNvXfzEB29NF-w',
            'PLM21IsezPrtoVrfNOScTe6DwFFpM6aRCy',
            'PLM21IsezPrtpxwIbLV_YYRGG5nob4bO5Z',
            'PLM21IsezPrtpVOF02RZqmNuEJIuekohvR',
            'PLM21IsezPrtrFX24Oun2bMu3SbGtCWipD',
            'PLM21IsezPrtqqpnOh21MbVepGtx1qm-b_',
            'PLM21IsezPrtoVw2aFtxm9bqb0fOumkqGL',]

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

        playlist_outfile = playlist_id + '_description.csv'
        with open(playlist_outfile, 'w', newline='', encoding='utf-8') as new_file:
            out_file_headers = ['video_id',
                                'video_title',
                                'video_description',
                                'video_playlist',
                                'playlist_item_id',
                                'video_position',
                                'video_episode',
                                'video_url',
            ]
            out_writer = csv.DictWriter(new_file, fieldnames = out_file_headers)
            out_writer.writeheader()

            for video in video_list:
                out_writer.writerow(video)
                print(video)

    print(f'Program done!')

if __name__ == "__main__":
    main()