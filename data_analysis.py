import pandas as pd

# Define the data frame
df = pd.read_csv("data.csv")

def view_data():
    """
    View the data frame in full.
    """
    print(df)


def search():
    """
    Allow the user to search for a specific item within the dataset.
    """
    print("\nWhat would you like to search for?")
    print("     1. An artist")
    print("     2. A song")
    print("     3. An album")
    choice = int(input("Select an option from above: "))

    if choice == 1:
        artist = input("Put the name of the artist: ")
        print(df[df["artist"].str.contains(artist, case=False)])

    elif choice == 2:
        song = input("Put the name of the song: ")
        print(df[df["track_name"].str.contains(song, case=False)])

    elif choice == 3:
        album = input("Put the name of the album: ")
        print(df[df["album"].str.contains(album, case=False)])


def popularity():
    """
    Display the popularity of a particular part of the data set.
    """
    print("\nWhat would you like to see?")
    print("     1. Popular songs")
    print("     2. Popular albums")
    print("     3. Songs from particular album")
    print("     4. Songs from a particular artist")
    type = int(input("Select an option from above: "))
    pop_type = input("Would you like to see the most popular (y) or the least popular (n)? ")
    values = int(input("How many values would you like to see? "))

    if type == 1:
        # See overall top tracks
        if pop_type == "y":
            # Select the top tracks
            print("\nMost popular songs:")
            top_tracks = df.sort_values(by="popularity", ascending=False).head(values)
            print(top_tracks[["track_name", "album", "popularity"]])

        elif pop_type == "n":
            print("\nLeast popular songs:")
            # Select the bottom tracks
            bottom_tracks = df.sort_values(by="popularity", ascending=True).head(values)
            print(bottom_tracks[["track_name", "album", "popularity"]])
    elif type == 2:
        # See overall albums
        album_popularity = df.groupby("album", as_index=False)["popularity"].mean().round(2)

        if pop_type == "y":
            # Select the top albums
            print("\nMost popular albums:")
            top_albums = album_popularity.sort_values(by="popularity", ascending=False).head(values)
            print(top_albums[["album", "popularity"]])

        elif pop_type == "n":
            # Select the bottom albums
            print("\nLeast popular albums:")
            bottom_albums = album_popularity.sort_values(by="popularity", ascending=True).head(values)
            print(bottom_albums[["album", "popularity"]])
    elif type == 3:
        # See top songs from a particular album
        # Get the album to search
        album = input("What ablum would you like to see the popularity of? ")

        # Put it in a smaller data frame
        album_data = df[df["album"].str.contains(album, case=False)]

        # Sort through the data
        if pop_type == "y":
            print(f"\nMost popular songs from {album.title()}")
            top_songs = album_data.sort_values(by="popularity", ascending=False).head(values)
            print(top_songs[["track_num", "track_name", "popularity"]])
        elif pop_type == "n":
            print(f"\nLeast popular songs from {album.title()}")
            top_songs = album_data.sort_values(by="popularity", ascending=True).head(values)
            print(top_songs[["track_num", "track_name", "popularity"]])
    elif type == 4:
        # See top songs from a particular artist
        # Get the artist to search
        artist = input("What artist would you like to see the popularity of? ")

        # Put it in a smaller dataframe
        artist_data = df[df["artist"].str.contains(artist, case=False)]

        # Sort through the data
        if pop_type == "y":
            print(f"\nMost popular songs featuring {artist.title()}:")
            top_songs = artist_data.sort_values(by="popularity", ascending=False).head(values)
            print(top_songs[["track_num", "track_name", "album", "popularity"]])
        elif pop_type == "n":
            print(f"\nLeast popular songs featuring {artist.title()}:")
            top_songs = artist_data.sort_values(by="popularity", ascending=True).head(values)
            print(top_songs[["track_num", "track_name", "album" , "popularity"]])


