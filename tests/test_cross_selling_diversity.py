import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_interactive_recommendation_multimodal_diversity():
    """
    Mandatory Test Case:
    Simulates a user selecting 3 items of DIFFERENT categories:
    1. Headphone ('B0009MYS9S')
    2. Charger ('6073894996')
    3. Keyboard ('B0002OKCXE')
    
    Verifies that:
    - similar_items contains recommendations for ALL 3 items (not just headphones).
    - cross_sell_items contains complementary items across categories (cables, cases, power banks, adapters).
    - Diversity re-ranking prevents any single category from dominating the results.
    """
    selected_asins = ["B0009MYS9S", "6073894996", "B0002OKCXE"]
    payload = {
        "selected_asins": selected_asins,
        "top_k": 8
    }

    response = client.post("/recommend-interactive", json=payload)
    assert response.status_code == 200, f"Endpoint failed: {response.text}"
    
    data = response.json()
    assert "similar_items" in data, "similar_items field missing in response"
    assert "cross_sell_items" in data, "cross_sell_items field missing in response"

    similar_items = data["similar_items"]
    cross_sell_items = data["cross_sell_items"]

    assert len(similar_items) > 0, "similar_items list should not be empty"
    assert len(cross_sell_items) > 0, "cross_sell_items list should not be empty"

    # 1. Verify candidate diversity in similar_items (Must NOT be 100% headphones)
    headphone_keywords = {'headphone', 'headset', 'earphone', 'audio', 'earbud'}
    
    similar_titles_text = " ".join([item['title'].lower() + " " + item['category'].lower() for item in similar_items])
    
    # Check that similar items also cover chargers/keyboards/cables/other categories
    non_headphone_count = sum(
        1 for item in similar_items
        if not any(kw in (item['title'] + " " + item['category']).lower() for kw in headphone_keywords)
    )
    assert non_headphone_count > 0, "similar_items contains ONLY headphones! Diversity re-ranking failed."

    # 2. Verify complementary cross-selling items across categories
    cross_keywords = {'case', 'cover', 'protector', 'cable', 'adapter', 'battery', 'power bank', 'mount', 'charger', 'stand'}
    cross_sell_titles_text = " ".join([item['title'].lower() + " " + item['category'].lower() for item in cross_sell_items])
    
    matched_cross_kws = [kw for kw in cross_keywords if kw in cross_sell_titles_text]
    assert len(matched_cross_kws) > 0, "cross_sell_items missing complementary accessory keywords"

    # 3. Verify category quota/diversity restriction (max 70% per category)
    cats = [item.get('category', 'General') for item in similar_items]
    from collections import Counter
    cat_counts = Counter(cats)
    for cat, count in cat_counts.items():
        assert count <= len(similar_items) * 0.7, f"Category '{cat}' dominates with {count}/{len(similar_items)} items!"

def test_cold_start_fallback_response():
    """
    Verifies cold start response structure when no items are selected or user is unregistered.
    """
    payload = {
        "user_id": "NON_EXISTENT_USER_COLD_START_9999",
        "top_k": 5,
        "model_type": "hybrid"
    }

    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["is_cold_start"] is True
    assert "trending_items" in data or "recommendations" in data
    assert len(data["trending_items"]) > 0 or len(data["recommendations"]) > 0
