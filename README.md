# pyTube #

pyTube exists to make managing large content libraries on YouTube a bit easier. It's also an excuse for coding, learning and doing boring stuff quickly.

![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)
![YouTube Data API V3](https://img.shields.io/badge/YouTube%20Data%20API-V3-red.svg)

## What's in the project ##

* [reorder_playlist.py](#reorder_playlist) takes a list of YouTube Playlist IDs, gathers the videos in each playlist and reorders them according to their episode number. This is highly customized to our internal needs, but with minor modifications should work with any Playlist you own.

### These have been moved to the legacy folder

* [pyTubePlaylist](#pytubeplaylist) lets you download all the video metadata for a YouTube playlist.
* [pyTubeReorderPlaylist](#pytubereorderplaylist) lets you take the metadata downloaded by pyTubePlaylist and (after some minor editing in Excel or Google Sheets) re-order the videos in the playlist by their episode number. This is particularly useful when you have a playlist with 150 episodes out of order.
* [pyTube](#pytube2) lets you download basic stats for a list of channels.

## Getting Started ##

### Clone this repository: ###

```bash
git clone https://github.com/cgranier/pyTube.git
```

### Install dependencies: ###

* Install the Google APIs Client Library for Python

```bash
pip install --upgrade google-api-python-client
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
```

* Install additional libraries

```bash
pip install pandas
```

### Setup YouTube APIs ###

If you're on my team, contact me for API access or CMS credentials if neeeded. Otherwise, you will need to create a Project on Google Cloud Platform and add the YouTube Data API V3.

The project doesn't need an API key anymore, as it uses OAuth to authenticate you with YouTube. You will need a YouTube account with permissions to manage the channel with the Playlist. This could be the channel owner's account or a YouTube CMS account (MCN Network) with admin permissions to act on behalf of channels in the network.

1. Create an OAuth token for your project in Google Cloud Platform, so that you can authorize modification of your videos (needed to reorder a playlist or access private videos):

* Go to the [APIs dashboard](https://console.cloud.google.com/apis/dashboard) for your project.

* Go to the [Credentials page](https://console.cloud.google.com/apis/credentials) and select Create credentials | OAuth client ID.

* Select the application type Other, give it a memorable name, and click the Create button.

* Click the file_download (Download JSON) button to the right of the client ID.

* Move the downloaded file to your working directory and rename it client_secret.json.

2. Create a _config.py_ file

```
# Project: Radar Network Tools
api_key = INSERT YOUR API KEY HERE
content_owner = INSERT YOUR CONTENT OWNER ID HERE (This is for MCN/CMS accounts only)
```

## reorder_playlist ##

### Description ###

reorder_playlist allows you to download a list of videos within a playlist and modify their order within the playlist.

It currently downloads the following data, but more data is available:

* playlist_item_id_: the video's ID within the playlist. This is different than the video's ID and is necessary for updating the video within the playlist.
* video_id_: the video's ID on YouTube.
* video_title: the video's title.
* video_position: the video's position within the playlist.

### Arguments ###

For reorder_playlist you must provide a list of playlist ids:

```python
PLAYLISTS = ['PLM21IsezPrtpSFaeQR7nvEft7S_4vsE8S',
             'PLM21IsezPrtqf4Bh6H1M3zI4zNO4KIGbX']
```

### Run the code ###

```bash
python reorder_playlist.py
```

### Functions ###

1. get_authenticated_service

Uses the Google API Client Libraries to authorize the script to modify your channels. You will see a message on the command line with a URL for OAuth authentication. Copy the URL into your browser (ideally one where you've already logged in into YouTube with the account that owns the playlist you wish to reorder), follow the instructions to authorize your project to manage the YouTube account, and copy the authorization code.

![Authorization code request](images/oauth-url.png)

Paste the authentication code into your terminal and continue.

2. get_playlist_videos

Uses youtube.playlistItems().list to request a list of all videos in a playlist, paging through the playlist until all videos have been processed (YouTube limits results to 50 per page). Returns a JSON object with all the video metadata.

3. get_video_list

Iterates through the video metadata collected by _get_playlist_videos_ and creates a dictionary with the data we need for reordering. Uses a regex to extract the episode number from the video title.

The resulting dictionary is converted into a Pandas dataframe and reordered by episode number.

4. reorder_playlist_videos

Calls youtube.playlistItems().update with new position data for each episode. Episodes need to be ordered from first to last in order to keep the proper position within the playlist.

**Note:** By default, YouTube limits API queries to 10,000 quota points per day. Reordering one video uses up 53 quota points right now, so you will be limited to around 180 videos per day.

## Contribution guidelines ##

Please take a look at our contributing [guidelines](CONTRIBUTING.md) if you're interested in helping!

## Pending Features ##

* Front end
* Edit video metadata
* Access metadata from a database
* Add comments to videos
* Download all reports every month for archiving