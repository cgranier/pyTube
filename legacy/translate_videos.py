# The purpose of this script is to add metadata to YouTube videos in different languages
# Based on this comment: https://stackoverflow.com/a/40870843/469449
#
# PUT https://www.googleapis.com/youtube/v3/videos?part=localizations&key={YOUR_API_KEY}
#
# {
#  "id": "kE7dYgd3F8E",  //https://www.youtube.com/edit?video_id=kE7dYgd3F8E
#  "localizations": {
#   "es-do": {           //local codes, http://www.science.co.il/Language/Locale-codes.php
#    "title": "Translated title",
#    "description": "Translated description"
#   }
#  }
# }
#
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import csv

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

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

    in_file = 'loco-video-loco-to-download-metadata_1.csv'

    with open(in_file, 'r', encoding='utf-8') as video_ids_file:
        video_ids = csv.DictReader(video_ids_file)

        for video_line in video_ids:
            video_id = video_line['video_id']

            request = youtube.videos().update(
                part="localizations",
                body={
                "id": video_id,
                "localizations": {
                    "en": {
                    "title":"Loco Video Loco",
                    "description": "The most fun videos in one place! Subscribe to watch new videos every day!"
                    }
                },
                }
            )
            response = request.execute()

            print(response)

if __name__ == "__main__":
    main()
