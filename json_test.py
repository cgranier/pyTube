import json
import pprint

raw_json = r"""
{
 "kind": "youtube#videoListResponse",
 "etag": "\"p4VTdlkQv3HQeTEaXgvLePAydmU/btIZWPMISvtJwhbAxO5iJmJnghE\"",
 "pageInfo": {
  "totalResults": 1,
  "resultsPerPage": 1
 },
 "items": [
  {
   "kind": "youtube#video",
   "etag": "\"p4VTdlkQv3HQeTEaXgvLePAydmU/0mBzV4lSGLdvh0LgT_H6KMGQ0Ag\"",
   "id": "ZZdnlZYMkZ0",
   "snippet": {
    "publishedAt": "2019-12-12T00:00:08.000Z",
    "channelId": "UCdUdJZHwVbzDZB7K__O7nbw",
    "title": "Por Estas Calles | Episodio 563 |  Marialejandra Martin y Aroldo Betancourt  |  Telenovelas RCTV",
    "description": "Por Estas Calles 563 : Una historia de amor en un mundo en crisis. Un mundo donde el dinero es más importante que la vida, donde la ley y el orden están en juego. Un mundo donde la gente honesta debe luchar para mantener sus sueños, el amor y la verdad con el fin de hacer un mundo mejor para las generaciones más jóvenes.\n\nSi te gustó Por Estas Calles, disfruta de más telenovelas en RCTV: \n\nSUSCRIBETE en YouTube ► http://goo.gl/s1KaKH\nDANOS UN LIKE en Facebook ►https://goo.gl/5xE6YS\nSIGUENOS EN Twitter ► https://goo.gl/oEKgp2\nSIGUENOS EN Instagram ► https://goo.gl/1wAaRU\n\nPor Estas Calles:\nUna historia de amor en un mundo en crisis. Un mundo donde el dinero es más importante que la vida, donde la ley y el orden están en juego. Un mundo donde la gente honesta debe luchar para mantener sus sueños, el amor y la verdad con el fin de hacer un mundo mejor para las generaciones más jóvenes.\n\nPROTAGONISTAS:\nMarialejandra Martin\nAroldo Betancourt\nFranklin Virguez\nGledys Ibarra\nAlicia Plaza\n\nESCRITOR:\n\n\nDIRECTOR:\n \n¿QUIENES SOMOS?\nRCTV canal oficial de Radio Caracas Televisión. Primer canal de Televisión en Venezuela con más de 60 años de historia. Estamos ahora con todo nuestro contenido, telenovelas, películas, documentales, comedia, y mucho más en YouTube. ¡Entra ya! http://goo.gl/s1KaKH\n\nRADAR:\nGana dinero con tus videos. Unete a Radar: https://goo.gl/Ap7Fhs\nJoin Radar and make money with your videos: https://goo.gl/Ap7Fhs",
    "thumbnails": {
     "default": {
      "url": "https://i.ytimg.com/vi/ZZdnlZYMkZ0/default.jpg",
      "width": 120,
      "height": 90
     },
     "medium": {
      "url": "https://i.ytimg.com/vi/ZZdnlZYMkZ0/mqdefault.jpg",
      "width": 320,
      "height": 180
     },
     "high": {
      "url": "https://i.ytimg.com/vi/ZZdnlZYMkZ0/hqdefault.jpg",
      "width": 480,
      "height": 360
     },
     "standard": {
      "url": "https://i.ytimg.com/vi/ZZdnlZYMkZ0/sddefault.jpg",
      "width": 640,
      "height": 480
     }
    },
    "channelTitle": "RCTV",
    "tags": [
     "telenovela",
     "novela",
     "rctv",
     "pongalo",
     "drama",
     "venezuela",
     "action",
     "entertainment",
     "latin",
     "hispanic",
     "episodio",
     "por estas calles",
     "Marialejandra Martín",
     "Aroldo Betancourt",
     "Franklin Virguez",
     "Gledys Ibarra",
     "Alicia Plaza"
    ],
    "categoryId": "24",
    "liveBroadcastContent": "none",
    "defaultLanguage": "es",
    "localized": {
     "title": "Por Estas Calles | Episodio 563 |  Marialejandra Martin y Aroldo Betancourt  |  Telenovelas RCTV",
     "description": "Por Estas Calles 563 : Una historia de amor en un mundo en crisis. Un mundo donde el dinero es más importante que la vida, donde la ley y el orden están en juego. Un mundo donde la gente honesta debe luchar para mantener sus sueños, el amor y la verdad con el fin de hacer un mundo mejor para las generaciones más jóvenes.\n\nSi te gustó Por Estas Calles, disfruta de más telenovelas en RCTV: \n\nSUSCRIBETE en YouTube ► http://goo.gl/s1KaKH\nDANOS UN LIKE en Facebook ►https://goo.gl/5xE6YS\nSIGUENOS EN Twitter ► https://goo.gl/oEKgp2\nSIGUENOS EN Instagram ► https://goo.gl/1wAaRU\n\nPor Estas Calles:\nUna historia de amor en un mundo en crisis. Un mundo donde el dinero es más importante que la vida, donde la ley y el orden están en juego. Un mundo donde la gente honesta debe luchar para mantener sus sueños, el amor y la verdad con el fin de hacer un mundo mejor para las generaciones más jóvenes.\n\nPROTAGONISTAS:\nMarialejandra Martin\nAroldo Betancourt\nFranklin Virguez\nGledys Ibarra\nAlicia Plaza\n\nESCRITOR:\n\n\nDIRECTOR:\n \n¿QUIENES SOMOS?\nRCTV canal oficial de Radio Caracas Televisión. Primer canal de Televisión en Venezuela con más de 60 años de historia. Estamos ahora con todo nuestro contenido, telenovelas, películas, documentales, comedia, y mucho más en YouTube. ¡Entra ya! http://goo.gl/s1KaKH\n\nRADAR:\nGana dinero con tus videos. Unete a Radar: https://goo.gl/Ap7Fhs\nJoin Radar and make money with your videos: https://goo.gl/Ap7Fhs"
    },
    "defaultAudioLanguage": "es-419"
   },
   "contentDetails": {
    "duration": "PT41M30S",
    "dimension": "2d",
    "definition": "sd",
    "caption": "false",
    "licensedContent": true,
    "projection": "rectangular",
    "hasCustomThumbnail": false
   },
   "status": {
    "uploadStatus": "processed",
    "privacyStatus": "public",
    "publishAt": "2019-12-12T00:00:00.000Z",
    "license": "youtube",
    "embeddable": true,
    "publicStatsViewable": true
   },
   "fileDetails": {
    "fileName": "por-estas-calles_22-563.mpg"
   }
  }
 ]
}
"""

