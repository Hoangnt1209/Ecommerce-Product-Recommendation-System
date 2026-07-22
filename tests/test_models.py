import torch
import pandas as pd
import numpy as np
from src.data.preprocessor import DataPreprocessor
from src.models.classical_ml import SVDRecommender, ContentBasedRecommender
from src.models.deep_learning import NeuralCollaborativeFiltering, NCFTrainer, InteractionDataset
from torch.utils.data import DataLoader

def test_svd_recommender():
    df = pd.DataFrame({
        'user_idx': [0, 0, 1, 1],
        'item_idx': [0, 1, 0, 1],
        'overall': [5.0, 4.0, 3.0, 5.0]
    })
    svd = SVDRecommender(n_components=2)
    svd.fit(df, num_users=2, num_items=2)
    
    score = svd.predict_score(0, 1)
    assert 1.0 <= score <= 5.0
    recs = svd.recommend_for_user(0, top_k=2)
    assert len(recs) == 2

def test_ncf_model_training():
    num_users, num_items = 5, 5
    model = NeuralCollaborativeFiltering(num_users=num_users, num_items=num_items, embedding_dim=8, hidden_dims=[16, 8])
    trainer = NCFTrainer(model, lr=0.01, device="cpu")
    
    ds = InteractionDataset(np.array([0, 1, 2]), np.array([0, 1, 2]), np.array([4.0, 5.0, 3.0]))
    loader = DataLoader(ds, batch_size=2)
    
    loss = trainer.train_epoch(loader)
    assert loss >= 0.0
    
    preds = trainer.predict(0, num_items)
    assert len(preds) == num_items
