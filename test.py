from packages.db_manager.youtube.api_calls_youtube import *
from packages.db_manager.youtube.youtube_data import push_audio_dataset
from tqdm import tqdm

playlist_link : str = "https://youtube.com/playlist?list=PLHdLJeeTQbtIrtOwvmJcO6XkKK5KKp18T&si=7wZJzpIbxwCdXbq1"
playlist_id : str = "PLHdLJeeTQbtIrtOwvmJcO6XkKK5KKp18T"

# Getting the url for each videos in the playlist
videos_urls : list[str] = get_playlist_videos(playlist_id)
print(videos_urls)

# downloading audios
for video_url in videos_urls:
    download_audio(video_url, "./datasets/youtube/audio/")

# # Creating the dataset
# push_audio_dataset()
