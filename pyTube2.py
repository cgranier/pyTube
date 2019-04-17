import json
import sys
from apiclient.errors import HttpError
import urllib.request
import csv
import config

# Documentation
# https://github.com/dsebastien/youtubeChannelVideosFinder/blob/master/youtubeChannelVideosFinder.py
# https://stackoverflow.com/questions/15512239/python-get-all-youtube-video-urls-of-a-channel

# Constants
api_key = config.api_key

# Strings
youtubeApiUrl = 'https://www.googleapis.com/youtube/v3/'
youtubeChannelsApiUrl = youtubeApiUrl + 'channels?key={0}&'.format(api_key)
youtubeSearchApiUrl = youtubeApiUrl + 'search?key={0}&'.format(api_key)
requestChannelVideosInfo = youtubeSearchApiUrl + 'channelId={0}&part=id,snippet&order=date&type=video&pageToken={1}&maxResults=50'
youtubeVideoUrl = 'https://www.youtube.com/watch?v={0}'
youtubeVideoApiUrl = youtubeApiUrl + 'videos?key={0}&'.format(api_key)
requestVideoStats = youtubeVideoApiUrl + 'id={0}&part=statistics'

#DEBUG
# print(youtubeApiUrl)
# print(youtubeChannelsApiUrl)
# print(requestChannelVideosInfo)
# print(youtubeVideoUrl)

# Channels
# channel_list = ['UCBhvAR0ggs7f85MB2VsOBYQ', 'UCydfSMZx3h_P6g2z3FQGOXw', 'UCGy7Y62Lgb8t6eRunAs8H9A', 'UC8gJ68jIXGkSq-ZDhRpQkaQ', 'UCHuYNb7jxH1tJpj0cOMKrnw', 'UCBDryx6K-qMJ7OLlek5tK3A', 'UCVILeru9h8rSqzqX8sjNA5w', 'UCPkwYgMgqZuO771455_oLDg', 'UCw5GvWAOu5UiaAbvhiBivJQ', 'UCw7IAcklGn6aWoFgS5zygew', 'UCQVqDTmzgUZ5YPJyMWyLfag', 'UCB1f-vL9xlOgAmGYnLZNIxA', 'UCuKT5mATDQYxv_ig12MARNQ', 'UC_MC9fGICiThZxdcaVpH5NQ', 'UC-u5sCLvCDpxhRHJ-a4uevw', 'UC0JVIhfmXkuKLhDSbeXuFLA', 'UCc3m_B0mXneb-hfsMvQLdxA', 'UCV0t85kQN7WVldBsa7DGP9g', 'UC7E_oQeYFZxAV4kA5IHVQMw', 'UCuVKaQOqKY9mXrXpq6EVNWQ', 'UCUfY0QeIAET7MgLoskLBHAg', 'UCTOohkKvXesXs3Outmbq1jQ', 'UC1i0_D4RWe6TqfTolJyjeGg', 'UCiWGcrHLf7yUwLNfS6KuFVg', 'UCI89ontjbuF9PbF9mizxCzQ', 'UC5Vh9KVMasCY_JM_rd75xlw', 'UCNNI61Q8FJXra_nzOKseySw', 'UCjv6y4dsTuVlLF_tARqqGqw', 'UCXx0mLcO4QCPpf-Llzo6zxw', 'UCjIROLxbsPxU8_HsHvIEC_w', 'UCeSooh4Uqj5dd4OrOI0IRnQ', 'UCmrwLtdZphDr6pubUUIr38g', 'UCvUf-1xmZYC9705I6y99UFw', 'UC8BMeEluVwyGgL9wtj-q0zQ', 'UCctVKZ_JSXYmly2GQq7UA3w', 'UCBxnTBE-aQ6dkovUb9bwOag', 'UCYOSwicdUY9TAk3zPrjERyA', 'UCJPucdVjgIBnPLVjsOeUpMg', 'UC3z-B_bfZGz1A7STC8waCTw', 'UCBOUVGQoLnnRkzWdSem_LxQ', 'UCy2_99Kq0Go2AF2j7ZeTwFA', 'UCJmD1-Hl3jO1mtcyhbvBPUw', 'UCZgn1RQCyPFBavF-DCakYrQ', 'UC6JZ1n7-WuNMFB-5w2diHfg', 'UCTOkp7YaYj6igrUnqY8IhJA', 'UCbeEFXUZ24gfzAUx0Pfv5aQ', 'UC15G08CM_e9VhGovpv3hClw', 'UCoknLUXqnZAHWfpXuVhHVow', 'UCgByx3bVJAFx2QqU7Hidefw', 'UCFZIBAfpsxyR3mauaPH3zcQ', 'UCleP0eraPxsDYGvvMLjigkA', 'UChB72ye8JczHV0SnVoUmWSw', 'UCuQqjt1aksB_V5zvICA6pcg', 'UCmluUsnDlGe7hwSHbBRR4ag', 'UCEICks9azp7q5dHE6VL0GNQ', 'UCEYL5HGGJCJSjeblfgHn5ag', 'UC_dIGY0r30CF_dntKCPW1uQ', 'UCqVRgi4vuIUXKTvdEVJkXjw', 'UChem3X7BVp0V7LKpnM-VbgQ', 'UC-mqa8PxKh5LosQyPhUp3vg', 'UCmeoz5_X_F2-ENY_QkEN04Q', 'UCFmq9e7ZAOJbKMdX9vbt4ZA', 'UC-Ipsk2TkMHzl4ZDcWUR7vg', 'UCXIBZN6BVHl0mc2lHPjo7aA', 'UCYmyU6lLkhYVChe56eaxckA', 'UC2iIR5oUFcF-y3NpleHt6yg', 'UCyja40Fe28aA_V9289fmLNA', 'UCAdT54xNQNCWAuFeith9oIw', 'UCSf1H9iXMMUqH5cB3wsPEwQ']


