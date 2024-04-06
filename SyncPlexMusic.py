from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.audio import Album, Audio
import plexapi
import os
from dotenv import load_dotenv
from pathlib import Path
import requests
import logging


load_dotenv()
username = os.getenv('PLEX_USER')
password = os.getenv('PLEX_PASSWORD')
server_name = os.getenv('SERVER_NAME')
base_url = os.getenv('BASE_URL')
token = os.getenv('TOKEN')
# print(username)
# print(password)
# print(server_name)
# account = MyPlexAccount(username, password)
# plex = account.resource(server_name).connect()
plex = PlexServer(base_url, token)
print(plex)

processed_albums_file = 'processed_albums.txt'
def load_processed_albums():
    """Load the set of processed albums from the processed_albums_file."""
    processed_albums = set()
    if os.path.exists(processed_albums_file):
        with open(processed_albums_file, 'r') as f:
            for line in f:
                processed_albums.add(line.strip())
    return processed_albums



def download_all_music(plex):
    # Access the music library section
    music = plex.library.section('Music')

    # Iterate over the first 3 tracks sorted by 'addedAt'
    for i, track in enumerate(music.search(sort= 'addedAt', libtype='track')):
        if i == 3:
            break
        try:
            # Extract track information
            song_title = track.title
            artist_title = track.grandparentTitle
            album_title = track.parentTitle

            # Print track details
            print(f"Song: {song_title}")
            print(f"Artist: {artist_title}")
            print(f"Album: {album_title}")
            print(track.addedAt)
            
            # Retrieve album object for additional metadata (e.g., genres)
            album_obj = track.album()
            for genre in album_obj.genres:
                print(f"Genre: {genre}")
            
            # Set save path for downloading
            cwd = os.getcwd()
            save_path = os.path.join(cwd, "music", artist_title, album_title)
            print(f"Save Path: {save_path}")

            # Ensure directory exists and download the track
            os.makedirs(save_path, exist_ok=True)
            track.download(savepath=save_path, includeExtras=True, keep_original_name=True, subfolders=False)
            
            # Download album artwork if available
            if
                if track.album().thumbUrl:
                    thumbnail_url = track.album().thumbUrl
                    response = requests.get(thumbnail_url)
                    if response.status_code == 200:
                        # Save album thumbnail to local file
                        thumbnail_filename = "albumart.jpg"  
                        thumbnail_filepath = os.path.join(save_path, thumbnail_filename)
                        with open(thumbnail_filepath, 'wb') as f:
                            f.write(response.content)
                        print(f"Downloaded thumbnail for '{album_title}' successfully.")
                    else:
                        print(f"Failed to download thumbnail for '{album_title}'. Status code: {response.status_code}")
            
            print("Downloaded successfully.\n")

        except:
            print("we broke")

# "addedAt<<": "2021-01-01" #replace date with last sync date

#  for album in music.search(sort=""):
#     print(album.title)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='plex_download.log',
        filemode='a'
    )
    download_all_music(plex)