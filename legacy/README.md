# pyTube #

pyTube exists to make managing large content libraries on YouTube a bit easier. It's also an excuse for coding, learning and doing boring stuff quickly.

![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)
![YouTube Data API V3](https://img.shields.io/badge/YouTube%20Data%20API-V3-red.svg)

## What's in the project ##

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

If you're on my team, contact me for the API key. Otherwise, you will need to create a Project on Google Cloud Platform and add the YouTube Data API V3. Then you must:

1. Create an API Key credential for the project.
2. Add the necessary restrictions to your API key to avoid unforeseen charges.
3. Create a config.py file and add the API key to it:

```python
api_key = '[Your API Key]'
```

4. Create an OAuth token for your project in Google Cloud Platform, so that you can authorize modification of your videos (needed to reorder a playlist):

* Go to the [APIs dashboard](https://console.cloud.google.com/apis/dashboard) for your project.

* Go to the [Credentials page](https://console.cloud.google.com/apis/credentials) and select Create credentials | OAuth client ID.

* Select the application type Other, give it a memorable name, and click the Create button.

* Click the file_download (Download JSON) button to the right of the client ID.

* Move the downloaded file to your working directory and rename it client_secret.json.

## pyTubePlaylist ##

### Description ###

pyTubePlaylist allows you to download a list of videos within a playlist and store the information in a csv file for further processing.

It currently downloads the following data, but more data is available:

* playlistItemId: the video's ID within the playlist. This is different than the video's ID and is necessary for updating the video within the playlist.
* videoId: the video's ID on YouTube.
* videoTitle: the video's title.
* videoPosition: the video's position within the playlist.

### Arguments ###

for pyTubePlaylist you must provide the playlist id and the csv file you want to write to:

```python
playlist_list = ['PLM21IsezPrtqf4Bh6H1M3zI4zNO4KIGbX']
playlist_outFile = 'mis-3-hermanas.csv'
```

### Run the code ###

```bash
python pyTubePlaylist.py
```

## pyTubeReorderPlaylist ##

### Description ###

pyTubeReorderPlaylist takes a csv file of videos and modifies their order in the playlist according to the _episode_ column in the csv file.

We first download the videos in the playlist using _pyTubePlaylist.py_ and then modify the csv file in Google Sheets to add the episode column.

For our particular data, we use the following formula to extract the episode number of each video:

```vb
=value(trim(mid(C2,find("sodio",C2,1)+5,find("|",C2,find("|",C2)+1)-find("sodio",C2,1)-5)))
```

Export the data from Google Sheets as a .csv file and use it as the input to pyTubeReorderPlaylist.

pyTubeReorderPlaylist uses OAuth to authenticate the channel owner, since you need this permission to be able to modify the playlist order.

It also uses the Pandas library to read the csv file.

### Arguments ###

pyTubeReorderPlaylist needs the Playlist ID of the playlist you wish to modify and a csv file with the following fields (currently needs all fields and in this particular order):

|playlistItemId|videoId|videoTitle|videoURL|videoPosition|episode|
|--------------|-------|----------|--------|-------------|-------|

```python
# Playlist to modify
playlist_ID = ['PLAYLIST-ID']

# CSV file with order of videos - Use pyTubePlaylist.py to retrieve the videos initially
ordered_videos_file = 'FILENAME.csv'
```

### Run the code ###

```bash
python pyTubeReorderPlaylist.py
```

You will see a message on the command line with a URL for OAuth authentication. Copy the URL into your browser (ideally one where you've already logged in into YouTube with the account that owns the playlist you wish to reorder), follow the instructions to authorize your project to manage the YouTube account, and copy the authorization code.

![Authorization code request](images/oauth-url.png)

Paste the authentication code into your terminal and continue. Your playlist will now be in the proper order.

## pyTube2 ##

### Description ###

pyTube2 allows you to download all the video metadata for a list of YouTube channels.

It currently downloads the following fields, but more metadata is available in the response object:

* channelId: The Channel ID where the video resides.
* videoTitle: The video's title.
* videoId: The video's ID on YouTube.
* videoViews: The amount of views on the video.

### Arguments ###

pyTube2 needs a list of Channel Ids you want to check and the csv file you want to write to:

```python
channel_list = ['CHANNEL-ID-1','CHANNEL-ID-2']
```

```python
out_file = 'FILENAME.csv'
```

### Run the code ###

```bash
python pyTube2.py
```

## Contribution guidelines ##

Please take a look at our contributing [guidelines](CONTRIBUTING.md) if you're interested in helping!

## Pending Features ##

* Front end
* Edit video metadata
* Access metadata from a database
* Add comments to videos
* Download all reports every month for archiving