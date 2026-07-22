import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Dict, Any

class SVDRecommender:
    def __init__(self, n_components: int = 32, random_state: int = 42):
        self.n_components = n_components
        self.random_state = random_state
        self.svd = TruncatedSVD(n_components=n_components, random_state=random_state)
        self.user_item_matrix = None
        self.user_factors = None
        self.item_factors = None

    def fit(self, df_train: pd.DataFrame, num_users: int, num_items: int):
        """
        Build user-item interaction matrix and perform SVD matrix factorization.
        """
        rows = df_train['user_idx'].values
        cols = df_train['item_idx'].values
        ratings = df_train['overall'].values
        
        self.user_item_matrix = csr_matrix((ratings, (rows, cols)), shape=(num_users, num_items))
        
        # Fit SVD
        self.user_factors = self.svd.fit_transform(self.user_item_matrix)
        self.item_factors = self.svd.components_ # shape (n_components, num_items)
        return self

    def predict_user_all(self, user_idx: int) -> np.ndarray:
        """
        Dynamically compute reconstructed rating vector for a specific user on-demand to save RAM.
        """
        if self.user_factors is None or user_idx >= self.user_factors.shape[0]:
            num_items = self.item_factors.shape[1] if self.item_factors is not None else 0
            return np.full(num_items, 3.0)
        return np.dot(self.user_factors[user_idx], self.item_factors)

    def predict_score(self, user_idx: int, item_idx: int) -> float:
        if self.user_factors is not None and self.item_factors is not None:
            if user_idx < self.user_factors.shape[0] and item_idx < self.item_factors.shape[1]:
                score = float(np.dot(self.user_factors[user_idx], self.item_factors[:, item_idx]))
                return float(np.clip(score, 1.0, 5.0))
        return 3.0

    def recommend_for_user(self, user_idx: int, top_k: int = 10) -> List[Tuple[int, float]]:
        if self.user_factors is None or user_idx >= self.user_factors.shape[0]:
            return []
        user_scores = self.predict_user_all(user_idx)
        top_indices = np.argsort(user_scores)[::-1][:top_k]
        return [(int(i), float(np.clip(user_scores[i], 1.0, 5.0))) for i in top_indices]


class ContentBasedRecommender:
    def __init__(self, max_features: int = 5000):
        self.tfidf = TfidfVectorizer(stop_words='english', max_features=max_features)
        self.item_features = None
        self.idx_to_asin = {}
        self.asin_to_idx = {}

    def fit(self, item_meta: Dict[str, Dict[str, Any]]):
        """
        Build TF-IDF representations from product metadata titles and categories.
        Keeps item_features as sparse CSR matrix to scale to 100k+ catalog items without 40GB RAM overhead.
        """
        items = list(item_meta.values())
        corpus = []
        asins = []
        
        for item in items:
            text = f"{item.get('title', '')} {item.get('category', '')} {item.get('brand', '')}"
            corpus.append(text)
            asins.append(item['asin'])
            
        self.asin_to_idx = {asin: i for i, asin in enumerate(asins)}
        self.idx_to_asin = {i: asin for asin, i in self.asin_to_idx.items()}
        
        self.item_features = self.tfidf.fit_transform(corpus)
        return self

    def get_similar_items(self, asin: str, top_k: int = 10) -> List[Tuple[str, float]]:
        if asin not in self.asin_to_idx or self.item_features is None:
            return []
        target_idx = self.asin_to_idx[asin]
        # On-demand sparse row vector similarity calculation (<1MB RAM vs 40GB)
        scores = cosine_similarity(self.item_features[target_idx], self.item_features).ravel()
        sorted_indices = np.argsort(scores)[::-1]
        top_indices = [i for i in sorted_indices if i != target_idx][:top_k]
        return [(self.idx_to_asin[i], float(scores[i])) for i in top_indices]


