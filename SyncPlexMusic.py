from plexapi.myplex import MyPlexAccount
from plexapi.audio import Album, Audio
import plexapi
import os
from dotenv import load_dotenv
from pathlib import Path
import requests

load_dotenv()
username = os.getenv('PLEX_USER')
password = os.getenv('PLEX_PASSWORD')
server_name = os.getenv('SERVER_NAME')
print(username)
print(password)
print(server_name)
account = MyPlexAccount(username, password)
plex = account.resource(server_name).connect()
print(plex)

# Example 1: List all unwatched movies.
music = plex.library.section('Music')
# print(music.albums())
for artist in music.search(sort= 'addedAt', libtype='artist'):
    print(artist.title)

# "addedAt<<": "2021-01-01" #replace date with last sync date

#  for album in music.search(sort=""):
#     print(album.title)


