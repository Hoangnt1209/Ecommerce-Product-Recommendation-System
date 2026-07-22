import os
from pydantic_settings import BaseSettings
from typing import List, Union, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Amazon E-Commerce Recommendation System"
    VERSION: str = "1.0.0"
    API_PREFIX: str = ""
    
    # Dataset Paths
    REVIEWS_PATHS: List[str] = [
        "dataset/Cell_Phones_and_Accessories_5.json",
        "dataset/Electronics_5.json"
    ]
    META_PATHS: List[str] = [
        "dataset/meta_Cell_Phones_and_Accessories.json",
        "dataset/meta_Electronics.json"
    ]
    
    # Training Parameters
    # Demo-scale training size. This keeps the default training run bounded while
    # retaining enough co-purchase data for cross-sell recommendations.
    SAMPLE_LIMIT: Optional[int] = 300_000
    MIN_USER_RATINGS: int = 2
    MIN_ITEM_RATINGS: int = 2
    SVD_COMPONENTS: int = 32
    EMBEDDING_DIM: int = 32
    EPOCHS: int = 15
    BATCH_SIZE: int = 256
    LEARNING_RATE: float = 0.001
    
    # Model Artifact Checkpoints
    CHECKPOINT_DIR: str = "checkpoints"
    RECOMMENDATION_CACHE_DIR: str = "checkpoints/recommendation_cache"
    
    # MLflow Settings
    MLFLOW_EXPERIMENT_NAME: str = "Amazon_Product_Recommendation_DDM501"
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")

settings = Settings()
