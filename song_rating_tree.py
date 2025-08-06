# song_rating_tree.py

class BSTNode:
    def __init__(self, rating):
        self.rating = rating  # The rating value (1 to 5) that acts as the key for this BST node
        self.songs = []       # List of songs that share this rating
        self.left = None      # Left child node for ratings less than current
        self.right = None     # Right child node for ratings greater than current

class SongRatingBST:
    def __init__(self):
        self.root = None  # Root of the BST, initially empty

    def insert_song(self, song, rating):
        """
        Insert a song into the BST, placing it under the correct rating bucket.
        Since ratings are limited (1 to 5), tree height is small (max 5 nodes),
        so this operation is practically constant time.

        Args:
            song: Song object to insert
            rating: Integer rating (1 to 5)
        """
        def insert_node(node, rating):
            # If reached a leaf position, create new node and add the song
            if node is None:
                node = BSTNode(rating)
                node.songs.append(song)
                return node
            
            if rating < node.rating:
                node.left = insert_node(node.left, rating)
            elif rating > node.rating:
                node.right = insert_node(node.right, rating)
            else:
                # Found matching rating node; just append the song to this node's list
                node.songs.append(song)
            return node

        self.root = insert_node(self.root, rating)

    def search_by_rating(self, rating):
        """
        Search the BST for the node with the specified rating and return all songs in that bucket.

        Args:
            rating: Integer rating to search for

        Returns:
            List of songs with that rating, or empty list if none found.
        """
        current = self.root
        while current:
            if rating == current.rating:
                return current.songs
            elif rating < current.rating:
                current = current.left
            else:
                current = current.right
        return []

    def delete_song(self, song_id):
        """
        Delete a song by its ID from the rating buckets.
        This requires searching through all rating nodes because
        song_id doesn't correspond to rating directly.

        Args:
            song_id: Unique identifier of the song to delete

        Returns:
            True if song was found and deleted, False otherwise.
        """
        def delete_from_list(songs, song_id):
            # Helper to delete a song from the list by song_id
            for i, s in enumerate(songs):
                if s.song_id == song_id:
                    songs.pop(i)
                    return True
            return False

        def delete_song_from_node(node):
            # Recursively search nodes to find and delete song
            if node is None:
                return False
            if delete_from_list(node.songs, song_id):
                return True
            # If not found, search left and right subtrees
            return delete_song_from_node(node.left) or delete_song_from_node(node.right)

        return delete_song_from_node(self.root)
