from fastapi import APIRouter
from src.services.explainability_service import explainability_service

router = APIRouter(tags=["Responsible AI & Explainability"])

@router.get("/explain")
def explain(user_id: str, asin: str):
    return explainability_service.explain(user_id, asin)

@router.get("/fairness")
def audit_fairness():
    return explainability_service.audit_fairness()