video_json = json.loads(raw_json)

# pprint.pprint(video_json)

# video_json = raw_json

metadata = []

# print(video_json['items'])

for item in video_json['items']:
    metadata.append(item)

# metadata.append(video_json[0])

pprint.pprint(metadata)

print(metadata[0]['snippet']['tags'])
metadata_tags = ('|'.join(metadata[0]['snippet']['tags']))
print(metadata_tags)

for video in metadata: 
    video_tags = ('|'.join(video.get('snippet').get('tags')))

print(video_tags)


more_json = r""{'etag': 'p4VTdlkQv3HQeTEaXgvLePAydmU/c3Sr0vpkZlhxWL_0e_B1Q7VYp5Y',
 'items': [{'contentDetails': {'caption': 'false',
                               'definition': 'sd',
                               'dimension': '2d',
                               'duration': 'PT40M21S',
                               'hasCustomThumbnail': True,
                               'licensedContent': True,
                               'projection': 'rectangular'},
            'etag': '"p4VTdlkQv3HQeTEaXgvLePAydmU/ZQCD4ls0Im3QXKKkGfwEyVZ6NrQ"',
            'fileDetails': {'fileName': 'dama-rosa-portugues_1-1.mp4'},
            'id': '0A9DHSxkOs0',
            'kind': 'youtube#video',
            'snippet': {'categoryId': '24',
                        'channelId': 'UCdUdJZHwVbzDZB7K__O7nbw',
                        'channelTitle': 'RCTV',
                        'defaultAudioLanguage': 'pt',
                        'defaultLanguage': 'es-419',
                        'description': 'La Dama De Rosa (En Portugués) / 1: '
                                       'Disfruta de nuestra telenovela La Dama '
                                       'de Rosa en portugues!',
                        'liveBroadcastContent': 'none',
                        'localized': {'description': 'La Dama De Rosa (En '
                                                     'Portugués) / 1: Disfruta '
                                                     'de nuestra telenovela La '
                                                     'Dama de Rosa en '
                                                     'portugues!',
                                      'title': 'La Dama De Rosa (En Portugués) '
                                               '| Episodio 1 | Jeannette '
                                               'Rodriguez y Carlos Mata | '
                                               'Telenovelas RCTV'},
                        'publishedAt': '2019-12-02T15:02:41.000Z',
                        'tags': ['telenovela',
                                 'novela',
                                 'rctv',
                                 'pongalo',
                                 'drama',
                                 'venezuela',
                                 'action',
                                 'entertainment',
                                 'latin',
                                 'hispanic',
                                 'episodio',
                                 'La Dama de Rosa',
                                 'dubbed',
                                 'dub',
                                 'potuguese',
                                 'Jeannette Rodriguez',
                                 'Carlos Mata',
                                 'Television venezolana',
                                 'south america',
                                 'historia',
                                 'telemundo',
                                 'amor latino',
                                 'novelas gratis',
                                 'motivacion',
                                 'pasion',
                                 'RadarPix',
                                 'pareja',
                                 'latin love',
                                 'amor amor amor',
                                 'espectaculos',
                                 'tv',
                                 'full novelas',
                                 'amor y amistad',
                                 'novelas novelas novelas',
                                 'novelas',
                                 'encuentra el amor',
                                 'jane the virgin'],
                        'thumbnails': {'default': {'height': 90,
                                                   'url': 'https://i.ytimg.com/vi/0A9DHSxkOs0/default.jpg',
                                                   'width': 120},
                                       'high': {'height': 360,
                                                'url': 'https://i.ytimg.com/vi/0A9DHSxkOs0/hqdefault.jpg',
                                                'width': 480},
                                       'maxres': {'height': 720,
                                                  'url': 'https://i.ytimg.com/vi/0A9DHSxkOs0/maxresdefault.jpg',
                                                  'width': 1280},
                                       'medium': {'height': 180,
                                                  'url': 'https://i.ytimg.com/vi/0A9DHSxkOs0/mqdefault.jpg',
                                                  'width': 320},
                                       'standard': {'height': 480,
                                                    'url': 'https://i.ytimg.com/vi/0A9DHSxkOs0/sddefault.jpg',
                                                    'width': 640}},
                        'title': 'La Dama De Rosa (En Portugués) | Episodio 1 '
                                 '| Jeannette Rodriguez y Carlos Mata | '
                                 'Telenovelas RCTV'},
            'status': {'embeddable': True,
                       'license': 'youtube',
                       'privacyStatus': 'public',
                       'publicStatsViewable': True,
                       'uploadStatus': 'processed'}}],
 'kind': 'youtube#videoListResponse',
 'pageInfo': {'resultsPerPage': 1, 'totalResults': 1}}""

# video_data = json.loads(more_json)
print('---------------------------------------------------------------')
print(more_json['items'])
more_json_tags = ('|'.join(more_json[0]['snippet']['tags']))
print(more_json_tags)
