class PlaybackHistory:
    """
    Manages the playback history using a stack.
    Allows tracking recently played songs and supports undoing the last played song.
    """

    def __init__(self):
        self.stack = []  # Stack to hold recently played songs, with the most recent on top

    def push_song(self, song):
        """
        Add a song to the playback history stack when it is played.
        Time Complexity: O(1)
        """
        self.stack.append(song)

    def undo_last_play(self):
        """
        Undo the last played song by removing it from the top of the stack.
        Returns the song to be re-added to the playlist.
        Time Complexity: O(1)
        """
        if not self.stack:
            print("No song to undo.")  # Inform user if no songs are in history
            return None
        return self.stack.pop()  # Remove and return the last played song

    def print_history(self):
        """
        Print the playback history from the oldest played song to the most recent.
        Useful for debugging or displaying user history.
        Time Complexity: O(n), where n is the number of songs in history.
        """
        print("Playback History (oldest to newest):")
        for i, song in enumerate(self.stack):
            print(f"{i}: {song}")
