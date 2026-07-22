from fastapi import APIRouter, Response
from src.monitoring.metrics import get_latest_metrics

router = APIRouter(tags=["Monitoring"])

@router.get("/metrics")
def get_metrics():
    content, media_type = get_latest_metrics()
    return Response(content=content, media_type=media_type)
