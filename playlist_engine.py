from node import Node
import random

class PlaylistEngine:
    """
    Manages a playlist using a doubly linked list.
    Supports adding, deleting, moving, reversing songs,
    pinning songs at fixed positions, and shuffling with pins intact.
    """

    def __init__(self):
        self.head = None  # Start of the linked list
        self.tail = None  # End of the linked list
        self.size = 0     # Number of songs in the playlist
        self.reversed = False  # Flag for lazy reversal of playlist order
        self.pinned_songs = {}  # Maps song_id to pinned position index

    def add_song(self, song):
        """
        Adds a new song node to the playlist.
        Adds to tail if not reversed, else adds to head.
        Time Complexity: O(1)
        """
        new_node = Node(song)
        if not self.head:  # If playlist empty
            self.head = self.tail = new_node
        else:
            if not self.reversed:
                self.tail.next = new_node
                new_node.prev = self.tail
                self.tail = new_node
            else:
                self.head.prev = new_node
                new_node.next = self.head
                self.head = new_node
        self.size += 1

    def delete_song(self, index):
        """
        Removes a song node at the given index.
        Also removes pin if the song was pinned.
        Time Complexity: O(n) due to traversal.
        """
        if index < 0 or index >= self.size:
            return False
        node_to_delete = self._get_node(index)
        if not node_to_delete:
            return False

        # Remove pin if pinned
        if node_to_delete.song.song_id in self.pinned_songs:
            del self.pinned_songs[node_to_delete.song.song_id]

        # Update links to remove node
        if node_to_delete.prev:
            node_to_delete.prev.next = node_to_delete.next
        else:
            self.head = node_to_delete.next
        if node_to_delete.next:
            node_to_delete.next.prev = node_to_delete.prev
        else:
            self.tail = node_to_delete.prev

        self.size -= 1
        return True

    def move_song(self, from_index, to_index):
        """
        Moves a song node from one position to another within the playlist.
        Does not allow moving pinned songs or moving to pinned positions.
        Time Complexity: O(n)
        """
        if (from_index < 0 or from_index >= self.size or
            to_index < 0 or to_index >= self.size or
            from_index == to_index):
            return False

        node_to_move = self._get_node(from_index)
        if not node_to_move:
            return False

        # Prevent moving pinned songs or to pinned positions
        if node_to_move.song.song_id in self.pinned_songs:
            print("Cannot move a pinned song.")
            return False
        if to_index in self.pinned_songs.values():
            print("Cannot move song to a pinned position.")
            return False

        # Detach node from current location
        if node_to_move.prev:
            node_to_move.prev.next = node_to_move.next
        else:
            self.head = node_to_move.next
        if node_to_move.next:
            node_to_move.next.prev = node_to_move.prev
        else:
            self.tail = node_to_move.prev

        # Insert node at new position
        if to_index == 0:
            node_to_move.next = self.head
            node_to_move.prev = None
            if self.head:
                self.head.prev = node_to_move
            self.head = node_to_move
            if self.size == 1:
                self.tail = node_to_move
        else:
            before_node = self._get_node(to_index - 1)
            after_node = before_node.next
            before_node.next = node_to_move
            node_to_move.prev = before_node
            node_to_move.next = after_node
            if after_node:
                after_node.prev = node_to_move
            else:
                self.tail = node_to_move

        return True

    def reverse_playlist(self):
        """
        Toggles the reversed flag to reverse the playlist order lazily.
        Time Complexity: O(1)
        """
        self.reversed = not self.reversed

    def print_playlist(self):
        """
        Prints the playlist respecting the reversed flag.
        Marks pinned songs explicitly.
        Time Complexity: O(n)
        """
        print("Playlist:")
        if not self.head:
            print("<empty>")
            return

        if not self.reversed:
            current = self.head
            idx = 0
            while current:
                pin_marker = ' [PINNED]' if current.song.song_id in self.pinned_songs else ''
                print(f"{idx}: {current.song}{pin_marker}")
                current = current.next
                idx += 1
        else:
            current = self.tail
            idx = 0
            while current:
                pin_marker = ' [PINNED]' if current.song.song_id in self.pinned_songs else ''
                print(f"{idx}: {current.song}{pin_marker}")
                current = current.prev
                idx += 1

    def _get_node(self, index):
        """
        Returns the node at a specific index, accounting for reversal.
        Time Complexity: O(n)
        """
        if index < 0 or index >= self.size:
            return None

        current = self.head if not self.reversed else self.tail
        for _ in range(index):
            current = current.next if not self.reversed else current.prev
        return current

    def to_list(self):
        """
        Converts playlist into a list of songs in normal order (ignores reversed flag).
        Time Complexity: O(n), Space Complexity: O(n)
        """
        songs = []
        current = self.head if not self.reversed else self.tail
        while current:
            songs.append(current.song)
            current = current.next if not self.reversed else current.prev
        if self.reversed:
            songs.reverse()
        return songs

    def from_list(self, songs):
        """
        Rebuilds the playlist from a list of songs.
        Resets pinned songs and reversal state.
        Time Complexity: O(n)
        """
        self.head = None
        self.tail = None
        self.size = 0
        self.reversed = False
        self.pinned_songs = {}  # Clear all pins on rebuild

        for song in songs:
            self.add_song(song)

    def sort_playlist(self, criteria="title", ascending=True):
        """
        Sorts the playlist by title, duration, or recent addition.
        Uses Python's built-in sort (Timsort).
        Time Complexity: O(n log n)
        """
        songs = self.to_list()

        if criteria == "title":
            key_func = lambda s: s.title.lower()
        elif criteria == "duration":
            key_func = lambda s: s.duration
        elif criteria == "recent":
            key_func = lambda s: s.song_id
        else:
            print("Unknown sorting criteria. Sorting by title by default.")
            key_func = lambda s: s.title.lower()

        songs.sort(key=key_func, reverse=not ascending)

        self.from_list(songs)

    # --- Pinned Songs Methods ---

    def pin_song(self, song_id, index):
        """
        Pins a song to a specific index, preventing it from moving during shuffle.
        Returns True if successful, False otherwise.
        """
        if index < 0 or index >= self.size:
            print("Invalid index for pinning.")
            return False
        node = self._get_node(index)
        if not node or node.song.song_id != song_id:
            print("Song ID does not match song at given index.")
            return False
        self.pinned_songs[song_id] = index
        print(f"Pinned song '{node.song.title}' at position {index}.")
        return True

    def unpin_song(self, song_id):
        """
        Removes pin from a song if it was pinned.
        Returns True if unpinned, False if song wasn't pinned.
        """
        if song_id in self.pinned_songs:
            del self.pinned_songs[song_id]
            print(f"Unpinned song ID {song_id}.")
            return True
        print("Song ID not pinned.")
        return False

    def shuffle_playlist_with_pins(self):
        """
        Shuffle playlist randomly but keep pinned songs fixed at their positions.
        """
        if self.size == 0:
            print("Playlist empty.")
            return
        
        # Convert playlist to list for easier manipulation
        all_songs = self.to_list()

        # Create a map of pinned positions to song_ids
        pinned_positions = {v: k for k, v in self.pinned_songs.items()}  # index -> song_id
        pinned_indices = set(pinned_positions.keys())

        # Extract songs that are not pinned to shuffle them
        songs_to_shuffle = [song for idx, song in enumerate(all_songs) if idx not in pinned_indices]

        # Shuffle the non-pinned songs randomly
        random.shuffle(songs_to_shuffle)

        # Rebuild the playlist merging pinned songs back in place
        new_order = []
        shuffle_idx = 0
        for i in range(self.size):
            if i in pinned_indices:
                pinned_song_id = pinned_positions[i]
                pinned_song = next((s for s in all_songs if s.song_id == pinned_song_id), None)
                new_order.append(pinned_song)
            else:
                new_order.append(songs_to_shuffle[shuffle_idx])
                shuffle_idx += 1

        self.from_list(new_order)
        print("Playlist shuffled with pinned songs fixed.")