def duration():
    """
    Sort data by checking the duration.
    """
    print("\nWhat would you like to see?")
    print("     1. Overall songs")
    print("     2. Overall albums")
    print("     3. Songs from particular album")
    print("     4. Songs from a particular artist")
    type = int(input("Select an option from above: "))
    len_type = input("Would you like to see the longest (y) or the shortest (n)? ")
    values = int(input("How many values would you like to see? "))
    # TODO allow user to view all results if they desire

    if type == 1:
        if len_type == "y":
            # See overall longest tracks
            print("\nLongest songs:")
            long_tracks = df.sort_values(by="duration_ms", ascending=False).head(values)
            long_tracks["duration (mins)"] = long_tracks["duration_ms"].apply(convert_to_min)
            print(long_tracks[["track_name", "album", "duration (mins)"]])
        elif len_type == "n":
            # See overall shortest tracks
            print("\nShortest songs:")
            long_tracks = df.sort_values(by="duration_ms", ascending=True).head(values)
            long_tracks["duration (mins)"] = long_tracks["duration_ms"].apply(convert_to_min)
            print(long_tracks[["track_name", "album", "duration (mins)"]])
    elif type == 2:
        # See overall albums
        album_length = df.groupby("album", as_index=False)["duration_ms"].sum().round(2)

        if len_type == "y":
            # Select longest albums
            print("\nLongest albums:")
            longest_albums = album_length.sort_values(by="duration_ms", ascending=False).head(values)
            longest_albums["duration (HH:MM:SS)"] = longest_albums["duration_ms"].apply(convert_to_hr)
            print(longest_albums[["album", "duration (HH:MM:SS)"]])
        if len_type == "n":
            # Select shortest albums
            print("\nShortest albums:")
            short_albums = album_length.sort_values(by="duration_ms", ascending=True).head(values)
            short_albums["duration (HH:MM:SS)"] = short_albums["duration_ms"].apply(convert_to_hr)
            print(short_albums[["album", "duration (HH:MM:SS)"]])
    elif type == 3:
        # See longest songs per album
        album = input("What album would you like to sort by length? ")

        # Put it in a smaller data frame
        album_data = df[df["album"].str.contains(album, case=False)]
        
        # Sort through
        if len_type == "y":
            print(f"\nLongest songs from {album.title()}:")
            long_tracks = album_data.sort_values(by="duration_ms", ascending=False).head(values)
            long_tracks["duration (mins)"] = long_tracks["duration_ms"].apply(convert_to_min)
            print(long_tracks[["track_name", "album", "duration (mins)"]])
        elif len_type == "n":
            print(f"\nShortest songs from {album.title()}:")
            short_tracks = album_data.sort_values(by="duration_ms", ascending=True).head(values)
            short_tracks["duration (mins)"] = short_tracks["duration_ms"].apply(convert_to_min)
            print(short_tracks[["track_name", "album", "duration (mins)"]])
    elif type == 4:
        # See songs from a particular artist
        # Get the artist
        artist = input("What artist would you like to view? ")

        # Put it in a smaller data frame
        artist_data = df[df["artist"].str.contains(artist, case=False)]

        # Sort
        if len_type == "y":
            print(f"\nLongest songs featuring {artist.title()}")
            long_tracks = artist_data.sort_values(by="duration_ms", ascending=False).head(values)
            long_tracks["duration (mins)"] = long_tracks["duration_ms"].apply(convert_to_min)
            print(long_tracks[["track_num", "track_name", "album", "duration (mins)"]])
        elif len_type == "n":
            print(f"\nShortest songs featuring {artist.title()}:")
            short_tracks = artist_data.sort_values(by="popularity", ascending=True).head(values)
            short_tracks["duration (mins)"] = short_tracks["duration_ms"].apply(convert_to_min)
            print(short_tracks[["track_num", "track_name", "album" , "duration (mins)"]])


def convert_to_min(ms):
    secs = ms // 1000
    mins = secs // 60
    secs = secs % 60
    return f"{mins}:{secs:02}"


def convert_to_hr(ms):
    secs = ms // 1000
    mins = secs // 60
    hrs = mins // 60
    secs = secs % 60
    mins = mins % 60
    return f"{hrs}:{mins:02}:{secs:02}"


def main():
    """
    The main function of the program.
    """
    while True: 
        print("\nWhat would you like to do?")
        print("     1. View data")
        print("     2. Search for something")
        print("     3. Sort data")
        print("     4. Exit")
        choice = int(input("Select an option from above: "))

        if choice == 1:
            view_data()
        elif choice == 2:
            search()
        elif choice == 3:
            print("\nWhat data would you like to sort?")
            print("     1. Popularity")
            print("     2. Length")
            # print("     3. Date")
            choice = int(input("Select an option from above: "))

            if choice == 1:
                popularity()
            elif choice == 2:
                duration()
            elif choice == 3:
                # TODO
                pass
        elif choice == 4:
            break
        else:
            print("Not a valid option.")


if __name__ == '__main__':
    main()