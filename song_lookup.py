class SongLookup:
    """
    Provides fast lookup of songs by their unique ID or by title (case-insensitive).
    Maintains internal dictionaries to enable quick retrieval and updates.
    """

    def __init__(self):
        # Dictionary mapping song ID to Song object for O(1) lookup by ID
        self.id_map = {}
        # Dictionary mapping lowercase song title to list of Song objects for O(1) title-based lookup
        self.title_map = {}

    def add_song(self, song):
        """
        Add a song to the lookup maps.
        Updates both ID and title dictionaries.
        """
        self.id_map[song.song_id] = song
        title_key = song.title.lower()
        if title_key not in self.title_map:
            self.title_map[title_key] = []
        self.title_map[title_key].append(song)

    def remove_song(self, song):
        """
        Remove a song from the lookup maps.
        Removes by ID and updates title mapping accordingly.
        """
        self.id_map.pop(song.song_id, None)  # Remove from ID map if exists
        title_key = song.title.lower()
        if title_key in self.title_map:
            # Remove song from the list of songs under that title
            self.title_map[title_key] = [
                s for s in self.title_map[title_key] if s.song_id != song.song_id
            ]
            # If no songs remain for this title, remove the title key
            if not self.title_map[title_key]:
                del self.title_map[title_key]

    def search_by_id(self, song_id):
        """
        Search and return the Song object by its unique ID.
        Returns None if not found.
        """
        return self.id_map.get(song_id)

    def search_by_title(self, title):
        """
        Search and return a list of Song objects matching the title (case-insensitive).
        Returns empty list if no match found.
        """
        return self.title_map.get(title.lower(), [])

    def print_all_songs(self):
        """
        Print all songs currently in the lookup maps.
        Useful for debugging or displaying the full list.
        """
        print("All songs in lookup:")
        for song_id, song in self.id_map.items():
            print(song)
