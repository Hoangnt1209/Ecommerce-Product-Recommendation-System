import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from src.models.classical_ml import SVDRecommender, ContentBasedRecommender, AssociationRuleMiner
from src.models.deep_learning import NCFTrainer
from src.data.preprocessor import DataPreprocessor

COMPLEMENTARY_MAP = {
    'screen': ['case', 'cover', 'protector', 'glass', 'charger', 'cable', 'stylus'],
    'protector': ['case', 'cover', 'glass', 'charger', 'cable', 'skin'],
    'case': ['screen', 'protector', 'glass', 'charger', 'cable', 'mount', 'stand', 'holster'],
    'cover': ['screen', 'protector', 'glass', 'charger', 'cable', 'skin'],
    'charger': ['cable', 'adapter', 'battery', 'power bank', 'case', 'car charger'],
    'headphone': ['audio', 'adapter', 'case', 'bluetooth', 'headset', 'earphone'],
    'headset': ['audio', 'adapter', 'case', 'bluetooth', 'headphone', 'earphone'],
    'battery': ['charger', 'cable', 'case', 'power bank', 'adapter'],
    'cable': ['charger', 'adapter', 'car charger', 'hub'],
    'mount': ['car charger', 'case', 'cable', 'holder']
}

class HybridRecommender:
    """
    Production Hybrid Recommendation Engine.
    Combines Classical SVD Matrix Factorization, PyTorch Neural Collaborative Filtering (NCF),
    TF-IDF Content Similarity, and Learned Data-Driven Association Rule Cross-Selling.
    """
    def __init__(
        self,
        svd_model: SVDRecommender,
        content_model: ContentBasedRecommender,
        ncf_trainer: NCFTrainer,
        preprocessor: DataPreprocessor,
        assoc_model: Optional[AssociationRuleMiner] = None,
        w_svd: float = 0.5,
        w_ncf: float = 0.5
    ):
        self.svd = svd_model
        self.ncf = ncf_trainer
        self.content = content_model
        self.prep = preprocessor
        self.assoc_model = assoc_model
        self.w_svd = w_svd
        self.w_ncf = w_ncf

    def _get_popular_recommendations(self, top_k: int = 10) -> List[Dict[str, Any]]:
        popular_asins = self.prep.popular_items[:top_k]
        items = []
        for rank, asin in enumerate(popular_asins):
            meta = self.prep.item_meta.get(asin, {})
            score = max(4.0, round(4.9 - (rank * 0.05), 2))
            items.append({
                'asin': asin,
                'title': meta.get('title', f"Product {asin}"),
                'price': meta.get('price', 0.0),
                'category': meta.get('category', 'General'),
                'imUrl': meta.get('imUrl', 'https://via.placeholder.com/150'),
                'brand': meta.get('brand', 'Generic'),
                'predicted_score': score,
                'type': 'popular',
                'explanation': f"Top #{rank+1} sản phẩm phổ biến nhất"
            })
        return items

    def balance_and_rerank_by_source(
        self,
        candidates_by_source: List[List[Dict[str, Any]]],
        top_k: int = 8
    ) -> List[Dict[str, Any]]:
        """
        Guarantees that EVERY source item (selected product) gets equal candidate quota
        in the final recommendation list, preventing any single item or category from dominating.
        """
        if not candidates_by_source:
            return []

        num_sources = len(candidates_by_source)
        quota_per_source = max(1, top_k // num_sources)
        
        result = []
        seen_asins = set()

        # Pass 1: Give each source item its fair share (quota_per_source)
        for c_list in candidates_by_source:
            added_for_source = 0
            for cand in c_list:
                if cand['asin'] not in seen_asins:
                    seen_asins.add(cand['asin'])
                    result.append(cand)
                    added_for_source += 1
                    if added_for_source >= quota_per_source:
                        break

        # Pass 2: Round-robin fill remaining slots up to top_k
        max_depth = max((len(c) for c in candidates_by_source), default=0)
        for d in range(max_depth):
            if len(result) >= top_k:
                break
            for c_list in candidates_by_source:
                if len(result) >= top_k:
                    break
                if d < len(c_list):
                    cand = c_list[d]
                    if cand['asin'] not in seen_asins:
                        seen_asins.add(cand['asin'])
                        result.append(cand)

        return result[:top_k]

    def _generate_similar_candidates(
        self,
        target_items: List[Dict[str, Any]],
        exclude_asins: set,
        top_k: int = 8
    ) -> List[Dict[str, Any]]:
        """
        Generates similar_items stream (content-based similarity / item-item CF).
        Ensures candidates are sourced equally from ALL target_items.
        """
        candidates_by_source: List[List[Dict[str, Any]]] = []
        
        for titem in target_items:
            asin = titem.get('asin', '')
            title = titem.get('title', f"Product {asin}")
            cat = titem.get('category', 'General')
            t_text = f"{title} {cat}".lower()
            
            item_candidates = []
            similar_list = []
            if self.content and asin in self.content.asin_to_idx:
                similar_list = self.content.get_similar_items(asin, top_k=60)

            if similar_list:
                for sim_asin, sim_score in similar_list:
                    if sim_asin in exclude_asins:
                        continue
                    meta = self.prep.item_meta.get(sim_asin, {})
                    scat = meta.get('category', 'General')
                    
                    norm_score = round(min(4.95, max(4.0, 4.0 + sim_score * 0.95)), 2)
                    item_candidates.append({
                        'asin': sim_asin,
                        'title': meta.get('title', f"Product {sim_asin}"),
                        'price': meta.get('price', 0.0),
                        'category': scat,
                        'imUrl': meta.get('imUrl', 'https://via.placeholder.com/150'),
                        'brand': meta.get('brand', 'Generic'),
                        'predicted_score': norm_score,
                        'type': 'similar',
                        'source_asin': asin,
                        'source_title': title,
                        'explanation': f"Sản phẩm tương tự cho '{title[:30]}...'"
                    })
            else:
                for sim_asin, meta in self.prep.item_meta.items():
                    if sim_asin in exclude_asins or sim_asin == asin:
                        continue
                    stext = f"{meta.get('title', '')} {meta.get('category', '')}".lower()
                    overlap = sum(1.0 for w in t_text.split() if len(w) > 3 and w in stext)
                    if overlap > 0:
                        item_candidates.append({
                            'asin': sim_asin,
                            'title': meta.get('title', f"Product {sim_asin}"),
                            'price': meta.get('price', 0.0),
                            'category': meta.get('category', 'General'),
                            'imUrl': meta.get('imUrl', 'https://via.placeholder.com/150'),
                            'brand': meta.get('brand', 'Generic'),
                            'predicted_score': round(min(4.9, 4.0 + overlap * 0.15), 2),
                            'type': 'similar',
                            'source_asin': asin,
                            'source_title': title,
                            'explanation': f"Sản phẩm tương tự cho '{title[:30]}...'"
                        })
            
            item_candidates.sort(key=lambda x: x['predicted_score'], reverse=True)
            candidates_by_source.append(item_candidates)

        return self.balance_and_rerank_by_source(candidates_by_source, top_k=top_k)

    def _generate_cross_sell_candidates(
        self,
        target_items: List[Dict[str, Any]],
        exclude_asins: set,
        top_k: int = 8
    ) -> List[Dict[str, Any]]:
        """
        Generates cross_sell_items stream using Learned Data-Driven Association Rules.
        Falls back to keyword complementarity heuristics if needed.
        """
        candidates_by_source: List[List[Dict[str, Any]]] = []
        
        for titem in target_items:
            asin = titem.get('asin', '')
            title = titem.get('title', f"Product {asin}")
            cat = titem.get('category', 'General')
            t_text = f"{title} {cat}".lower()
            
            item_candidates = []
            seen_cand_asins = set()

            # 1. Use Learned Data-Driven Association Rule Miner if available
            if self.assoc_model:
                assoc_recs = self.assoc_model.get_cross_sell_candidates(
                    target_asin=asin,
                    target_category=cat,
                    item_meta=self.prep.item_meta,
                    exclude_asins=exclude_asins,
                    top_k=10
                )
                for cand_asin, score in assoc_recs:
                    meta = self.prep.item_meta.get(cand_asin, {})
                    seen_cand_asins.add(cand_asin)
                    item_candidates.append({
                        'asin': cand_asin,
                        'title': meta.get('title', f"Product {cand_asin}"),
                        'price': meta.get('price', 0.0),
                        'category': meta.get('category', 'General'),
                        'imUrl': meta.get('imUrl', 'https://via.placeholder.com/150'),
                        'brand': meta.get('brand', 'Generic'),
                        'predicted_score': score,
                        'type': 'cross_sell',
                        'source_asin': asin,
                        'source_title': title,
                        'explanation': f"Mô hình Association Rules phát hiện mua kèm với '{title[:25]}...'"
                    })

            # 2. Keyword Complementarity Fallback
            comp_keywords = set()
            for kw, c_list in COMPLEMENTARY_MAP.items():
                if kw in t_text:
                    comp_keywords.update(c_list)
            if not comp_keywords:
                comp_keywords = {'case', 'cover', 'charger', 'cable', 'adapter', 'protector', 'battery', 'mount', 'stand'}

            for sim_asin, meta in self.prep.item_meta.items():
                if sim_asin in exclude_asins or sim_asin == asin or sim_asin in seen_cand_asins:
                    continue
                stext = f"{meta.get('title', '')} {meta.get('category', '')}".lower()
                scat = meta.get('category', 'General')
                
                matched_kws = [ck for ck in comp_keywords if ck in stext]
                if matched_kws:
                    match_score = round(min(4.95, 4.1 + 0.25 * len(matched_kws)), 2)
                    item_candidates.append({
                        'asin': sim_asin,
                        'title': meta.get('title', f"Product {sim_asin}"),
                        'price': meta.get('price', 0.0),
                        'category': scat,
                        'imUrl': meta.get('imUrl', 'https://via.placeholder.com/150'),
                        'brand': meta.get('brand', 'Generic'),
                        'predicted_score': match_score,
                        'type': 'cross_sell',
                        'source_asin': asin,
                        'source_title': title,
                        'explanation': f"Phụ kiện/Sản phẩm mua kèm gợi ý cho '{title[:25]}...'"
                    })

            item_candidates.sort(key=lambda x: x['predicted_score'], reverse=True)
            candidates_by_source.append(item_candidates)

        return self.balance_and_rerank_by_source(candidates_by_source, top_k=top_k)

    def recommend(
        self,
        user_id: str,
        top_k: int = 10,
        model_type: str = "hybrid"
    ) -> Dict[str, Any]:
        """
        Generate Top-K recommendations for a registered user or cold-start user.
        Supports dual streams: similar_items & cross_sell_items.
        """
        # Registered User with history
        user_hist = self.prep.user_history.get(user_id, [])

        # Cold Start User fallback if no interaction history exists
        if not user_hist:
            trending = self._get_popular_recommendations(top_k=top_k)
            return {
                'user_id': user_id,
                'is_cold_start': True,
                'model_used': 'Popularity Fallback (Cold Start)',
                'trending_items': trending,
                'similar_items': [],
                'cross_sell_items': [],
                'recommendations': trending
            }

        purchased_asins = {h['asin'] for h in user_hist if 'asin' in h}
        purchased_main_cats = {h.get('category', 'General').split(' > ')[0] for h in user_hist if h.get('category')}
        
        target_items = []
        for h in user_hist:
            asin = h.get('asin')
            meta = self.prep.item_meta.get(asin, {}) if asin else {}
            target_items.append({
                'asin': asin,
                'title': meta.get('title', h.get('title', f"Product {asin}")),
                'category': meta.get('category', h.get('category', 'General'))
            })

        half_k = max(4, top_k // 2)

        if model_type == "svd" and self.svd:
            user_idx = self.prep.user_to_idx.get(user_id)
            raw_recs = self.svd.recommend_for_user(user_idx, top_k=top_k * 2) if user_idx is not None else []
            svd_items = []
            for item_idx, score in raw_recs:
                asin = self.prep.idx_to_item.get(item_idx)
                if asin and asin not in purchased_asins:
                    meta = self.prep.item_meta.get(asin, {})
                    svd_items.append({
                        'asin': asin,
                        'title': meta.get('title', f"Product {asin}"),
                        'price': meta.get('price', 0.0),
                        'category': meta.get('category', 'General'),
                        'imUrl': meta.get('imUrl', 'https://via.placeholder.com/150'),
                        'brand': meta.get('brand', 'Generic'),
                        'predicted_score': round(float(score), 2)
                    })
            
            similar_items = [it for it in svd_items if it.get('category', 'General').split(' > ')[0] in purchased_main_cats]
            cross_sell_items = [it for it in svd_items if it.get('category', 'General').split(' > ')[0] not in purchased_main_cats]
            
            for it in similar_items: it['type'] = 'similar'
            for it in cross_sell_items: it['type'] = 'cross_sell'

            if len(similar_items) < half_k:
                similar_items += self._generate_similar_candidates(target_items, exclude_asins=purchased_asins, top_k=half_k - len(similar_items))
            if len(cross_sell_items) < half_k:
                cross_sell_items += self._generate_cross_sell_candidates(target_items, exclude_asins=purchased_asins, top_k=half_k - len(cross_sell_items))
            
            source_label = "Classical SVD Matrix Factorization Engine"

        elif model_type == "ncf" and self.ncf:
            user_idx = self.prep.user_to_idx.get(user_id)
            if user_idx is not None:
                ncf_scores = self.ncf.predict(user_idx, self.prep.num_items)
                top_indices = np.argsort(ncf_scores)[::-1]
                ncf_items = []
                for item_idx in top_indices:
                    asin = self.prep.idx_to_item.get(int(item_idx))
                    if asin and asin not in purchased_asins:
                        meta = self.prep.item_meta.get(asin, {})
                        score = float(ncf_scores[item_idx])
                        ncf_items.append({
                            'asin': asin,
                            'title': meta.get('title', f"Product {asin}"),
                            'price': meta.get('price', 0.0),
                            'category': meta.get('category', 'General'),
                            'imUrl': meta.get('imUrl', 'https://via.placeholder.com/150'),
                            'brand': meta.get('brand', 'Generic'),
                            'predicted_score': round(score, 2)
                        })
                        if len(ncf_items) >= top_k * 2:
                            break
                similar_items = [it for it in ncf_items if it.get('category', 'General').split(' > ')[0] in purchased_main_cats]
                cross_sell_items = [it for it in ncf_items if it.get('category', 'General').split(' > ')[0] not in purchased_main_cats]
            else:
                similar_items, cross_sell_items = [], []

            for it in similar_items: it['type'] = 'similar'
            for it in cross_sell_items: it['type'] = 'cross_sell'

            if len(similar_items) < half_k:
                similar_items += self._generate_similar_candidates(target_items, exclude_asins=purchased_asins, top_k=half_k - len(similar_items))
            if len(cross_sell_items) < half_k:
                cross_sell_items += self._generate_cross_sell_candidates(target_items, exclude_asins=purchased_asins, top_k=half_k - len(cross_sell_items))

            source_label = "PyTorch Neural Collaborative Filtering (NCF) Deep Learning Engine"

        elif model_type == "content":
            similar_items = self._generate_similar_candidates(target_items, exclude_asins=purchased_asins, top_k=half_k * 2)
            cross_sell_items = []
            source_label = "TF-IDF Content Similarity Engine"

        else: # hybrid
            # True Hybrid Fusion: Fusion of SVD + PyTorch NCF scores for candidate items
            user_idx = self.prep.user_to_idx.get(user_id)
            if user_idx is not None and self.svd and self.ncf:
                svd_scores = self.svd.predict_user_all(user_idx)
                ncf_scores = self.ncf.predict(user_idx, self.prep.num_items)
                
                # Hybrid score blending (0.5 * SVD + 0.5 * NCF)
                fused_scores = (self.w_svd * svd_scores) + (self.w_ncf * ncf_scores)
                top_indices = np.argsort(fused_scores)[::-1]
                
                fused_items = []
                for item_idx in top_indices:
                    asin = self.prep.idx_to_item.get(int(item_idx))
                    if asin and asin not in purchased_asins:
                        meta = self.prep.item_meta.get(asin, {})
                        score = float(fused_scores[item_idx])
                        fused_items.append({
                            'asin': asin,
                            'title': meta.get('title', f"Product {asin}"),
                            'price': meta.get('price', 0.0),
                            'category': meta.get('category', 'General'),
                            'imUrl': meta.get('imUrl', 'https://via.placeholder.com/150'),
                            'brand': meta.get('brand', 'Generic'),
                            'predicted_score': round(float(np.clip(score, 1.0, 5.0)), 2)
                        })
                        if len(fused_items) >= top_k * 2:
                            break
                similar_items = [it for it in fused_items if it.get('category', 'General').split(' > ')[0] in purchased_main_cats]
                cross_sell_items = [it for it in fused_items if it.get('category', 'General').split(' > ')[0] not in purchased_main_cats]
            else:
                similar_items = self._generate_similar_candidates(target_items, exclude_asins=purchased_asins, top_k=half_k)
                cross_sell_items = self._generate_cross_sell_candidates(target_items, exclude_asins=purchased_asins, top_k=half_k)

            if len(similar_items) < half_k:
                similar_items += self._generate_similar_candidates(target_items, exclude_asins=purchased_asins, top_k=half_k - len(similar_items))
            if len(cross_sell_items) < half_k:
                cross_sell_items += self._generate_cross_sell_candidates(target_items, exclude_asins=purchased_asins, top_k=half_k - len(cross_sell_items))

            source_label = "🌟 Dual-Stream Hybrid Ensemble Engine (SVD + PyTorch NCF + Association Rules)"

        for it in similar_items:
            it['type'] = 'similar'
        for it in cross_sell_items:
            it['type'] = 'cross_sell'

        combined_recs = similar_items + cross_sell_items

        return {
            'user_id': user_id,
            'is_cold_start': False,
            'model_used': source_label,
            'trending_items': [],
            'similar_items': similar_items[:half_k],
            'cross_sell_items': cross_sell_items[:half_k],
            'recommendations': combined_recs[:top_k]
        }

    def recommend_from_selected_items(self, selected_asins: List[str], top_k: int = 10) -> Dict[str, Any]:
        """
        Generates real-time dual-stream recommendations (Similar + Cross-selling)
        for a user based on their active selection of items.
        """
        if not selected_asins:
            return self.recommend("NEW_USER_COLD_START", top_k=top_k)
            
        exclude_asins = set(selected_asins)
        target_items = []
        for asin in selected_asins:
            meta = self.prep.item_meta.get(asin, {})
            target_items.append({
                'asin': asin,
                'title': meta.get('title', f"Product {asin}"),
                'category': meta.get('category', 'General')
            })

        half_k = max(4, top_k // 2)
        similar_items = self._generate_similar_candidates(target_items, exclude_asins=exclude_asins, top_k=half_k)
        cross_sell_items = self._generate_cross_sell_candidates(target_items, exclude_asins=exclude_asins, top_k=half_k)

        combined_recs = similar_items + cross_sell_items

        return {
            'user_id': 'Interactive Cold-Start User',
            'is_cold_start': False,
            'model_used': 'Interactive Personalization (TF-IDF Similarity + Cross-Sell Engine)',
            'trending_items': [],
            'similar_items': similar_items,
            'cross_sell_items': cross_sell_items,
            'recommendations': combined_recs
        }

