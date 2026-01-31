from fastapi import FastAPI, HTTPException
import json
from pathlib import Path

from scoring import total_score

app = FastAPI(title="Culture Circle Outfit Recommender")

# ---------------------------
# LOAD PRODUCTS
# ---------------------------

DATA_PATH = Path("products.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

CATEGORY_COMPATIBILITY = {
    "top": {"bottom", "footwear", "accessory"},
    "bottom": {"tops", "footwear", "accessory"},
    "footwear": {"tops", "bottom", "accessory"},
    "accessory": {"tops", "bottom", "footwear"} 
}


# ---------------------------
# HELPERS
# ---------------------------

def get_product(product_id: str):
    for product in PRODUCTS:
        if str(product["id"]) == str(product_id):
            return product
    return None


# ---------------------------
# ROUTES
# ---------------------------

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Culture Circle API running"}


@app.get("/products")
def list_products(limit: int = 20):
    return PRODUCTS[:limit]


# main.py (Update the recommend endpoint)

@app.get("/recommend/{product_id}")
def recommend_outfit(product_id: str):
    base_product = get_product(product_id)
    if not base_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # The assessment requires these 4 categories specifically
    slots = ["top", "bottom", "footwear", "accessory"]
    outfit = {}
    
    # Place the base product in its slot
    base_cat = base_product["category"]
    outfit[base_cat] = base_product

    # Fill remaining slots with the best matching product for each
    for slot in slots:
        if slot not in outfit:
            # Filter PRODUCTS for the slot, then find the highest score
            candidates = [p for p in PRODUCTS if p["category"] == slot]
            if candidates:
                best_match = max(candidates, key=lambda p: total_score(base_product, p))
                outfit[slot] = best_match

    # Calculate overall match_score (0-1) as required by assessment
    relevant_scores = [total_score(base_product, item) for k, item in outfit.items() if item["id"] != product_id]
    overall_score = sum(relevant_scores) / len(relevant_scores) if relevant_scores else 1.0

    return {
        "base_product": base_product,
        "complete_outfit": outfit, # Returns 4 distinct items
        "match_score": round(overall_score, 2)
    }

print(f"Loaded {len(PRODUCTS)} products")