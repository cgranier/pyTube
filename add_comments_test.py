# -*- coding: utf-8 -*-

import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import config

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "client_secret.json"

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def main():
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()

    request = service.commentThreads().insert(
        part="snippet",
        body={
          "snippet": {
            "videoId": "kTrJjA9t6tY",
            "topLevelComment": {
              "snippet": {
                "textOriginal": "Hey Nick, check this out! Also, don't forget to subscribe for more videos: http://www.youtube.com/channel/UCD7l8UPl4xQ0h74pNiroSRw?sub_confirmation=1"
              }
            }
          }
        }
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()