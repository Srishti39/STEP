class Song:
    def __init__(self, song_id, title, artist, duration, genre=None):
        """
        Represents a song with basic metadata.

        Args:
            song_id (int): Unique identifier for the song.
            title (str): Title of the song.
            artist (str): Artist name.
            duration (int): Duration of the song in seconds.
            genre (str, optional): Genre of the song (e.g., Pop, Rock). Defaults to None.
        """
        self.song_id = song_id
        self.title = title
        self.artist = artist
        self.duration = duration  # stored as seconds for easier computation
        self.genre = genre  # optional, can be None if unknown

    def __str__(self):
        """
        Returns a human-readable string representation of the song,
        useful for printing and logging.
        """
        return f"{self.title} by {self.artist} ({self.duration} sec)"
