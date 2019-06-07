import json
import sys
import googleapiclient.discovery
import googleapiclient.errors
import urllib.request
import csv
import config

# Documentation
# https://github.com/dsebastien/youtubeChannelVideosFinder/blob/master/youtubeChannelVideosFinder.py
# https://stackoverflow.com/questions/15512239/python-get-all-youtube-video-urls-of-a-channel

# Constants
api_key = config.api_key

# REST Command
# GET https://www.googleapis.com/youtube/v3/videos?part=id%2Csnippet&id=vCdEfUueb3s&key=APIKEY

# Strings

# youtubeChannelsApiUrl = youtubeApiUrl + 'channels?key={0}&'.format(api_key)
# youtubeSearchApiUrl = youtubeApiUrl + 'search?key={0}&'.format(api_key)
# requestChannelVideosInfo = youtubeSearchApiUrl + 'channelId={0}&part=id,snippet&order=date&type=video&pageToken={1}&maxResults=50'
# requestVideoStats = youtubeVideoApiUrl + 'id={0}&part=statistics'

youtubeApiUrl = 'https://www.googleapis.com/youtube/v3/'
youtubeVideoApiUrl = youtubeApiUrl + 'videos?key={0}&'.format(api_key)
requestVideoInfo = youtubeVideoApiUrl + 'id={0}&part=id,snippet'
youtubeVideoUrl = 'https://www.youtube.com/watch?v={0}'

# For testing. Use a csv to read all the videos to process.
# video_list = ['--B7mjgLig0','--LER3VU_os','--MpLvU70-Q','--Ym3GZEmx4']

def getVideoURL(videoId):
    retVal = youtubeVideoUrl.format(videoId)
    return retVal

def main():

    # in_file: a CSV file with one column (video_id) of video ids corresponding
    # to the video's whose metadata you want to download.
    # out_file: a CSV file with the videos' metadata.

    in_file = 'loco-video-loco-to-download-metadata.csv'
    out_file = 'lvl-video-descriptions.csv'

    with open(in_file, 'r', encoding='utf-8') as video_ids_file:
        video_ids = csv.DictReader(video_ids_file)
    
        with open(out_file, 'w', newline='', encoding='utf-8') as new_file:
            out_file_headers = ['video_id','channel_id','channel_title','video_title','video_description','video_keywords','video_url']
            out_writer = csv.DictWriter(new_file, fieldnames = out_file_headers)
            out_writer.writeheader()

            for video_line in video_ids:
                video_id = video_line['video_id']
                print(video_id)
                url = requestVideoInfo.format(video_id)
                response = urllib.request.urlopen(url)
                response_as_json = json.load(response)
                print(url)
                print(response)
                response.close()

                if response_as_json['items']:
                    channel_id = response_as_json['items'][0]['snippet']['channelId']
                    channel_title = response_as_json['items'][0]['snippet']['channelTitle']
                    # If tag is empty, assign empty string to variable
                    video_title = response_as_json['items'][0]['snippet']['title'] or ''
                    video_description = response_as_json['items'][0]['snippet']['description'] or ''
                    # Check for the existence of the 'tags' key
                    if 'tags' in response_as_json['items'][0]['snippet']:
                        video_keywords = ('|'.join(response_as_json['items'][0]['snippet']['tags']) or '')
                    else:
                        video_keywords = ''
                    video_url = getVideoURL(video_id)

                    data_row = {
                        'video_id':video_id,
                        'channel_id':channel_id,
                        'channel_title':channel_title,
                        'video_title':video_title,
                        'video_description':video_description,
                        'video_keywords':video_keywords,
                        'video_url':video_url
                    }
                    out_writer.writerow(data_row)

if __name__ == '__main__':
    main()
