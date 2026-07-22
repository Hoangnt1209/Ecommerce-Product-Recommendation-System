from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.config.settings import settings
from src.api.routes import health, recommend, explain, metrics, ui

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Models load on the first cache miss. Cached responses can therefore be served
    # immediately after startup without deserializing the large ML checkpoints.
    yield
    # Shutdown event
    pass

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="End-to-End ML System with SVD Matrix Factorization, PyTorch Neural Collaborative Filtering (NCF), MLflow, Prometheus & Responsible AI.",
    version=settings.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix = settings.API_PREFIX if settings.API_PREFIX else ""

# Include modular API routers
app.include_router(ui.router, prefix=prefix)
app.include_router(health.router, prefix=prefix)
app.include_router(recommend.router, prefix=prefix)
app.include_router(explain.router, prefix=prefix)
app.include_router(metrics.router, prefix=prefix)

if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
