"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile: target values the recommender compares each song against.
    #   genre         -> exact match vs. Song.genre        (categorical)
    #   mood          -> exact match vs. Song.mood         (categorical)
    #   energy        -> proximity to Song.energy          (numeric 0-1, closer = better)
    #   likes_acoustic-> preference vs. Song.acousticness  (boolean: prefer high/low acousticness)
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 44)
    print("  TOP RECOMMENDATIONS")
    print("=" * 44 + "\n")

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f}")
        print("   Why:")
        for reason in explanation.split(", "):
            print(f"     • {reason}")
        print()


if __name__ == "__main__":
    main()
