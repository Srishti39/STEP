class SystemSnapshot:
    def __init__(self, playlist_engine, playback_history, rating_bst):
        """
        Initialize the SystemSnapshot module with references to the main components.

        Args:
            playlist_engine (PlaylistEngine): The playlist manager instance.
            playback_history (PlaybackHistory): The playback history stack instance.
            rating_bst (RatingBST): The rating binary search tree instance.
        """
        self.playlist_engine = playlist_engine
        self.playback_history = playback_history
        self.rating_bst = rating_bst

    def export_snapshot(self):
        """
        Generate a snapshot summary of the system state containing:

        - Top 5 longest songs currently in the playlist.
        - Most recently played 5 songs from playback history.
        - Counts of songs grouped by their ratings.

        Returns:
            dict: A dictionary with keys:
                'top_5_longest_songs': List of Song objects (top 5 by duration).
                'most_recently_played_songs': List of Song objects (last 5 played).
                'song_count_by_rating': Dict mapping rating (1-5) to count of songs.
        """
        # Fetch all songs currently in the playlist
        songs = self.playlist_engine.to_list()

        # Sort songs by duration descending to find the longest ones
        top_5_longest_songs = sorted(songs, key=lambda s: s.duration, reverse=True)[:5]

        # Get last 5 played songs from playback history stack (newest first)
        recent_played = self.playback_history.stack[-5:]
        most_recently_played_songs = recent_played[::-1]

        # Get count of songs for each rating from the rating BST
        song_count_by_rating = self.rating_bst.count_songs_by_rating()

        # Return snapshot data as a dictionary
        return {
            "top_5_longest_songs": top_5_longest_songs,
            "most_recently_played_songs": most_recently_played_songs,
            "song_count_by_rating": song_count_by_rating
        }
