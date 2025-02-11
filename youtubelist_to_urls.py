#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__date__ = '2025/01/10'

from googleapiclient.discovery import build
import os
import requests

"""
YouTubeの再生リストURLから全ての動画のURLを取得し、niconicoURLに変換するプログラム
"""

DEVELOPER_KEY = os.getenv('DEVELOPER_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_playlist_video_urls(playlist_url):
    """再生リストURLからniconicoURLリストに変換する"""
    
    playlist_id = playlist_url.split("list=")[-1]

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
    )

    video_urls = []
    next_page_token = None

    while True:
        playlist_items_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=100,
            pageToken=next_page_token
        ).execute()
        for item in playlist_items_response['items']:
            
            video_id = item['snippet']['resourceId']['videoId']
            print(video_id)
            video_urls.append(video_id)

        for item in playlist_items_response['items']:
            youtube_base_url = 'https://www.youtube.com/watch?v='
            video_id = item['snippet']['resourceId']['videoId']
            vocadb_url = f'https://vocadb.net/api/songs?query={youtube_base_url + video_id}&fields=PVs'
            try:
                vocadb_response = requests.get(vocadb_url)
                if vocadb_response.status_code == 200:
                    json = vocadb_response.json()
                    for item in json['items']:
                        for pv in item['pvs']:
                            if pv['service'] == 'Youtube':
                                video_urls.append(pv['url'])
                if vocadb_response.status_code == 404:
                    video_urls.append(youtube_base_url + video_id)
            except Exception as e:
                print(e)
            print(video_urls[-1])
        next_page_token = playlist_items_response.get('nextPageToken')
        if not next_page_token:
            break

    return "\n".join(video_urls)

def main():
    """url_list.txtに書き込みを行う"""

    playlist_url = 'https://www.youtube.com/watch?v=p3ymzi70Gjs&list=PLAaqbXSZIG6xmT6noHxHA2YD65cOXRZBS'
    urls = get_playlist_video_urls(playlist_url)

    print(urls)

    with open("url_list.txt", "w") as file:
        file.write(urls)


if __name__ == "__main__":
    import sys
    sys.exit(main())
