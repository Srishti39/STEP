What is PlayWise?

1) Backend engine to manage personalized music playlists smartly
2) Supports adding, deleting, reordering, reversing songs
3) Tracks playback history with undo functionality
4) Organizes songs by user ratings
5) Enables fast song lookup by ID or title
6) Allows sorting and pinning of songs within playlists
7) Provides summary dashboard with playlist insights


Key Features

1) Playlist Engine: Doubly linked list for efficient song management
2) Playback History: Stack to undo last played songs
3) Song Ratings: Binary Search Tree grouping songs by ratings (1–5 stars)
4) Instant Lookup: HashMap for O(1) retrieval by song ID or title
5) Sorting: Merge sort for sorting playlists by title, duration, or recent addition
6) Pinning: Fix songs at specific positions even when shuffling
7) Dashboard: Quick stats on longest songs, recent plays, and rating counts


Technical Overview

1) Doubly Linked List:
Fast insertions, deletions, and reordering without data shifts
2) Stack: 
LIFO structure for undoing playback
3) BST: 
Efficient insertion, deletion, and search by rating buckets
4) HashMap:
Constant-time lookup synced with playlist updates
5) Merge Sort: 
Stable, efficient sorting algorithm with O(n log n) complexity
6) Pinning: 
Maintains pinned song positions via hashmap during shuffle


Performance Summary

| Operation             | Time Complexity  |
| --------------------- | ---------------- |
| Add/Delete/Move Song  | O(1) – O(n)      |
| Undo Last Played Song | O(1)             |
| Insert/Search in BST  | O(log n) average |
| Lookup by ID/Title    | O(1)             |
| Sort Playlist         | O(n log n)       |
| Pin/Unpin Song        | O(1)             |


How to Run

1) Install Python 3.13 or above
2) Place all .py source files in the same folder
3) Open terminal or command prompt, navigate to project folder
4) Run: python main.py
5) Use the interactive menu to manage playlists and explore features