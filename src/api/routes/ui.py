import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Web UI"])

@router.get("/", response_class=HTMLResponse)
def serve_dashboard():
    template_path = os.path.join("src", "templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
            return HTMLResponse(content=content)
    return HTMLResponse(content="<h1>Recommendation System Dashboard Template Not Found</h1>")
