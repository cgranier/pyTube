# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import sys

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import config
import re

import json
import csv

# Playlist ID
playlist_id = 'PLM21IsezPrtq1rvDBdmQLuJVPP1bKCnWu'
playlist_outFile = 'pura-sangre-2.csv'

# pura-sangre	PLM21IsezPrtq1rvDBdmQLuJVPP1bKCnWu

# youtubepartner scope is needed in order to use onBehalfOfContentOwner
scopes = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    out_file = playlist_outFile
    with open(playlist_outFile, 'w', newline='', encoding='utf-8') as new_file:
        out_file_headers = ['playlistItemId','videoId','videoTitle','videoURL','videoPosition','videoEpisode']
        out_writer = csv.DictWriter(new_file, fieldnames = out_file_headers)
        out_writer.writeheader()
        
        # playlistVideos = getPlaylistVideos(playlist_id)

        playlistVideos = []
        next_page_token = 'FIRST'

        while next_page_token != '':
            if next_page_token == 'FIRST':
                next_page_token = ''
            request = youtube.playlistItems().list(
            part="id,snippet",
            onBehalfOfContentOwner=config.content_owner,
            playlistId=playlist_id,
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

        for video in playlistVideos:
                playlistItemId = video.get('id')
                videoId = video.get('snippet').get('resourceId').get('videoId')
                videoTitle = video.get('snippet').get('title')
                # videoURL = getVideoURL(videoId)
                videoURL = 'https://www.youtube.com/watch?v={0}'.format(videoId)
                videoPosition = video.get('snippet').get('position')
                videoEpisode = re.search('(Episodio\s)(\d+)(\s\|)',videoTitle).group(2)

                data_row = {'playlistItemId':playlistItemId,'videoId':videoId,'videoTitle':videoTitle,'videoURL':videoURL, 'videoPosition':videoPosition, 'videoEpisode':videoEpisode}
                out_writer.writerow(data_row)
                
                print('{0},{1},{2},{3},{4},{5}'.format(playlistItemId,videoId,videoTitle,videoURL,videoPosition,videoEpisode))

if __name__ == "__main__":
    main()