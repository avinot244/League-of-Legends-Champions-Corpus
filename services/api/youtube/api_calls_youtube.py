import requests
import os
import json
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
import yt_dlp

from packages.globals import DATASETS_PATH


def get_token():
    with open(DATASETS_PATH + "token_ytb.json", "r") as f:
        token_dict : dict = json.load(f)
        return token_dict["token"]

def get_playlist_videos(playlist_id):
    token = get_token()
    youtube = build('youtube', 'v3', developerKey=token)
    
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=50
    )

    video_urls = []
    while request:
        response = request.execute()

        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_urls.append(f"https://www.youtube.com/watch?v={video_id}")

        request = youtube.playlistItems().list_next(request, response)

    return video_urls

def get_playlist_id(url):
    query = urlparse(url).query
    params = parse_qs(query)
    return params['list'][0] if 'list' in params else None

def download_audio(youtube_url, output_path='.'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
            print("Audio downloaded successfully.")
    except Exception as e:
        print(f'An error occurred: {e}')
    