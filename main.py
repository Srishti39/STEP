from playlist_engine import PlaylistEngine
from playback_history import PlaybackHistory
from song import Song
from rating_bst import RatingBST
from system_snapshot import SystemSnapshot
from playlist_summary import PlaylistSummary  # <-- New import

def main():
    playlist = PlaylistEngine()
    history = PlaybackHistory()
    rating_tree = RatingBST()
    snapshot_module = SystemSnapshot(playlist, history, rating_tree)
    summary_module = PlaylistSummary(playlist)  # <-- Initialize summary module

    song_id_counter = 1

    while True:
        print("\n--- PlayWise Menu ---")
        print("1. Add a new song to playlist")
        print("2. Play a song (add to playback history)")
        print("3. Undo last played song")
        print("4. Show playlist")
        print("5. Exit")
        print("6. Search song by ID")
        print("7. Search song by Title")
        print("8. Pin a song at a specific position")
        print("9. Unpin a song")
        print("10. Shuffle playlist with pinned songs fixed")
        print("11. Sort playlist")
        print("12. Add song rating")
        print("13. Show songs by rating")
        print("14. Show system snapshot dashboard")
        print("15. Show Playlist Summary")  # <-- New menu option

        choice = input("Enter your choice (1-15): ")

        if choice == '1':
            title = input("Enter song title: ")
            artist = input("Enter artist name: ")
            try:
                duration = int(input("Enter duration in seconds: "))
            except ValueError:
                print("Invalid duration. Must be an integer.")
                continue
            song = Song(song_id_counter, title, artist, duration)
            playlist.add_song(song)
            rating_tree.insert_song(song, None)  # No rating initially
            print(f"Added '{title}' by {artist} to playlist with ID {song_id_counter}.")
            song_id_counter += 1

        elif choice == '2':
            if playlist.size == 0:
                print("Playlist is empty. Add songs first.")
                continue
            playlist.print_playlist()
            try:
                idx = int(input("Enter index of song to play: "))
            except ValueError:
                print("Invalid index.")
                continue
            node = playlist._get_node(idx)
            if not node:
                print("Invalid song index.")
                continue
            song = node.song
            history.push_song(song)
            print(f"Played: {song}")

        elif choice == '3':
            song = history.undo_last_play()
            if song:
                playlist.add_song(song)
                print(f"Re-added last played song: {song}")

        elif choice == '4':
            playlist.print_playlist()

        elif choice == '5':
            print("Exiting PlayWise. Goodbye!")
            break

        elif choice == '6':
            try:
                search_id = int(input("Enter song ID to search: "))
            except ValueError:
                print("Invalid ID.")
                continue
            found = False
            for idx in range(playlist.size):
                node = playlist._get_node(idx)
                if node.song.song_id == search_id:
                    print(f"Found song at index {idx}: {node.song}")
                    found = True
                    break
            if not found:
                print("No song found with that ID.")

        elif choice == '7':
            search_title = input("Enter song title to search: ").lower()
            found = False
            for idx in range(playlist.size):
                node = playlist._get_node(idx)
                if node.song.title.lower() == search_title:
                    print(f"Found song at index {idx}: {node.song}")
                    found = True
            if not found:
                print("No song found with that title.")

        elif choice == '8':
            if playlist.size == 0:
                print("Playlist empty, add songs first.")
                continue
            try:
                song_id = int(input("Enter song ID to pin: "))
                index = int(input("Enter position to pin the song at (0-based): "))
            except ValueError:
                print("Invalid input.")
                continue
            result = playlist.pin_song(song_id, index)
            if not result:
                print("Pinning failed.")

        elif choice == '9':
            try:
                song_id = int(input("Enter song ID to unpin: "))
            except ValueError:
                print("Invalid input.")
                continue
            result = playlist.unpin_song(song_id)
            if not result:
                print("Unpinning failed.")

        elif choice == '10':
            playlist.shuffle_playlist_with_pins()

        elif choice == '11':
            print("Sort by: 1. Title 2. Duration 3. Recently Added")
            sort_choice = input("Enter choice (1-3): ")
            criteria_map = {'1': 'title', '2': 'duration', '3': 'recent'}
            criteria = criteria_map.get(sort_choice, 'title')
            asc_choice = input("Sort ascending? (y/n): ").lower()
            ascending = True if asc_choice == 'y' else False
            playlist.sort_playlist(criteria, ascending)
            print("Playlist sorted.")

        elif choice == '12':
            if playlist.size == 0:
                print("Playlist empty, add songs first.")
                continue
            try:
                song_id = int(input("Enter song ID to rate: "))
                rating = int(input("Enter rating (1 to 5): "))
                if rating < 1 or rating > 5:
                    raise ValueError
            except ValueError:
                print("Invalid input for song ID or rating.")
                continue
            rating_tree.delete_song(song_id)
            song = None
            for idx in range(playlist.size):
                node = playlist._get_node(idx)
                if node.song.song_id == song_id:
                    song = node.song
                    break
            if not song:
                print("Song not found in playlist.")
                continue
            rating_tree.insert_song(song, rating)
            print(f"Rated song '{song.title}' with {rating} stars.")

        elif choice == '13':
            try:
                rating = int(input("Enter rating to search (1 to 5): "))
                if rating < 1 or rating > 5:
                    raise ValueError
            except ValueError:
                print("Invalid rating.")
                continue
            songs = rating_tree.search_by_rating(rating)
            if not songs:
                print(f"No songs found with rating {rating}.")
            else:
                print(f"Songs with rating {rating}:")
                for song in songs:
                    print(f"- {song}")

        elif choice == '14':
            snapshot = snapshot_module.export_snapshot()
            print("\n--- System Snapshot Dashboard ---")

            print("Top 5 Longest Songs:")
            for s in snapshot['top_5_longest_songs']:
                print(f"- {s}")

            print("\nMost Recently Played Songs:")
            for s in snapshot['most_recently_played_songs']:
                print(f"- {s}")

            print("\nSong Count by Rating:")
            for rating, count in snapshot['song_count_by_rating'].items():
                print(f"Rating {rating}: {count} song(s)")

        elif choice == '15':  # Playlist Summary option
            summary_module.print_summary()

        else:
            print("Invalid choice. Please enter a number between 1 and 15.")

if __name__ == "__main__":
    main()
