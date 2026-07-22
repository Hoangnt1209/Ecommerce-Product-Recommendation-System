from pathlib import Path

from src.services.recommendation_cache import RecommendationCache


def test_cache_persists_and_returns_a_response(tmp_path: Path):
    checkpoint_dir = tmp_path / "checkpoints"
    checkpoint_dir.mkdir()
    (checkpoint_dir / "preprocessor.pkl").write_text("model-v1", encoding="utf-8")
    cache = RecommendationCache(str(tmp_path / "cache"), str(checkpoint_dir))
    payload = {"user_id": "user-1", "top_k": 8, "model_type": "hybrid"}
    expected = {"user_id": "user-1", "cross_sell_items": [{"asin": "item-1"}]}

    assert cache.get("user", payload) is None
    cache.set("user", payload, expected)

    reloaded_cache = RecommendationCache(str(tmp_path / "cache"), str(checkpoint_dir))
    assert reloaded_cache.get("user", payload) == expected


def test_checkpoint_change_invalidates_cached_response(tmp_path: Path):
    checkpoint_dir = tmp_path / "checkpoints"
    checkpoint_dir.mkdir()
    artifact = checkpoint_dir / "preprocessor.pkl"
    artifact.write_text("model-v1", encoding="utf-8")
    cache = RecommendationCache(str(tmp_path / "cache"), str(checkpoint_dir))
    payload = {"user_id": "user-1", "top_k": 8, "model_type": "hybrid"}
    cache.set("user", payload, {"user_id": "user-1"})

    artifact.write_text("model-version-2", encoding="utf-8")

    assert cache.get("user", payload) is None
