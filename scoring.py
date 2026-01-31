# scoring.py

from rules import brand_tier, color_score, occasion_score


def brand_synergy_score(base_brand: str, candidate_brand: str) -> float:
    base_tier = brand_tier(base_brand)
    candidate_tier = brand_tier(candidate_brand)

    if base_tier == candidate_tier:
        return 1.0

    if base_tier == "luxury" and candidate_tier == "premium":
        return 0.7

    if base_tier == "premium" and candidate_tier in {"luxury", "premium"}:
        return 0.8

    return 0.2


def total_score(base_product: dict, candidate_product: dict) -> float:
    brand_score = brand_synergy_score(
        base_product["brand"],
        candidate_product["brand"]
    )

    palette_score = color_score(
        base_product["color"],
        candidate_product["color"]
    )

    occasion_alignment = occasion_score(
        base_product,
        candidate_product
    )

    # Penalize accessories being over-compatible
    category_penalty = 1.0
    if base_product["category"] == "accessory":
        category_penalty = 0.85

    final_score = (
        0.45 * brand_score +
        0.35 * palette_score +
        0.20 * occasion_alignment
    ) * category_penalty

    return round(final_score, 3)

