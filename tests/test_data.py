import pandas as pd
import pytest
from src.data.preprocessor import DataPreprocessor

def test_preprocessor_fit_transform():
    reviews_data = [
        {'reviewerID': 'U1', 'asin': 'P1', 'overall': 5.0, 'unixReviewTime': 100},
        {'reviewerID': 'U1', 'asin': 'P2', 'overall': 4.0, 'unixReviewTime': 101},
        {'reviewerID': 'U2', 'asin': 'P1', 'overall': 3.0, 'unixReviewTime': 102},
        {'reviewerID': 'U2', 'asin': 'P2', 'overall': 5.0, 'unixReviewTime': 103},
    ]
    meta_data = [
        {'asin': 'P1', 'title': 'Phone Case 1', 'price': 10.0, 'category': 'Cases'},
        {'asin': 'P2', 'title': 'Charger 2', 'price': 15.0, 'category': 'Chargers'}
    ]
    df_reviews = pd.DataFrame(reviews_data)
    df_meta = pd.DataFrame(meta_data)
    
    prep = DataPreprocessor(min_user_ratings=1, min_item_ratings=1)
    train_df, test_df = prep.fit_transform(df_reviews, df_meta, test_size=0.25)
    
    assert prep.num_users == 2
    assert prep.num_items == 2
    assert 'user_idx' in train_df.columns
    assert 'item_idx' in train_df.columns
    assert len(train_df) + len(test_df) == 4
    assert len(prep.popular_items) == 2

def test_parse_price():
    from src.data.loader import _parse_price
    assert _parse_price("$19.99") == 19.99
    assert _parse_price("19.99") == 19.99
    assert _parse_price(15.5) == 15.5
    assert _parse_price(None) == 0.0
    assert _parse_price("invalid") == 0.0
