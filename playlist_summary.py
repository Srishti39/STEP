from collections import Counter

class PlaylistSummary:
    """
    Generates and prints summary statistics about a playlist.
    """

    def __init__(self, playlist):
        """
        Initialize with a PlaylistEngine object.

        Args:
            playlist (PlaylistEngine): The playlist to summarize.
        """
        self.playlist = playlist

    def generate_summary(self):
        """
        Generate summary information about the playlist:
        - Distribution of genres (if genre info exists)
        - Total duration of all songs (in seconds)
        - Count of unique artists

        Returns:
            dict: {
                'genre_distribution': {genre: count, ...},
                'total_playtime': int,
                'artist_count': int
            }

        Time Complexity: O(n), where n is the number of songs.
        Space Complexity: O(n) for tracking counts.
        """
        songs = self.playlist.to_list()

        genre_counter = Counter()
        total_playtime = 0
        artist_set = set()

        for song in songs:
            # If the Song object has a 'genre' attribute, count it
            if hasattr(song, 'genre'):
                genre_counter[song.genre] += 1
            total_playtime += song.duration
            artist_set.add(song.artist)

        summary = {
            'genre_distribution': dict(genre_counter),
            'total_playtime': total_playtime,
            'artist_count': len(artist_set)
        }
        return summary

    def print_summary(self):
        """
        Print the generated summary in a user-friendly format.
        Handles case when genre info is missing.
        """
        summary = self.generate_summary()
        print("\n--- Playlist Summary ---")
        if summary['genre_distribution']:
            print("Genre Distribution:")
            for genre, count in summary['genre_distribution'].items():
                print(f"  {genre}: {count} song(s)")
        else:
            print("Genre Distribution: Not available (no genre info)")

        print(f"Total Playtime: {summary['total_playtime']} seconds")
        print(f"Unique Artists: {summary['artist_count']}")
