from fastapi import APIRouter
from src.services.recommendation_service import recommendation_service

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "system": "Production Recommendation Engine",
        "models_loaded": recommendation_service.recommender is not None
    }
