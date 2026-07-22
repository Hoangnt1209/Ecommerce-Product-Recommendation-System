import os
import pickle
import torch
from typing import Optional, Dict, Any, List

from src.config.settings import settings
from src.data.preprocessor import DataPreprocessor
from src.models.classical_ml import SVDRecommender, ContentBasedRecommender
from src.models.deep_learning import NeuralCollaborativeFiltering, NCFTrainer
from src.models.hybrid import HybridRecommender
from src.services.recommendation_cache import RecommendationCache
from src.monitoring.metrics import MODEL_LOAD_TIME, ERROR_COUNT

class RecommendationService:
    def __init__(self):
        self.recommender: Optional[HybridRecommender] = None
        self.cache = RecommendationCache(
            cache_dir=settings.RECOMMENDATION_CACHE_DIR,
            checkpoint_dir=settings.CHECKPOINT_DIR,
        )

    def ensure_models_loaded(self):
        if self.recommender is None:
            self._load_models()

    def _load_models(self):
        import time as _time
        _load_start = _time.time()
        checkpoint_dir = settings.CHECKPOINT_DIR
        prep_path = os.path.join(checkpoint_dir, "preprocessor.pkl")
        svd_path = os.path.join(checkpoint_dir, "svd_model.pkl")
        content_path = os.path.join(checkpoint_dir, "content_model.pkl")
        assoc_path = os.path.join(checkpoint_dir, "assoc_model.pkl")
        ncf_weights_path = os.path.join(checkpoint_dir, "pytorch_ncf.pt")

        if not os.path.exists(prep_path) or not os.path.exists(assoc_path):
            print("[RecommendationService] Checkpoints or Association Rules not found. Triggering training pipeline...")
            from src.models.train import train_and_evaluate
            train_and_evaluate(sample_limit=10000, epochs=2)

        with open(prep_path, "rb") as f:
            prep: DataPreprocessor = pickle.load(f)
        with open(svd_path, "rb") as f:
            svd_model: SVDRecommender = pickle.load(f)
        with open(content_path, "rb") as f:
            content_model: ContentBasedRecommender = pickle.load(f)
            
        assoc_model = None
        if os.path.exists(assoc_path):
            with open(assoc_path, "rb") as f:
                assoc_model = pickle.load(f)

        ncf_model = NeuralCollaborativeFiltering(
            num_users=prep.num_users,
            num_items=prep.num_items,
            embedding_dim=settings.EMBEDDING_DIM
        )
        if os.path.exists(ncf_weights_path):
            ncf_model.load_state_dict(torch.load(ncf_weights_path, map_location="cpu"))
        ncf_model.eval()
        ncf_trainer = NCFTrainer(ncf_model, device="cpu")

        self.recommender = HybridRecommender(
            svd_model=svd_model,
            content_model=content_model,
            ncf_trainer=ncf_trainer,
            preprocessor=prep,
            assoc_model=assoc_model
        )
        _load_elapsed = _time.time() - _load_start
        MODEL_LOAD_TIME.set(_load_elapsed)
        print(f"[RecommendationService] Production ML Models & Data-Driven Association Miner Successfully Initialized! (loaded in {_load_elapsed:.1f}s)")

    def recommend(self, user_id: str, top_k: int = 10, model_type: str = "hybrid") -> Dict[str, Any]:
        request_payload = {
            "user_id": user_id,
            "top_k": top_k,
            "model_type": model_type,
        }
        cached = self.cache.get("user", request_payload)
        if cached is not None:
            return cached

        self.ensure_models_loaded()
        if self.recommender is None:
            raise RuntimeError("Recommendation service models not loaded.")
        result = self.recommender.recommend(user_id=user_id, top_k=top_k, model_type=model_type)
        self.cache.set("user", request_payload, result)
        return result

    def recommend_from_items(self, selected_asins: List[str], top_k: int = 10) -> Dict[str, Any]:
        request_payload = {
            "selected_asins": sorted(selected_asins),
            "top_k": top_k,
        }
        cached = self.cache.get("interactive", request_payload)
        if cached is not None:
            return cached

        self.ensure_models_loaded()
        if self.recommender is None:
            raise RuntimeError("Recommendation service models not loaded.")
        result = self.recommender.recommend_from_selected_items(selected_asins, top_k=top_k)
        self.cache.set("interactive", request_payload, result)
        return result

    def get_sample_users(self, count: int = 15) -> List[str]:
        self.ensure_models_loaded()
        if self.recommender is None:
            return []
            
        phone_users = []
        electronics_users = []
        mixed_users = []
        
        for uid, history in self.recommender.prep.user_history.items():
            cats = [h.get('category', '').lower() for h in history]
            has_phone = any('cell' in c for c in cats)
            has_elec = any('electronics' in c for c in cats)
            if has_phone and has_elec:
                mixed_users.append(uid)
            elif has_elec:
                electronics_users.append(uid)
            elif has_phone:
                phone_users.append(uid)
                
        n_group = max(1, count // 3)
        sample = phone_users[:n_group] + electronics_users[:n_group] + mixed_users[:n_group]
        return sample[:count]

    def get_user_history(self, user_id: str) -> List[Dict[str, Any]]:
        self.ensure_models_loaded()
        if self.recommender is None or not hasattr(self.recommender.prep, 'user_history'):
            return []
        return self.recommender.prep.user_history.get(user_id, [])

    def get_catalog_items(self, query: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        self.ensure_models_loaded()
        if self.recommender is None:
            return []
        items = list(self.recommender.prep.item_meta.values())
        if query:
            q_lower = query.lower()
            items = [it for it in items if q_lower in it.get('title', '').lower() or q_lower in it.get('category', '').lower()]
        return items[:limit]

# Singleton Service Instance
recommendation_service = RecommendationService()
