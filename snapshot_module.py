class SnapshotModule:
    """
    Aggregates and exports a snapshot summary of the current system state:
    - Playlist details
    - Playback history
    - Rating distribution
    """

    def __init__(self, playlist_engine, playback_history, rating_tree):
        """
        Initialize with references to core modules:
        playlist_engine: PlaylistEngine instance
        playback_history: PlaybackHistory instance
        rating_tree: RatingBST instance
        """
        self.playlist_engine = playlist_engine
        self.playback_history = playback_history
        self.rating_tree = rating_tree

    def export_snapshot(self):
        """
        Generates a dictionary snapshot containing:
        1. Top 5 longest songs from the playlist
        2. 5 most recently played songs from playback history
        3. Counts of songs by their rating from the rating BST

        Returns:
            dict: Snapshot data
        """
        snapshot = {}

        # 1. Get all songs from playlist, sort descending by duration, pick top 5
        songs = self.playlist_engine.to_list()
        sorted_by_duration = sorted(songs, key=lambda s: s.duration, reverse=True)
        snapshot['top_5_longest_songs'] = [
            {'title': s.title, 'artist': s.artist, 'duration': s.duration} 
            for s in sorted_by_duration[:5]
        ]

        # 2. Most recent songs are last pushed on playback stack - reverse stack to get recent first
        recent_songs = self.playback_history.stack[::-1]
        snapshot['most_recently_played'] = [
            {'title': s.title, 'artist': s.artist, 'duration': s.duration} 
            for s in recent_songs[:5]
        ]

        # 3. Count songs grouped by rating from the rating BST
        rating_counts = {}
        def count_songs_by_rating(node):
            if not node:
                return
            rating_counts[node.rating] = len(node.songs)
            count_songs_by_rating(node.left)
            count_songs_by_rating(node.right)

        count_songs_by_rating(self.rating_tree.root)
        snapshot['song_count_by_rating'] = rating_counts

        return snapshot
