from typing import Dict, Any, List
from src.services.recommendation_service import recommendation_service
from src.explainability.explainer import ModelExplainerAndFairness

class ExplainabilityService:
    def __init__(self):
        self._explainer = None

    @property
    def explainer(self) -> ModelExplainerAndFairness:
        if self._explainer is None:
            recommendation_service.ensure_models_loaded()
            self._explainer = ModelExplainerAndFairness(recommendation_service.recommender)
        return self._explainer

    def explain(self, user_id: str, asin: str) -> Dict[str, Any]:
        return self.explainer.explain_recommendation(user_id, asin)

    def audit_fairness(self) -> Dict[str, Any]:
        recommendation_service.ensure_models_loaded()
        sample_users = list(recommendation_service.recommender.prep.user_to_idx.keys())[:50]
        return self.explainer.audit_fairness_and_bias(sample_users)

explainability_service = ExplainabilityService()
