from services.create_database.create_youtube_database import get_mp3_files
from services.api.youtube.youtube_data import push_audio_dataset

playlist_links : list[str] = [
    "https://youtube.com/playlist?list=PLW95uNtA6Sdj0RLPdvUMM_ItGzDJEKYxD&si=uJkcxagjbGgZ0o_x",
    "https://youtube.com/playlist?list=PL3jpWy4k77KPrAPRjiXyKUk4_91_P75N7&si=_h1SiJVPGUID32x1",
    "https://youtube.com/playlist?list=PLNw7fFNwVdzu2jBEBDtjRtSPUCsSh-MWd&si=Vldpa8VCwRLZBBd8",
]

for playlist_link in playlist_links:
    get_mp3_files(playlist_link)


push_audio_dataset()