"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# Taste profiles: target values the recommender compares each song against.
#   genre         -> exact match vs. Song.genre        (categorical)
#   mood          -> exact match vs. Song.mood         (categorical)
#   energy        -> proximity to Song.energy          (numeric 0-1, closer = better)
#   likes_acoustic-> preference vs. Song.acousticness  (boolean: prefer high/low acousticness)
USER_PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.85,
        "likes_acoustic": False,
    },
    # --- Adversarial / edge-case profiles ---
    # Conflicting energy + mood. Also note: "sad" is NOT a mood in the
    # dataset, so the mood term silently scores 0 (unknown/typo value) —
    # the contradiction is invisible and high-energy pop still gets served.
    "Conflicting Sad High-Energy": {
        "genre": "pop",
        "mood": "sad",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    # Out-of-range energy. score_song never clamps target energy, so
    # 1 - abs(song.energy - 5.0) goes negative and total scores turn negative.
    "Out-of-Range Energy": {
        "genre": "rock",
        "mood": "intense",
        "energy": 5.0,
        "likes_acoustic": False,
    },
}


def print_recommendations(name: str, recommendations) -> None:
    print("\n" + "=" * 44)
    print(f"  {name.upper()}")
    print("=" * 44 + "\n")

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f}")
        print("   Why:")
        for reason in explanation.split(", "):
            print(f"     • {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in USER_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, recommendations)


if __name__ == "__main__":
    main()
