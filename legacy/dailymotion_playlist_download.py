# -*- coding: utf-8 -*-
import json
import urllib.request
import csv

# INPUT DATA
import playlists
PLAYLISTS = playlists.DAILYMOTION

# SETUP

dailymotion_API_url = 'https://api.dailymotion.com/'
dailymotion_playlist_API_url = dailymotion_API_url + 'playlist/{0}/videos?fields=id,title,url'

def get_playlist_videos(PLAYLIST_ID):
    playlist_videos = []
    page = 1
    limit = 100
    has_more = True
    base_url = dailymotion_playlist_API_url.format(PLAYLIST_ID)

    while has_more:
        url = base_url + '&page={0}&limit={1}'.format(page,limit)
        response = urllib.request.urlopen(url)
        response_as_json = json.load(response)
        response.close()
        returned_videos = response_as_json['list']
        for video in returned_videos:
            playlist_videos.append(video)
        page +=1
        has_more = response_as_json['has_more']

    return playlist_videos

def main():
    for playlist in PLAYLISTS:
        out_file = playlist + '_dailymotion.csv'
        with open(out_file, 'w', newline='', encoding='utf-8') as new_file:
            out_file_headers = ['id','title','url']
            out_writer = csv.DictWriter(new_file, fieldnames = out_file_headers)
            out_writer.writeheader()
            
            playlist_videos = get_playlist_videos(playlist)
            for video in playlist_videos:
                video_id = video.get('id')
                video_title = video.get('title')
                video_url = video.get('url')

                data_row = {'id':video_id,'title':video_title,'url':video_url}
                out_writer.writerow(data_row)


if __name__ == '__main__':
    main()
