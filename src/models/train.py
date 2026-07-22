import os
import pickle
import torch
import numpy as np
import pandas as pd
import mlflow
import mlflow.pytorch
from torch.utils.data import DataLoader
from typing import Union, List, Optional

from src.data.loader import load_processed_data
from src.data.preprocessor import DataPreprocessor
from src.models.classical_ml import SVDRecommender, ContentBasedRecommender
from src.models.deep_learning import NeuralCollaborativeFiltering, InteractionDataset, NCFTrainer

from src.config.settings import settings

def train_and_evaluate(
    reviews_paths: Union[str, List[str]] = settings.REVIEWS_PATHS,
    meta_paths: Union[str, List[str]] = settings.META_PATHS,
    sample_limit: Optional[int] = settings.SAMPLE_LIMIT,
    n_components: int = 32,
    embedding_dim: int = 32,
    epochs: int = 15,
    batch_size: int = 256,
    lr: float = 0.001,
    output_dir: str = "checkpoints"
):
    print("==================================================")
    print(" Starting ML & Deep Learning Training Pipeline ")
    print("==================================================")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Load Data
    print(f"[1/5] Loading datasets from {reviews_paths}...")
    df_reviews, df_meta = load_processed_data(reviews_paths, meta_paths, sample_limit=sample_limit)
    print(f" Loaded {len(df_reviews)} reviews and {len(df_meta)} metadata products.")
    
    # 2. Preprocess
    print("[2/5] Preprocessing and indexing data...")
    prep = DataPreprocessor(min_user_ratings=2, min_item_ratings=2)
    train_df, test_df = prep.fit_transform(df_reviews, df_meta)
    print(f" Train size: {len(train_df)}, Test size: {len(test_df)}")
    print(f" Total Users: {prep.num_users}, Total Items: {prep.num_items}")
    
    # Set MLflow experiment
    mlflow.set_experiment("Amazon_Product_Recommendation_DDM501")
    
    with mlflow.start_run(run_name="Hybrid_SVD_NCF_Pipeline"):
        # Log Parameters
        mlflow.log_params({
            "sample_limit": sample_limit,
            "n_components": n_components,
            "embedding_dim": embedding_dim,
            "epochs": epochs,
            "batch_size": batch_size,
            "learning_rate": lr,
            "num_users": prep.num_users,
            "num_items": prep.num_items
        })
        
        # 3. Train Classical SVD Model
        print("[3/5] Fitting Classical SVD Matrix Factorization model...")
        svd_model = SVDRecommender(n_components=n_components)
        svd_model.fit(train_df, num_users=prep.num_users, num_items=prep.num_items)
        
        # Evaluate SVD
        svd_preds = [svd_model.predict_score(r['user_idx'], r['item_idx']) for _, r in test_df.iterrows()]
        svd_targets = test_df['overall'].values
        svd_rmse = float(np.sqrt(np.mean((np.array(svd_preds) - svd_targets) ** 2)))
        svd_mae = float(np.mean(np.abs(np.array(svd_preds) - svd_targets)))
        print(f" SVD Test RMSE: {svd_rmse:.4f} | SVD Test MAE: {svd_mae:.4f}")
        mlflow.log_metric("svd_rmse", svd_rmse)
        mlflow.log_metric("svd_mae", svd_mae)
        
        # 4. Train Deep Learning NCF Model (PyTorch)
        print(f"[4/5] Training PyTorch NCF Deep Learning model for {epochs} epochs...")
        train_ds = InteractionDataset(train_df['user_idx'].values, train_df['item_idx'].values, train_df['overall'].values)
        test_ds = InteractionDataset(test_df['user_idx'].values, test_df['item_idx'].values, test_df['overall'].values)
        
        train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)
        
        ncf_model = NeuralCollaborativeFiltering(num_users=prep.num_users, num_items=prep.num_items, embedding_dim=embedding_dim)
        ncf_trainer = NCFTrainer(ncf_model, lr=lr)
        
        for epoch in range(1, epochs + 1):
            train_loss = ncf_trainer.train_epoch(train_loader)
            ncf_rmse, ncf_mae = ncf_trainer.evaluate(test_loader)
            print(f" Epoch {epoch}/{epochs} | Loss: {train_loss:.4f} | NCF RMSE: {ncf_rmse:.4f} | NCF MAE: {ncf_mae:.4f}")
            mlflow.log_metric("ncf_train_loss", train_loss, step=epoch)
            mlflow.log_metric("ncf_rmse", ncf_rmse, step=epoch)
            mlflow.log_metric("ncf_mae", ncf_mae, step=epoch)
            
        # 5. Fit Content-Based TF-IDF Model & Association Rule Miner
        print("[5/5] Fitting Content-Based TF-IDF and Association Rule Miner models...")
        content_model = ContentBasedRecommender()
        content_model.fit(prep.item_meta)
        
        from src.models.classical_ml import AssociationRuleMiner
        assoc_miner = AssociationRuleMiner()
        assoc_miner.fit(train_df, prep.item_meta)
        
        # Save Artifacts to Checkpoint directory & MLflow
        print(" Saving trained model weights and preprocessor artifacts...")
        prep_path = os.path.join(output_dir, "preprocessor.pkl")
        svd_path = os.path.join(output_dir, "svd_model.pkl")
        content_path = os.path.join(output_dir, "content_model.pkl")
        assoc_path = os.path.join(output_dir, "assoc_model.pkl")
        ncf_weights_path = os.path.join(output_dir, "pytorch_ncf.pt")
        
        with open(prep_path, "wb") as f:
            pickle.dump(prep, f)
        with open(svd_path, "wb") as f:
            pickle.dump(svd_model, f)
        with open(content_path, "wb") as f:
            pickle.dump(content_model, f)
        with open(assoc_path, "wb") as f:
            pickle.dump(assoc_miner, f)
        torch.save(ncf_model.state_dict(), ncf_weights_path)
        
        # Log artifacts to MLflow
        mlflow.log_artifact(prep_path)
        mlflow.log_artifact(svd_path)
        mlflow.log_artifact(content_path)
        mlflow.log_artifact(assoc_path)
        mlflow.log_artifact(ncf_weights_path)
        input_example = (torch.tensor([0], dtype=torch.long), torch.tensor([0], dtype=torch.long))
        mlflow.pytorch.log_model(
            ncf_model,
            "ncf_pytorch_model",
            input_example=input_example,
            serialization_format="pickle",
        )
        
        print("==================================================")
        print(" Training Successfully Completed & Saved to MLflow ")
        print("==================================================")

if __name__ == "__main__":
    train_and_evaluate()
