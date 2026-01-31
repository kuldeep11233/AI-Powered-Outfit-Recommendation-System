# Importing Files
import json
Jdata = json
from typing import List, Dict
# from ty
File_Path = "products.json"


def load_products() -> List[Dict]:
    try:
        with open(File_Path, "r", encoding="utf-8") as file:
            products = json.load(file)
            return products
    except FileNotFoundError:
        raise Exception("products.json file not found. Please check data path.")
    except json.JSONDecodeError:
        raise Exception("Invalid JSON format in products.json")
def get_product_by_id(product_id: str) -> Dict:
    """
    Fetches a single product by its ID.
    """
    products = load_products()
    for product in products:
        if product["id"] == product_id:
            return product

    raise Exception(f"Product with id '{product_id}' not found")
# def root():
#     return{"Hello":"world"}