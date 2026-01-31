# rules.py
# Fashion compatibility and scoring rules

# -----------------------------------
# BRAND TIERS
# -----------------------------------

HERITAGE_LUXURY = {
    "saint laurent", "balenciaga", "gucci", "prada",
    "bottega veneta", "dior", "celine", "fear of god"
}

PREMIUM_CONTEMPORARY = {
    "culture circle", "ami", "jacquemus", "toteme", "myugen"
}

MASS_MARKET = {
    "nike", "adidas", "puma", "gymshark", "h&m", "zara"
}


def brand_tier(brand: str) -> str:
    """
    Maps a brand to its market tier.
    Used to prevent luxury items pairing with mass-market products.
    """
    brand = brand.lower()

    if brand in HERITAGE_LUXURY:
        return "luxury"

    if brand in PREMIUM_CONTEMPORARY:
        return "premium"

    return "mass"


# -----------------------------------
# COLOR PALETTE LOGIC (Quiet Luxury)
# -----------------------------------

QUIET_LUXURY_COLORS = {
    "black", "white", "cream", "beige",
    "navy", "charcoal", "grey", "gray", "brown"
}


def color_score(base_color: str, candidate_color: str) -> float:
    """
    Scores color harmony between products.
    """
    base_color = (base_color or "").lower()
    candidate_color = (candidate_color or "").lower()

    if base_color == candidate_color:
        return 1.0

    if (
        base_color in QUIET_LUXURY_COLORS
        and candidate_color in QUIET_LUXURY_COLORS
    ):
        return 0.8

    return 0.3


# -----------------------------------
# OCCASION / BRAND COMPATIBILITY
# -----------------------------------

OCCASION_COMPATIBILITY = {
    "luxury": {"luxury", "premium"},
    "premium": {"luxury", "premium", "mass"},
    "mass": {"premium", "mass"}
}


def occasion_score(base_product: dict, candidate_product: dict) -> float:
    """
    Ensures styling consistency.
    Example:
    - Luxury skirt → leather loafers ✔
    - Luxury skirt → gym trainers ✖
    """
    base_tier = brand_tier(base_product.get("brand", ""))
    candidate_tier = brand_tier(candidate_product.get("brand", ""))



    if candidate_tier in OCCASION_COMPATIBILITY.get(base_tier, set()):
        return 1.0

    return 0.2

def apply_rules(base_product, all_products):
    seen = set()
    recommendations = []

    for product in all_products:

        # skip same product
        if product["id"] == base_product["id"]:
            continue

        # ✅ your rule condition
        if product["category"] == base_product["category"]:

            pid = product.get("id") or product.get("handle")

            if pid not in seen:
                seen.add(pid)
                recommendations.append(product)

    return recommendations
