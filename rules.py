# rules.py

# ---------------------------
# BRAND GROUPING
# ---------------------------

HERITAGE_LUXURY = {
    "Saint Laurent", "Balenciaga", "Gucci", "Prada",
    "Bottega Veneta", "Dior", "Celine"
}

PREMIUM_CONTEMPORARY = {
    "Culture Circle", "Ami", "Jacquemus", "Toteme"
}

MASS_MARKET = {
    "Nike", "Adidas", "Puma", "Gymshark", "H&M", "Zara"
}


def brand_tier(brand: str) -> str:
    if brand in HERITAGE_LUXURY:
        return "luxury"
    if brand in PREMIUM_CONTEMPORARY:
        return "premium"
    return "mass"


# ---------------------------
# COLOR / PALETTE LOGIC
# ---------------------------

QUIET_LUXURY_COLORS = {
    "black", "white", "cream", "beige",
    "navy", "charcoal", "grey", "gray", "brown"
}


def color_score(base_color: str, candidate_color: str) -> float:
    if base_color == candidate_color:
        return 1.0

    if (
        base_color in QUIET_LUXURY_COLORS
        and candidate_color in QUIET_LUXURY_COLORS
    ):
        return 0.8

    return 0.3


# ---------------------------
# OCCASION COMPATIBILITY
# ---------------------------

OCCASION_COMPATIBILITY = {
    "luxury": {"luxury", "premium"},
    "premium": {"luxury", "premium", "mass"},
    "mass": {"premium", "mass"}
}


def occasion_score(base_product: dict, candidate_product: dict) -> float:
    base_tier = brand_tier(base_product["brand"])
    candidate_tier = brand_tier(candidate_product["brand"])

    if candidate_tier in OCCASION_COMPATIBILITY[base_tier]:
        return 1.0

    return 0.2
