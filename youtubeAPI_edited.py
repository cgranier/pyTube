# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json
import sys

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import config

import urllib.request
import csv

content_owner = config.content_owner
api_key = config.api_key

# Strings
youtubeApiUrl = 'https://www.googleapis.com/youtube/v3/'
# youtubeChannelsApiUrl = youtubeApiUrl + 'channels?key={0}&'.format(api_key)
# youtubeSearchApiUrl = youtubeApiUrl + 'search?key={0}&'.format(api_key)
# requestChannelVideosInfo = youtubeSearchApiUrl + 'channelId={0}&part=id,snippet&order=date&type=video&pageToken={1}&maxResults=50'
youtubeVideoUrl = 'https://www.youtube.com/watch?v={0}'
# youtubeVideoApiUrl = youtubeApiUrl + 'videos?key={0}&'.format(api_key)
# requestVideoStats = youtubeVideoApiUrl + 'id={0}&part=statistics'

# GET https://www.googleapis.com/youtube/v3/playlistItems?part=id%2C+snippet&maxResults=50&playlistId=PLD89ABDD950A3E5E5&key={YOUR_API_KEY}
# youtubePlaylistApiUrl = youtubeApiUrl + 'playlistItems?onBehalfOfContentOwner={0}&key={1}&'.format(content_owner,api_key)
youtubePlaylistApiUrl = youtubeApiUrl + 'playlistItems?onBehalfOfContentOwner={0}&'.format(content_owner)
requestPlaylistVideos = youtubePlaylistApiUrl + 'playlistId={0}&part=id,snippet&pageToken={1}&maxResults=50'


# Playlist ID
playlist_list = ['PLM21IsezPrtqXOQ-vAZ0XRP0i_SLrzxSK']
playlist_outFile = 'angelica-pecado.csv'

# youtubepartner scope is need in order to use onBehalfOfContentOwner
scopes = ["https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner",
          "https://www.googleapis.com/auth/youtubepartner-content-owner-readonly",
          "https://www.googleapis.com/auth/youtube.force-ssl",]

def getPlaylistVideos(playlistID):

    # initialization
    retVal = []
    found_all = False
    next_page_token = ''

    while not found_all:
        try:
            print('We\'re looking for them...')
            print('PlaylistID: {0}'.format(playlistID))
            url = requestPlaylistVideos.format(playlistID,next_page_token)
            print(url)
            response = urllib.request.urlopen(url)
            print(response)
            response_as_json = json.load(response)

            response.close()

            returned_videos = response_as_json['items']

            for video in returned_videos:
                retVal.append(video)
            
            try:
                next_page_token = response_as_json['nextPageToken']
            except Exception:
                found_all = True

        except Exception:
            found_all = True
            print('We found them all!')

    return retVal

def getVideoURL(videoId):
    retVal = youtubeVideoUrl.format(videoId)
    return retVal

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    out_file = playlist_outFile
    with open(out_file, 'w', newline='', encoding='utf-8') as new_file:
        out_file_headers = ['playlistItemId','videoId','videoTitle','videoURL','videoPosition']
        out_writer = csv.DictWriter(new_file, fieldnames = out_file_headers)
        out_writer.writeheader()

        for playlistId in playlist_list:
            playlistVideos = getPlaylistVideos(playlistId)
            videoURLs = []
            for video in playlistVideos:
                playlistItemId = video.get('id')
                videoId = video.get('snippet').get('resourceId').get('videoId')
                videoTitle = video.get('snippet').get('title')
                videoURL = getVideoURL(videoId)
                videoPosition = video.get('snippet').get('position')
                # videoViews = getVideoStats(videoId)
                # videoURLs.append(videoURL)

                data_row = {'playlistItemId':playlistItemId,'videoId':videoId,'videoTitle':videoTitle,'videoURL':videoURL, 'videoPosition':videoPosition}
                out_writer.writerow(data_row)
                
                print('{0},{1},{2},{3},{4}'.format(playlistItemId,videoId,videoTitle,videoURL,videoPosition))

    # request = youtube.playlistItems().list(
    #     part="id,snippet",
    #     onBehalfOfContentOwner=content_owner,
    #     playlistId="PLM21IsezPrtqXOQ-vAZ0XRP0i_SLrzxSK"
    # )
    # response = request.execute()

    # print(response)

if __name__ == "__main__":
    main()