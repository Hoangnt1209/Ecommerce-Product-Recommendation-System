"""Precompute persistent recommendations for representative users.

Run after training or checkpoint replacement:
    python scripts/warm_recommendation_cache.py --count 30 --top-k 8
"""
import argparse
import sys
from pathlib import Path

# Allow `python scripts/warm_recommendation_cache.py` from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.services.recommendation_service import recommendation_service


def main() -> None:
    parser = argparse.ArgumentParser(description="Warm the persistent recommendation cache.")
    parser.add_argument("--count", type=int, default=30, help="Number of sample users to cache.")
    parser.add_argument("--top-k", type=int, default=8, help="Recommendations stored per user.")
    parser.add_argument("--model-type", default="hybrid", help="Recommendation model type to cache.")
    args = parser.parse_args()

    user_ids = recommendation_service.get_sample_users(count=args.count)
    for index, user_id in enumerate(user_ids, start=1):
        recommendation_service.recommend(
            user_id=user_id,
            top_k=args.top_k,
            model_type=args.model_type,
        )
        print(f"Cached {index}/{len(user_ids)}: {user_id}")

    print(f"Finished caching {len(user_ids)} user recommendation responses.")


if __name__ == "__main__":
    main()
