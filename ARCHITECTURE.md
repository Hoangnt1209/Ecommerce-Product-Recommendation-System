# Production MLOps & Backend AI Architecture

## 1. Clean Layered Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                Presentation & API Layer                           |
|  - src/templates/index.html (Web Dashboard)                                      |
|  - src/api/routes/ (Modular APIRouters: health, recommend, explain, metrics, ui) |
|  - src/api/main.py (FastAPI Application Entrypoint)                              |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+------------------------------------------+----------------------------------------+
|                                 Service & Business Layer                          |
|  - src/services/recommendation_service.py (Inference Engine Wrapper)            |
|  - src/services/explainability_service.py (SHAP / Fairness Audit Wrapper)       |
|  - src/monitoring/metrics.py (Prometheus Metrics Collector)                       |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+------------------------------------------+----------------------------------------+
|                                Core ML & Model Layer                              |
|  - src/models/classical_ml.py (Truncated SVD & Content TF-IDF)                    |
|  - src/models/deep_learning.py (PyTorch Neural Collaborative Filtering - NCF)    |
|  - src/models/hybrid.py (Hybrid Score Fusion & Cold-Start Popularity Engine)      |
|  - src/models/train.py (MLflow Training Pipeline Orchestrator)                   |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+------------------------------------------+----------------------------------------+
|                              Data & Configuration Layer                           |
|  - src/config/settings.py (Centralized Pydantic BaseSettings)                    |
|  - src/data/loader.py (Streaming Multi-Dataset Loader)                          |
|  - src/data/preprocessor.py (Matrix Sparsity & Index Mapping)                     |
+-----------------------------------------------------------------------------------+
```

## 2. Directory Design & Responsibilities

| Directory | Layer Responsibility | Key Modules |
|---|---|---|
| `src/config/` | Config Management | `settings.py` (BaseSettings for dataset paths, MLflow URI, hyperparameters) |
| `src/data/` | Data Engineering | `loader.py` (JSON streaming), `preprocessor.py` (Sparsity & Indexing) |
| `src/models/` | ML & Deep Learning | `classical_ml.py` (SVD), `deep_learning.py` (PyTorch NCF), `hybrid.py` (Ensemble) |
| `src/services/` | Business & Inference Service | `recommendation_service.py`, `explainability_service.py` |
| `src/monitoring/` | System Observability | `metrics.py` (Prometheus counters & histograms) |
| `src/api/` | REST Transport Layer | `main.py`, `routes/health.py`, `routes/recommend.py`, `routes/explain.py` |
| `src/templates/` | Frontend Assets | `index.html` (Modern HTML/JS Web Dashboard) |
