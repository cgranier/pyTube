# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import config

# Playlist ID
playlist_list = ['PLM21IsezPrtqXOQ-vAZ0XRP0i_SLrzxSK']
playlist_outFile = 'angelica-pecado.csv'

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

    request = youtube.playlistItems().list(
        part="id,snippet",
        onBehalfOfContentOwner=config.content_owner,
        playlistId="PLM21IsezPrtqXOQ-vAZ0XRP0i_SLrzxSK"
    )
    response = request.execute()

    print(request)

    print('***********************************')

    print(response)

if __name__ == "__main__":
    main()