channel_list = ['UCwQJ_LhqY8890dP3TlyAbYQ','UCJ_kbH97OTBS7MR_T5TZNPQ','UCIvN8b2OY-eadz8TPT4Vf0A','UCmI4l1lfLG85mzsc4TELcyA','UCdaVfRWSDcx_10DNXvtD0Cw','UCQNDo1vpHkvFVJswL5DdIEw','UCkjWFJCOKVZCMS_l0zi3v9Q','UC7AIsBvu0MKY_yrUOh0sIRA','UCApbNN02BZR88DPeFQloSlA','UCU0h5uO1nxqYwrDvV9DOxHg','UCHVtixP2oVV_-hGPNGXyw2g','UCvCVDlqotZNZn69NFdRHP2Q','UCCDYCcYVcmacIetGtKJfoZg','UCs65sGsRriSRl6MBQdSS88w','UCyDReWu3i5HHB1YHFiwbJdg','UCx11cMutASlGhRygc01GeAQ','UCNqlULEOgpzWtyfZ0_kwA2Q','UCnSa7yi3VnWlNF8Ovfma06Q','UC6cZCVUIncr9gZruxGEIg5A','UC3yAGQWk_XlQT-5lBYiKmlw','UCld-8Q77GSFdXL_VAaPeVLw','UC6O_QK4KNrGvVAo0Qajuccw','UCNGH6LP3v-6m-sraRpiKr0Q','UCFRcCHzaImgHcN6LFbTijUA','UCIVbiFcULAlqlzTHvHOmKwA','UC3N9bTIs3DmLz8GN35gRmMQ','UCzJF2QCoyIrs2-yQOGeBnBg','UCskm7ajqJ6vHEHYJNBDDIXw','UCLHnG989CEbQrAM4bJxoaVQ','UCC3aC68C1SuY0anJQPBp3UQ','UCzWODsH2Uu4k8RY2SqSr2aw','UCFuNYDrH7vG7AmjlgFCkAoQ','UCiUg2xsVTff1Sn6EvmVn2_w','UCCtwLYT5F6K4Qj49-it83mA','UCjixoMo7g74eepPOXeLofMQ','UCFQbERlE7xedvNoZFjK3yJg','UCkpoaN5hS_Veou7eTNN0EdA','UCypNBhi1mfX__YLUCmsSvHQ','UCqBtJj1C1zUljbDkSQb2QwQ','UCuOilO9SG7iMeKRvrfPUu_g','UCj-2TqWb4FH4Z-DuT8UFWuQ','UC7eP8T0J2DdV5h13hT0FfFg','UCs3uct5_gv16_EOWJoSEs_A','UC4nBaj9yB6E57HQkNAXiMCw','UCKSe91WI2AaveUOWsvJTD7g','UChJyIMdw3N3I-F1i-eYBGdQ','UCJSPvHI1M98HSwnl_QZRFHg','UCElFWzckAkjbnwHkEuoxF5w','UC2eRKNBIg2u8xc97ngHwUng','UCsLH6hVFpoN7vJ42QLFmcUQ','UC3TLJk_Lg2z94CXgxbuHQWA','UCplbjvaIGdBh298btrFZaSA','UC5mLl8sb5Ki5CTrNYYVPhwg','UCWTqukum7QE-Q2B7gTrLRDQ','UC5h9hTXDPT_VZCl5BJoZVVQ','UCxI5RMOjdCo91LFvKKt3OzQ','UC4HDZVeVgoI-6v9JZ23XMdw','UCVILo6RHFzejVTPI1PeAUVg','UCo4y4HIh39KX-WO4HU3pCcw','UC4ZgcwW48Rdir7rdYardFxg','UCGVkCsrLzjYMkAR8W1ZrVpQ','UC2rbZfRn7QLebgseirqXf3A','UCCgXXtxTjgmNSGapHHfl1cQ','UCJiv8vMVyOCYsJJ6mXFS3VA','UCnmQflszbtimzPHU0aCgKZw','UC4MpK0M0UsPMB9rPbsnfbsg','UCdbmf5uT7BtbffP8rJShFeA','UCLeH1xpm1FgKLv6iHBcuqWw','UCEg5FUogo0bq5_c_n7DYdYA','UC9yAVyZiqaAjyzRspBBy36g','UC6RhWzRHoEEvMcNyYXDJrPA','UC3YuHBPc_qiZkhwblnDwq8A','UC60Y2aO8P3gZcjQJC5ll2zA','UCkT0Fak1heB8o_BmbvvRRGA','UCeTPqQOk15D0qc3qYgRtDIA','UCdIECbqBxMfVp1ZasJ4Vm5g','UC0l2zogcQrjq6VHThdnfBkA','UCX7gfFTUhwOoKjeUt4b5rWw','UCRrwAGSn-9n6Q5NlbcdYweQ','UCozP26k9na9oYiIbYISNWUw','UC7kpjUDLuie23QH82RcoIzw','UCH_-E63Xm8uvj_n85dwF6IA','UCJSUlGNuld70WpNmQKGi41w','UClXIfQRnqnz5SuFhjEf2kwQ','UC80jTDp0MYp78AAwvYEmpvw','UCwz1kXfge5JwhRznZ7SzGHQ']

