import json
import sys
import googleapiclient.discovery
import googleapiclient.errors
import urllib.request
import csv
import config

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Documentation
# https://github.com/dsebastien/youtubeChannelVideosFinder/blob/master/youtubeChannelVideosFinder.py
# https://stackoverflow.com/questions/15512239/python-get-all-youtube-video-urls-of-a-channel

api_key = config.api_key

# Strings
youtubeApiUrl = 'https://www.googleapis.com/youtube/v3/'
youtubeChannelsApiUrl = youtubeApiUrl + 'channels?key={0}&'.format(api_key)
youtubeSearchApiUrl = youtubeApiUrl + 'search?key={0}&'.format(api_key)
requestChannelVideosInfo = youtubeSearchApiUrl + 'channelId={0}&part=id,snippet&order=date&type=video&pageToken={1}&maxResults=50'
youtubeVideoUrl = 'https://www.youtube.com/watch?v={0}'
youtubeVideoApiUrl = youtubeApiUrl + 'videos?key={0}&'.format(api_key)
requestVideoStats = youtubeVideoApiUrl + 'id={0}&part=statistics'

# GET https://www.googleapis.com/youtube/v3/playlistItems?part=id%2C+snippet&maxResults=50&playlistId=PLD89ABDD950A3E5E5&key={YOUR_API_KEY}
youtubePlaylistApiUrl = youtubeApiUrl + 'playlistItems?key={0}&'.format(api_key)
requestPlaylistVideos = youtubePlaylistApiUrl + 'playlistId={0}&part=id,snippet&pageToken={1}&maxResults=50'

#DEBUG
# print(youtubeApiUrl)
# print(youtubeChannelsApiUrl)
# print(requestChannelVideosInfo)
# print(youtubeVideoUrl)

# Playlist ID
playlist_list = ['PLM21IsezPrtqXOQ-vAZ0XRP0i_SLrzxSK']
playlist_outFile = 'angelica-pecado.csv'

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

# def getVideoStats(videoId):
#     url = requestVideoStats.format(videoId)
#     response = urllib.request.urlopen(url)
#     response_as_json = json.load(response)
#     response.close()
#     retVal = response_as_json['items'][0]['statistics']['viewCount']
#     return retVal

def main():

    # ****
    # Data needed:
    # Playlist to modify
    playlist_ID = ['PLM21IsezPrtpvlcm5UMj9X2ZsbUWzy-k6']
    # CSV file with order of videos - Use pyTubePlaylist.py to retrieve the videos initially
    ordered_videos_file = 'amantes-ordered.csv'

    # Read the ordered CSV file into memory
    video_file = pandas.read_csv(ordered_videos_file)

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
    # ****
    
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
                # print(video.get('snippet').get('description'))
            
            # for videoURL in videoURLs:
            #     print('Channel: {0}, Title: , URL: {1}'.format(channelId,videoURL))

if __name__ == '__main__':
    main()