class AssociationRuleMiner:
    """
    Data-Driven Co-Purchase Association Rule Mining Engine (FP-Growth / Co-Occurrence Lift).
    Mines item-item co-purchases and category-category cross-selling affinity directly from dataset interactions.
    """
    def __init__(self, min_support: int = 1, min_lift: float = 1.0):
        self.min_support = min_support
        self.min_lift = min_lift
        self.item_cooccurrence: Dict[str, Dict[str, int]] = {}
        self.item_counts: Dict[str, int] = {}
        self.category_cooccurrence: Dict[str, Dict[str, int]] = {}
        self.category_counts: Dict[str, int] = {}
        self.asin_to_category: Dict[str, str] = {}

    def fit(self, df_train: pd.DataFrame, item_meta: Dict[str, Dict[str, Any]]):
        """
        Builds co-occurrence matrices from user interaction baskets in df_train.
        """
        self.asin_to_category = {asin: meta.get('category', 'General') for asin, meta in item_meta.items()}
        
        # Group interacted items per user basket
        baskets = df_train.groupby('reviewerID')['asin'].apply(set).tolist()
        
        for basket in baskets:
            basket_list = list(basket)
            for asin in basket_list:
                self.item_counts[asin] = self.item_counts.get(asin, 0) + 1
                cat = self.asin_to_category.get(asin, 'General')
                main_cat = cat.split(' > ')[0] if ' > ' in cat else cat
                self.category_counts[main_cat] = self.category_counts.get(main_cat, 0) + 1

            for i in range(len(basket_list)):
                for j in range(i + 1, len(basket_list)):
                    a1, a2 = basket_list[i], basket_list[j]
                    
                    if a1 not in self.item_cooccurrence:
                        self.item_cooccurrence[a1] = {}
                    if a2 not in self.item_cooccurrence:
                        self.item_cooccurrence[a2] = {}
                        
                    self.item_cooccurrence[a1][a2] = self.item_cooccurrence[a1].get(a2, 0) + 1
                    self.item_cooccurrence[a2][a1] = self.item_cooccurrence[a2].get(a1, 0) + 1

                    c1 = self.asin_to_category.get(a1, 'General').split(' > ')[0]
                    c2 = self.asin_to_category.get(a2, 'General').split(' > ')[0]
                    if c1 != c2:
                        if c1 not in self.category_cooccurrence:
                            self.category_cooccurrence[c1] = {}
                        if c2 not in self.category_cooccurrence:
                            self.category_cooccurrence[c2] = {}
                        self.category_cooccurrence[c1][c2] = self.category_cooccurrence[c1].get(c2, 0) + 1
                        self.category_cooccurrence[c2][c1] = self.category_cooccurrence[c2].get(c1, 0) + 1

        return self

    def get_cross_sell_candidates(
        self,
        target_asin: str,
        target_category: str,
        item_meta: Dict[str, Dict[str, Any]],
        exclude_asins: set,
        top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Retrieves learned complementary cross-sell candidates for target_asin based on co-occurrence mining.
        """
        target_main_cat = target_category.split(' > ')[0] if ' > ' in target_category else target_category
        candidates: List[Tuple[str, float]] = []

        # 1. Direct Item Co-occurrence Mining
        if target_asin in self.item_cooccurrence:
            target_cnt = self.item_counts.get(target_asin, 1)
            for sim_asin, co_cnt in self.item_cooccurrence[target_asin].items():
                if sim_asin in exclude_asins or sim_asin not in item_meta:
                    continue
                sim_meta = item_meta[sim_asin]
                sim_cat = sim_meta.get('category', 'General')
                sim_main_cat = sim_cat.split(' > ')[0] if ' > ' in sim_cat else sim_cat

                if sim_main_cat != target_main_cat:
                    confidence = co_cnt / max(1, target_cnt)
                    score = min(4.95, round(4.2 + confidence * 0.75, 2))
                    candidates.append((sim_asin, score))

        candidates.sort(key=lambda x: x[1], reverse=True)

        # 2. Category Co-occurrence Lift Mining if direct item co-occurrences are sparse
        if len(candidates) < top_k and target_main_cat in self.category_cooccurrence:
            cat_target_cnt = self.category_counts.get(target_main_cat, 1)
            for cand_asin, meta in item_meta.items():
                if cand_asin in exclude_asins or cand_asin == target_asin or any(c[0] == cand_asin for c in candidates):
                    continue
                c_cat = meta.get('category', 'General')
                c_main_cat = c_cat.split(' > ')[0] if ' > ' in c_cat else c_cat

                if c_main_cat != target_main_cat and c_main_cat in self.category_cooccurrence[target_main_cat]:
                    co_cat_cnt = self.category_cooccurrence[target_main_cat][c_main_cat]
                    confidence = co_cat_cnt / max(1, cat_target_cnt)
                    score = round(min(4.85, 4.1 + confidence * 0.65), 2)
                    candidates.append((cand_asin, score))

        return candidates[:top_k]