def getChannelVideos(channelId):

    # initialization
    retVal = []
    found_all = False
    next_page_token = ''

    while not found_all:
        try:
            print('We\'re looking for them...')
            print('ChannelId: {0}'.format(channelId))
            url = requestChannelVideosInfo.format(channelId,next_page_token)
            print(url)
            response = urllib.request.urlopen(url)
            print(response)
            response_as_json = json.load(response)

            response.close()

            returned_videos = response_as_json['items']

            for video in returned_videos:
                retVal.append(video)
            
            try:
                next_page_token = response_as_json['next_page_token']
            except Exception:
                found_all = True

        except Exception:
            found_all = True
            print('We found them all!')

    return retVal

def getVideoURL(videoId):
    retVal = youtubeVideoUrl.format(videoId)
    return retVal

def getVideoStats(videoId):
    url = requestVideoStats.format(videoId)
    response = urllib.request.urlopen(url)
    response_as_json = json.load(response)
    response.close()
    retVal = response_as_json['items'][0]['statistics']['viewCount']
    return retVal

def main():
    out_file = 'october_partners.csv'
    with open(out_file, 'w', newline='', encoding='utf-8') as new_file:
        out_file_headers = ['channelId','videoTitle','videoURL','videoViews']
        out_writer = csv.DictWriter(new_file, fieldnames = out_file_headers)
        out_writer.writeheader()

        for channelId in channel_list:
            channelVideos = getChannelVideos(channelId)
            videoURLs = []
            for video in channelVideos:
                videoId = video.get('id').get('videoId')
                videoTitle = video.get('snippet').get('title')
                videoURL = getVideoURL(videoId)
                videoViews = getVideoStats(videoId)
                # videoURLs.append(videoURL)

                data_row = {'channelId':channelId,'videoTitle':videoTitle,'videoURL':videoURL,'videoViews':videoViews}
                out_writer.writerow(data_row)
                
                print('{0},{1},{2},{3}'.format(channelId,videoTitle,videoURL,videoViews))
                # print(video.get('snippet').get('description'))
            
            # for videoURL in videoURLs:
            #     print('Channel: {0}, Title: , URL: {1}'.format(channelId,videoURL))

if __name__ == '__main__':
    main()
