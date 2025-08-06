class BSTNode:
    def __init__(self, rating):
        """
        Node representing a rating bucket in the BST.
        Holds all songs with the same rating.
        """
        self.rating = rating
        self.songs = []  # List of songs sharing this rating
        self.left = None
        self.right = None

class RatingBST:
    """
    Binary Search Tree (BST) where each node is a rating bucket (1 to 5 stars).
    Allows fast insertion, deletion, and search of songs by their rating.
    """

    def __init__(self):
        self.root = None

    def insert_song(self, song, rating):
        """
        Insert a song into the BST under the given rating bucket.
        If rating is None, skip insertion.

        Time Complexity: O(h), h = height of the BST
        """
        if rating is None:
            # Skip inserting unrated songs
            return
        self.root = self._insert(self.root, song, rating)

    def _insert(self, node, song, rating):
        """
        Recursive helper to insert song into BST.
        """
        if node is None:
            node = BSTNode(rating)
            node.songs.append(song)
            return node

        if rating < node.rating:
            node.left = self._insert(node.left, song, rating)
        elif rating > node.rating:
            node.right = self._insert(node.right, song, rating)
        else:
            # Rating bucket exists, append song
            node.songs.append(song)
        return node

    def search_by_rating(self, rating):
        """
        Search BST for rating bucket and return list of songs with that rating.
        Returns empty list if not found.
        """
        node = self._search(self.root, rating)
        if node:
            return node.songs
        return []

    def _search(self, node, rating):
        """
        Recursive BST search by rating.
        """
        if node is None:
            return None
        if rating == node.rating:
            return node
        elif rating < node.rating:
            return self._search(node.left, rating)
        else:
            return self._search(node.right, rating)

    def delete_song(self, song_id):
        """
        Remove a song by ID from the BST.
        Removes the rating bucket node if no songs remain in that bucket.
        """
        self.root = self._delete_song(self.root, song_id)

    def _delete_song(self, node, song_id):
        """
        Recursive helper to remove a song from the BST nodes.
        """
        if node is None:
            return None

        # Remove song from current node's list
        node.songs = [s for s in node.songs if s.song_id != song_id]

        if not node.songs:
            # If no songs left in this rating bucket, delete this BST node
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children: find inorder successor to replace this node
            successor = self._min_value_node(node.right)
            node.rating = successor.rating
            node.songs = successor.songs
            node.right = self._delete_node(node.right, successor.rating)
        else:
            # Songs remain, keep the node
            # Since deletion is by song_id, this part is a safe fallback; no further traversal needed.
            pass

        return node

    def _delete_node(self, node, rating):
        """
        Helper function to delete a node by rating value (used when a bucket is empty).
        """
        if node is None:
            return None
        if rating < node.rating:
            node.left = self._delete_node(node.left, rating)
        elif rating > node.rating:
            node.right = self._delete_node(node.right, rating)
        else:
            # Node to delete found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # Node has two children: replace with inorder successor
            successor = self._min_value_node(node.right)
            node.rating = successor.rating
            node.songs = successor.songs
            node.right = self._delete_node(node.right, successor.rating)
        return node

    def _min_value_node(self, node):
        """
        Find the node with minimum rating value in the BST subtree.
        """
        current = node
        while current.left:
            current = current.left
        return current

    def count_songs_by_rating(self):
        """
        Traverse the BST inorder and count the number of songs in each rating bucket (1 to 5).

        Returns:
            dict: {rating: count_of_songs}

        Time Complexity: O(n), n = number of BST nodes
        """
        counts = {rating: 0 for rating in range(1, 6)}

        def inorder_count(node):
            if not node:
                return
            inorder_count(node.left)
            if node.rating in counts:
                counts[node.rating] = len(node.songs)
            inorder_count(node.right)

        inorder_count(self.root)
        return counts
