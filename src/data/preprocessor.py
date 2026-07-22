import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from typing import Dict, Tuple, Any, List

class DataPreprocessor:
    def __init__(self, min_user_ratings: int = 2, min_item_ratings: int = 2):
        self.min_user_ratings = min_user_ratings
        self.min_item_ratings = min_item_ratings
        self.user_to_idx: Dict[str, int] = {}
        self.idx_to_user: Dict[int, str] = {}
        self.item_to_idx: Dict[str, int] = {}
        self.idx_to_item: Dict[int, str] = {}
        self.item_meta: Dict[str, Dict[str, Any]] = {}
        self.popular_items: list = []
        self.sparsity_stats: Dict[str, Any] = {}
        self.user_history: Dict[str, List[Dict[str, Any]]] = {}

    def compute_sparsity_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculates matrix sparsity, interaction density, and user/item activity distributions.
        """
        num_users = df['reviewerID'].nunique()
        num_items = df['asin'].nunique()
        num_interactions = len(df)
        total_possible = num_users * num_items if num_users > 0 and num_items > 0 else 1
        
        density = (num_interactions / total_possible) * 100
        sparsity = 100.0 - density
        
        user_counts = df['reviewerID'].value_counts()
        item_counts = df['asin'].value_counts()
        
        single_rating_users = (user_counts == 1).sum()
        single_rating_items = (item_counts == 1).sum()
        
        return {
            'num_users': num_users,
            'num_items': num_items,
            'num_interactions': num_interactions,
            'matrix_density_pct': round(density, 4),
            'matrix_sparsity_pct': round(sparsity, 4),
            'single_rating_users': single_rating_users,
            'single_rating_users_pct': round((single_rating_users / max(num_users, 1)) * 100, 2),
            'single_rating_items': single_rating_items,
            'single_rating_items_pct': round((single_rating_items / max(num_items, 1)) * 100, 2),
            'avg_user_activity': round(num_interactions / max(num_users, 1), 2),
            'avg_item_popularity': round(num_interactions / max(num_items, 1), 2)
        }

    def fit_transform(
        self, df_reviews: pd.DataFrame, df_meta: pd.DataFrame, test_size: float = 0.2, random_state: int = 42
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Processes raw reviews and meta DataFrames into mapped datasets with train/test split.
        """
        # Calculate raw matrix sparsity BEFORE filtering
        self.sparsity_stats = self.compute_sparsity_stats(df_reviews)
        
        # Filter sparse interactions below thresholds
        user_counts = df_reviews['reviewerID'].value_counts()
        item_counts = df_reviews['asin'].value_counts()
        
        valid_users = user_counts[user_counts >= self.min_user_ratings].index
        valid_items = item_counts[item_counts >= self.min_item_ratings].index
        
        filtered_df = df_reviews[
            df_reviews['reviewerID'].isin(valid_users) & df_reviews['asin'].isin(valid_items)
        ].copy()
        
        if len(filtered_df) == 0:
            filtered_df = df_reviews.copy()
            
        # Build User and Item Index Mappings
        unique_users = filtered_df['reviewerID'].unique()
        unique_items = filtered_df['asin'].unique()
        
        self.user_to_idx = {uid: i for i, uid in enumerate(unique_users)}
        self.idx_to_user = {i: uid for uid, i in self.user_to_idx.items()}
        
        self.item_to_idx = {asin: i for i, asin in enumerate(unique_items)}
        self.idx_to_item = {i: asin for asin, i in self.item_to_idx.items()}
        
        filtered_df['user_idx'] = filtered_df['reviewerID'].map(self.user_to_idx)
        filtered_df['item_idx'] = filtered_df['asin'].map(self.item_to_idx)
        
        # Store metadata mapping
        import html
        meta_dict = df_meta.set_index('asin').to_dict(orient='index')
        for asin, item_i in self.item_to_idx.items():
            info = meta_dict.get(asin, {})
            raw_title = html.unescape(str(info.get('title', ''))).strip()
            category = info.get('category', 'General')
            
            if not raw_title or raw_title.startswith('Product '):
                cat_name = category.split(' > ')[-1] if ' > ' in category else category
                if cat_name == 'General':
                    cat_name = 'Electronics Accessory'
                raw_title = f"{cat_name} ({asin})"
                
            im_url = str(info.get('imUrl', '')).strip()
            if 'images-amazon.com' in im_url:
                im_url = im_url.replace('http://ecx.images-amazon.com', 'https://images-na.ssl-images-amazon.com').replace('http://g-ecx.images-amazon.com', 'https://images-na.ssl-images-amazon.com').replace('http://', 'https://')
            elif not im_url or 'placeholder' in im_url:
                im_url = 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&q=75'
                
            self.item_meta[asin] = {
                'asin': asin,
                'item_idx': item_i,
                'title': raw_title,
                'price': info.get('price', 0.0),
                'category': category,
                'imUrl': im_url,
                'brand': info.get('brand', 'Generic')
            }
            
        # Calculate Bayesian Weighted Rating for items
        item_popularity = filtered_df.groupby('asin').agg(
            rating_count=('overall', 'count'),
            avg_rating=('overall', 'mean')
        ).reset_index()
        
        C = item_popularity['avg_rating'].mean()
        m = 2
        item_popularity['weighted_score'] = (
            (item_popularity['rating_count'] / (item_popularity['rating_count'] + m)) * item_popularity['avg_rating'] +
            (m / (item_popularity['rating_count'] + m)) * C
        )
        self.popular_items = item_popularity.sort_values(by='weighted_score', ascending=False)['asin'].tolist()
        
        # Populate User History mapping (past interacted items per user)
        history_map = {}
        for uid, group in filtered_df.groupby('reviewerID'):
            items_list = []
            for _, row in group.head(4).iterrows():
                asin = row['asin']
                info = self.item_meta.get(asin, {})
                items_list.append({
                    'asin': asin,
                    'title': info.get('title', f"Product {asin}"),
                    'rating': float(row['overall']),
                    'category': info.get('category', 'General')
                })
            history_map[uid] = items_list
        self.user_history = history_map
        
        # Train / Test split
        train_df, test_df = train_test_split(
            filtered_df, test_size=test_size, random_state=random_state, stratify=None
        )
        
        return train_df, test_df

    @property
    def num_users(self) -> int:
        return len(self.user_to_idx)

    @property
    def num_items(self) -> int:
        return len(self.item_to_idx)
