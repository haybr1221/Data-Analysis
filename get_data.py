import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import threading
from config import CLIENT_ID, CLIENT_SECRET

client_credentials = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials)

class Track:
    def __init__(self, track_num, track_name, album, release_date,  artists, duration_ms, popularity):
        self.track_num = track_num
        self.track_name = track_name
        self.album = album
        self.release_date = release_date
        self.artists = artists
        self.duration_ms = duration_ms
        self.popularity = popularity

    def to_dict(self):
        return {
            "track_num": self.track_num,
            "track_name": self.track_name,
            "album": self.album,
            "release_date": self.release_date,
            "artist": ", ".join(self.artists),
            "duration_ms": self.duration_ms,
            "popularity": self.popularity
        }

# Define a term to search for
search_for = input("What would you like to search for? ")
search_limit = int(input("How many would you like to get? "))

if search_limit > 50:
    # If a user inputs more than 50, set it to 50 to properly execute
    print("Max requests is 50. Setting limit to 50.")
    search_limit = 50

# Search for the defined term, get albums
results = sp.search(q=search_for, type="album", limit=search_limit)

# Make a list to add results to
track_list = []

# Make a lock for the threads
lock = threading.Lock()

# Set a semaphore to make sure API calls are kept within the limit
semaphore = threading.Semaphore(15)

print("Getting data...")

def track_info(album):
    specific_tracks = []
    with semaphore:
        print("Getting a new album...")
        album_name = album["name"]
        release_date = album["release_date"]

        tracks = sp.album_tracks(album["id"])

        for track in tracks["items"]:
            track_name = track["name"]
            track_num = track["track_number"]
            artists = [artist["name"] for artist in track["artists"]]
            duration_ms = track["duration_ms"]

            track_details = sp.track(track["id"])
            popularity = track_details.get("popularity", 0)

            new_track = Track(album_name, release_date, track_name, track_num, artists, duration_ms, popularity)
            specific_tracks.append(new_track)

    with lock:
        # Make sure each track is added with the correct information
        print("Pushing tracks to final list")
        track_list.extend(specific_tracks)

threads = []

for album in results["albums"]["items"]:
    t = threading.Thread(target=track_info, args=(album,))
    threads.append(t)

# Start all threads
for t in threads:
    t.start()

# Wait for threads to finish
for t in threads:
    t.join()

print("Found all albums, creating CSV file...")
df_tracks = pd.DataFrame([track.to_dict() for track in track_list])
df_tracks.to_csv("data.csv", index=False)
print("CSV file created!")