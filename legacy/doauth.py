import os
import pprint
import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import config

pp = pprint.PrettyPrinter(indent=2)

CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner"]

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

PLAYLIST_ID = 'PLM21IsezPrtqDqn1-t9s-NPXc-w1nFZpC'

PLAYLIST_ITEM_ID = 'UExNMjFJc2V6UHJ0cURxbjEtdDlzLU5QWGMtdzFuRlpwQy4wNEU1MTI4NkZEMzVBN0JF'
VIDEO_NEW_ORDER = 1
VIDEO_ID = 'Uh8NmVK-gUM'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def list_playlist_videos(service, **kwargs):
    results = service.playlistItems().list(
        **kwargs
    ).execute()

    pp.pprint(results)

def reorder_playlist_videos(service, **kwargs):
    results = service.playlistItems().update(
        **kwargs
    ).execute()

    pp.pprint(results)

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    # list_playlist_videos(service,
    #                    part="id,snippet",
    #                    onBehalfOfContentOwner=config.content_owner,
    #                    playlistId=PLAYLIST_ID,
    #                    maxResults=50,)
    reorder_playlist_videos(service,
                            onBehalfOfContentOwner=config.content_owner,
                            part="snippet",
                            body={
                                "id": PLAYLIST_ITEM_ID,
                                "snippet": {
                                    "playlistId": PLAYLIST_ID,
                                    "position": VIDEO_NEW_ORDER,
                                    "resourceId": {
                                        "kind": "youtube#video",
                                        "videoId": VIDEO_ID
                                    }
                                }
                            }
    )
