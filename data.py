import json
from typing import List, Dict
from pathlib import Path

# ---------------------------
# LOAD DATA ONCE
# ---------------------------

DATA_PATH = Path("products.json")

def load_products() -> List[Dict]:
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            products = json.load(file)

            # 🔥 NORMALIZE HERE
            for p in products:
                p["category"] = normalize_category(p.get("category"))

            return products
    except FileNotFoundError:
        raise Exception("products.json file not found. Please check data path.")
    except json.JSONDecodeError:
        raise Exception("Invalid JSON format in products.json")



# ---------------------------
# HELPERS
# ---------------------------

def get_all_products() -> List[Dict]:
    products = load_products()
    return products


def get_product_by_id(product_id: str) -> Dict:
    """
    Fetch product by id / handle / sku (robust lookup)
    """
    product_id = str(product_id).lower()
    products = load_products()
    for product in products:
        if (
            str(product.get("id", "")).lower() == product_id
            or str(product.get("handle", "")).lower() == product_id
            or str(product.get("sku", "")).lower() == product_id
        ):
            return product

    raise Exception(f"Product '{product_id}' not found")

def normalize_category(cat: str) -> str:
    cat = cat.lower().strip()
    mapping = {
        "tops": "top",
        "bottoms": "bottom",
        "shoes": "footwear",
        "footwear": "footwear",
        "accessories": "accessory",
        "accessory": "accessory"
    }
    return mapping.get(cat, cat)
