import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from typing import List, Tuple, Optional

class InteractionDataset(Dataset):
    def __init__(self, user_indices: np.ndarray, item_indices: np.ndarray, ratings: np.ndarray):
        self.user_indices = torch.tensor(user_indices, dtype=torch.long)
        self.item_indices = torch.tensor(item_indices, dtype=torch.long)
        self.ratings = torch.tensor(ratings, dtype=torch.float32)

    def __len__(self):
        return len(self.ratings)

    def __getitem__(self, idx):
        return self.user_indices[idx], self.item_indices[idx], self.ratings[idx]


class NeuralCollaborativeFiltering(nn.Module):
    """
    Neural Collaborative Filtering (NCF) Deep Learning Recommender Model.
    Learns dense embeddings for users and items and combines them via MLP layers.
    """
    def __init__(self, num_users: int, num_items: int, embedding_dim: int = 32, hidden_dims: List[int] = [64, 32, 16], dropout: float = 0.2):
        super(NeuralCollaborativeFiltering, self).__init__()
        
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.item_embedding = nn.Embedding(num_items, embedding_dim)
        
        # GMF (Generalized Matrix Factorization) element-wise multiplication path
        self.gmf_fc = nn.Linear(embedding_dim, 16)
        
        # MLP path
        mlp_layers = []
        input_dim = embedding_dim * 2
        for h_dim in hidden_dims:
            mlp_layers.append(nn.Linear(input_dim, h_dim))
            mlp_layers.append(nn.ReLU())
            mlp_layers.append(nn.Dropout(p=dropout))
            input_dim = h_dim
        self.mlp = nn.Sequential(*mlp_layers)
        
        # Final output layer predicting rating score (1 to 5)
        self.output_layer = nn.Linear(hidden_dims[-1] + 16, 1)
        self._init_weights()

    def _init_weights(self):
        nn.init.normal_(self.user_embedding.weight, std=0.01)
        nn.init.normal_(self.item_embedding.weight, std=0.01)
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    def forward(self, user_idx: torch.Tensor, item_idx: torch.Tensor) -> torch.Tensor:
        u_emb = self.user_embedding(user_idx)
        i_emb = self.item_embedding(item_idx)
        
        # GMF vector
        gmf_vec = self.gmf_fc(u_emb * i_emb)
        
        # MLP vector
        cat_vec = torch.cat([u_emb, i_emb], dim=-1)
        mlp_vec = self.mlp(cat_vec)
        
        # Fusion
        fusion = torch.cat([gmf_vec, mlp_vec], dim=-1)
        logits = self.output_layer(fusion)
        return logits.squeeze(-1)


class NCFTrainer:
    def __init__(self, model: NeuralCollaborativeFiltering, lr: float = 0.001, device: Optional[str] = None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model.to(self.device)
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr, weight_decay=1e-5)

    def train_epoch(self, dataloader: DataLoader) -> float:
        self.model.train()
        total_loss = 0.0
        for user_idx, item_idx, ratings in dataloader:
            user_idx = user_idx.to(self.device)
            item_idx = item_idx.to(self.device)
            ratings = ratings.to(self.device)
            
            self.optimizer.zero_grad()
            preds = self.model(user_idx, item_idx)
            loss = self.criterion(preds, ratings)
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item() * len(ratings)
        return total_loss / len(dataloader.dataset)

    def evaluate(self, dataloader: DataLoader) -> Tuple[float, float]:
        self.model.eval()
        total_loss = 0.0
        preds_all = []
        targets_all = []
        with torch.no_grad():
            for user_idx, item_idx, ratings in dataloader:
                user_idx = user_idx.to(self.device)
                item_idx = item_idx.to(self.device)
                ratings = ratings.to(self.device)
                
                preds = self.model(user_idx, item_idx)
                loss = self.criterion(preds, ratings)
                
                total_loss += loss.item() * len(ratings)
                preds_all.extend(preds.cpu().numpy())
                targets_all.extend(ratings.cpu().numpy())
                
        rmse = np.sqrt(np.mean((np.array(preds_all) - np.array(targets_all)) ** 2))
        mae = np.mean(np.abs(np.array(preds_all) - np.array(targets_all)))
        return float(rmse), float(mae)

    def predict(self, user_idx: int, num_items: int) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            u_tensor = torch.tensor([user_idx] * num_items, dtype=torch.long, device=self.device)
            i_tensor = torch.arange(num_items, dtype=torch.long, device=self.device)
            preds = self.model(u_tensor, i_tensor).cpu().numpy()
            return np.clip(preds, 1.0, 5.0)
