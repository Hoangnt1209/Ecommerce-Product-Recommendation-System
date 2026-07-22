import os
import json
import ast
import re
import pandas as pd
from typing import Optional, Tuple, Union, List, Any

def _parse_price(price_val: Any) -> float:
    if price_val is None:
        return 0.0
    if isinstance(price_val, (int, float)):
        return float(price_val)
    if isinstance(price_val, str):
        cleaned = re.sub(r'[^\d.]', '', price_val)
        try:
            return float(cleaned) if cleaned else 0.0
        except ValueError:
            return 0.0
    return 0.0

def load_raw_reviews(reviews_paths: Union[str, List[str]], limit: Optional[int] = None) -> pd.DataFrame:
    """
    Load raw Amazon product reviews JSON file(s).
    Can accept a single path string or a list of paths.
    Splits the limit evenly across files if multiple files are provided.
    """
    if isinstance(reviews_paths, str):
        reviews_paths = [reviews_paths]
        
    records = []
    per_file_limit = (limit // len(reviews_paths)) if limit and len(reviews_paths) > 0 else None
    
    for path in reviews_paths:
        if not path or not os.path.exists(path):
            continue
        file_loaded = 0
        with open(path, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f):
                if per_file_limit and file_loaded >= per_file_limit:
                    break
                try:
                    data = json.loads(line.strip())
                    records.append({
                        'reviewerID': data.get('reviewerID'),
                        'asin': data.get('asin'),
                        'overall': float(data.get('overall', 0.0)),
                        'unixReviewTime': int(data.get('unixReviewTime', 0)),
                        'summary': data.get('summary', ''),
                        'reviewText': data.get('reviewText', '')
                    })
                    file_loaded += 1
                except Exception:
                    continue
                    
    return pd.DataFrame(records)

def load_raw_meta(meta_paths: Union[str, List[str]], limit: Optional[int] = None) -> pd.DataFrame:
    """
    Load Amazon product metadata JSON file(s).
    Can accept a single path string or a list of paths (e.g. ['dataset/meta_Cell_Phones_and_Accessories.json', 'dataset/meta_Electronics.json']).
    """
    if isinstance(meta_paths, str):
        meta_paths = [meta_paths]
        
    records = []
    total_loaded = 0
    
    for path in meta_paths:
        if not path or not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f):
                if limit and total_loaded >= limit:
                    break
                line_str = line.strip()
                if not line_str:
                    continue
                data = None
                try:
                    data = json.loads(line_str)
                except Exception:
                    try:
                        data = ast.literal_eval(line_str)
                    except Exception:
                        continue
                
                if data and isinstance(data, dict):
                    categories = data.get('categories', [[]])
                    cat_flat = categories[0] if categories and isinstance(categories[0], list) else []
                    cat_str = ' > '.join(cat_flat) if cat_flat else 'General'
                    
                    title = data.get('title', '').strip()
                    if not title:
                        title = f"Product {data.get('asin')}"
                        
                    records.append({
                        'asin': data.get('asin'),
                        'title': title,
                        'price': _parse_price(data.get('price')),
                        'category': cat_str,
                        'imUrl': data.get('imUrl', 'https://via.placeholder.com/150'),
                        'brand': data.get('brand', 'Generic')
                    })
                    total_loaded += 1
                if limit and total_loaded >= limit:
                    break
                    
    return pd.DataFrame(records).drop_duplicates(subset=['asin'])

def load_processed_data(
    reviews_paths: Union[str, List[str]],
    meta_paths: Union[str, List[str]],
    sample_limit: Optional[int] = 100000
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convenience function to load both reviews and metadata (supports single file or list of files).
    Metadata is loaded completely without line limit so all items have proper titles and categories.
    """
    df_reviews = load_raw_reviews(reviews_paths, limit=sample_limit)
    df_meta = load_raw_meta(meta_paths, limit=None)
    return df_reviews, df_meta
