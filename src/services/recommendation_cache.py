import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional


class RecommendationCache:
    """Versioned, persistent JSON cache for recommendation API responses."""

    def __init__(self, cache_dir: str, checkpoint_dir: str):
        self.cache_dir = Path(cache_dir)
        self.checkpoint_dir = Path(checkpoint_dir)

    def _model_fingerprint(self) -> str:
        """Return a stable version derived from the model artifacts on disk."""
        artifacts = [
            "preprocessor.pkl",
            "svd_model.pkl",
            "content_model.pkl",
            "assoc_model.pkl",
            "pytorch_ncf.pt",
        ]
        state = []
        for artifact in artifacts:
            path = self.checkpoint_dir / artifact
            if path.exists():
                stat = path.stat()
                state.append((artifact, stat.st_size, stat.st_mtime_ns))
            else:
                state.append((artifact, None, None))
        serialized = json.dumps(state, separators=(",", ":"), sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]

    def _path_for(self, namespace: str, payload: Dict[str, Any]) -> Path:
        key_payload = {
            "namespace": namespace,
            "model_fingerprint": self._model_fingerprint(),
            "payload": payload,
        }
        digest = hashlib.sha256(
            json.dumps(key_payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        ).hexdigest()
        return self.cache_dir / f"{namespace}-{digest}.json"

    def get(self, namespace: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        path = self._path_for(namespace, payload)
        try:
            with path.open("r", encoding="utf-8") as file:
                cached = json.load(file)
            return cached if isinstance(cached, dict) else None
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return None

    def set(self, namespace: str, payload: Dict[str, Any], result: Dict[str, Any]) -> None:
        path = self._path_for(namespace, payload)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        temp_path: Optional[str] = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=self.cache_dir, delete=False
            ) as file:
                json.dump(result, file, ensure_ascii=False, separators=(",", ":"))
                temp_path = file.name
            os.replace(temp_path, path)
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
