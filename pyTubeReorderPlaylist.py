import pandas
import urllib.request
import csv
import config
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import os

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
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

    for row in video_file.itertuples(name='VideoToUpdate'):
        # While I figure this one out, note that:
        # [0] = index
        # [1] = videoId
        # [2] = videoTitle
        # [3] = videoURL
        # [4] = videoPosition
        # playlist_item_id = row[1]
        # video_id = row[2]
        # video_new_order = row[6] - 1
        # video_position = row[5]
        playlist_item_id = getattr(row, 'playlistItemId')
        video_id = getattr(row, 'videoId')
        # Substract one from video_new_order, because playlist position is zero-based.
        video_new_order = getattr(row, 'episode') - 1

        request = youtube.playlistItems().update(
            part="snippet",
            body={
                "id": playlist_item_id,
                "snippet": {
                    "playlistId": playlist_ID,
                    "position": video_new_order,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        response = request.execute()

        print(response)

if __name__ == "__main__":
    main()