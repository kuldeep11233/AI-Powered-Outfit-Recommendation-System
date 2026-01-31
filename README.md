📌 Project Overview

This project is a rule-based fashion recommendation engine designed for Culture Circle.
It recommends complementary products based on brand positioning, color harmony, category compatibility, and occasion alignment, following luxury fashion styling principles.

The goal is not brute-force similarity, but curated, stylistically sensible pairings — closer to how a human stylist thinks.

🏗️ Architecture Overview
assessment/
│
├── main.py              # FastAPI app entry point
├── products.json        # Normalized product dataset (585 products)
├── rules.py             # Core recommendation rules & scoring logic
├── category_utils.py    # Intelligent category inference
├── scoring.py           # Modular scoring helpers
├── requirements.txt     # Dependencies
└── README.md            # Project documentation


📦 Data Processing & Normalization
**Source**
- Product data provided as CSV (exported product catalog)
**Key Challenges Solved**
- Inconsistent product_type
- Missing or incorrect categories (e.g. hoodies marked as accessories)
- Unstructured brand and color information
**Solution**
- Instead of relying on a single column, categories are inferred using multiple signals:
- product_type
- tags
- title
- description

This mirrors real-world e-commerce data pipelines.

infer_category(
    product_type + tags + title + description
)

This fix ensures:
- Hoodies → top
- Skirts → bottom
- Sneakers → footwear

🎯 **Recommendation Logic (Core Intelligence)**
1. Brand Synergy

Luxury brands pair best with:
- Heritage
- Avant-Garde
- Contemporary Premium brands

Penalized combinations:
- Luxury × Mass-Market Sportswear

  Balenciaga × Saint Laurent → High score
  Balenciaga × Gymwear → Penalized

2. Color Harmony (Quiet Luxury)
Luxury styling prefers:
- Neutrals: Black, Cream, Navy, Charcoal
- Monochromatic or low-contrast palettes
- Bright mismatches are down-ranked.

3. Category Compatibility
Ensures outfit logic:

| Base Product | Recommended      |
| ------------ | ---------------- |
| Skirt        | Top, Footwear    |
| Hoodie       | Bottom, Footwear |
| Shoe         | Bottom, Top      |

Prevents:
- Top → Top loops
- Footwear → Footwear loops

4. Occasion Alignment

A product’s use-case matters.
Example:
- Luxury silk skirt ❌ Gym trainers
- Luxury silk skirt ✅ Leather loafers / minimalist sneakers

Scoring System
Each candidate product receives a cumulative score:

| Factor         | Weight    |
| -------------- | --------- |
| Brand Synergy  | High      |
| Color Harmony  | Medium    |
| Category Match | Mandatory |
| Occasion Match | Medium    |

Only the top-scoring items are returned.

API Usage
Run the server
uvicorn main:app --reload

Endpoint
GET /recommend/{product_id}

Example
GET /recommend/FEAACKB108D2

Response

{
  "base_product": "Fear of God Hoodie",
  "recommendations": [
    {
      "title": "Minimal Leather Sneaker",
      "brand": "Common Projects",
      "score": 87
    }
  ]
}


Technologies Used
- Python
- FastAPI
- JSON-based data modeling
- Rule-based scoring engine

Design Philosophy
- Simple > Complex
- Explainable > Black box
- Fashion logic > pure cosine similarity

This system is:
- Easy to debug
- Easy to extend
- Easy to justify in interviews

Future Enhancements
- User preference weighting
- Machine learning re-ranking
- Seasonal context
- Brand affinity learning

**Key Interview Takeaway**
“I focused on data quality, explainable logic, and real fashion styling principles instead of generic similarity scores.”
