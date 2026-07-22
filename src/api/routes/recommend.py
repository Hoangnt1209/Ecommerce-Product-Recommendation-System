import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any

from src.services.recommendation_service import recommendation_service
from src.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY, ERROR_COUNT

router = APIRouter(tags=["Recommendation & Catalog"])

class RecommendationRequest(BaseModel):
    user_id: str = Field(..., json_schema_extra={"example": "A30TL5EWN6DFXT"}, description="Amazon Reviewer ID")
    top_k: int = Field(default=10, ge=1, le=50, description="Number of items to recommend")
    model_type: str = Field(default="hybrid", json_schema_extra={"example": "hybrid"}, description="Model engine: 'hybrid', 'ncf', 'svd', 'content'")

class RecommendationResponse(BaseModel):
    user_id: str
    is_cold_start: bool
    model_used: str
    user_history: List[Dict[str, Any]] = []
    similar_items: List[Dict[str, Any]] = []
    cross_sell_items: List[Dict[str, Any]] = []
    trending_items: List[Dict[str, Any]] = []
    recommendations: List[Dict[str, Any]] = []

@router.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(req: RecommendationRequest):
    start_time = time.time()
    REQUEST_COUNT.labels(model_type=req.model_type).inc()
    
    try:
        result = recommendation_service.recommend(
            user_id=req.user_id,
            top_k=req.top_k,
            model_type=req.model_type
        )
        result["user_history"] = recommendation_service.get_user_history(req.user_id)
    except Exception as e:
        ERROR_COUNT.labels(error_type="recommendation").inc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        latency = time.time() - start_time
        REQUEST_LATENCY.observe(latency)
    return result

@router.get("/sample-users")
def get_sample_users(count: int = 10):
    return {"users": recommendation_service.get_sample_users(count=count)}

@router.get("/user-history/{user_id}")
def get_user_history_endpoint(user_id: str):
    history = recommendation_service.get_user_history(user_id)
    is_cold = len(history) == 0
    return {
        "user_id": user_id,
        "is_cold_start": is_cold,
        "history": history
    }

@router.get("/items")
def get_catalog_items(query: str = "", limit: int = 20):
    return {"items": recommendation_service.get_catalog_items(query=query, limit=limit)}

class InteractiveRecommendationRequest(BaseModel):
    selected_asins: List[str] = Field(..., description="List of selected ASINs by user")
    top_k: int = Field(default=8, ge=1, le=50)

@router.post("/recommend-interactive", response_model=RecommendationResponse)
def get_interactive_recommendations(req: InteractiveRecommendationRequest):
    start_time = time.time()
    REQUEST_COUNT.labels(model_type="content").inc()
    
    try:
        result = recommendation_service.recommend_from_items(
            selected_asins=req.selected_asins,
            top_k=req.top_k
        )
    except Exception as e:
        ERROR_COUNT.labels(error_type="interactive").inc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        latency = time.time() - start_time
        REQUEST_LATENCY.observe(latency)
    return result
