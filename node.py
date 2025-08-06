class Node:
    """
    Represents a node in a doubly linked list for the playlist.
    Each node holds a 'song' object and pointers to the previous and next nodes.
    """

    def __init__(self, song):
        self.song = song       # The song object stored in this node
        self.prev = None       # Pointer to the previous node in the list
        self.next = None       # Pointer to the next node in the list
