
import json

from flask import Blueprint, jsonify, request
from recommendation_service import recommend_products

recommendation_bp = Blueprint("recommendations", __name__)


@recommendation_bp.get("/api/recommendations")
def get_recommendations():
    try:
        department = request.args.get("department") or None
        product_class = request.args.get("class") or None

        minimum_rating = float(
            request.args.get("minimum_rating", 4)
        )
        minimum_recommendation_rate = float(
            request.args.get("minimum_recommendation_rate", 80)
        )
        minimum_reviews = int(
            request.args.get("minimum_reviews", 1)
        )
        top_n = int(request.args.get("top_n", 5))

        products = recommend_products(
            department=department,
            product_class=product_class,
            minimum_rating=minimum_rating,
            minimum_recommendation_rate=minimum_recommendation_rate,
            minimum_reviews=minimum_reviews,
            top_n=top_n,
        )

        # Convert Pandas values into JSON-compatible Python values.
        recommendations = json.loads(
            products.to_json(orient="records")
        )

        return jsonify({
            "status": "ok",
            "count": len(recommendations),
            "filters": {
                "department": department,
                "class": product_class,
                "minimum_rating": minimum_rating,
                "minimum_recommendation_rate":
                    minimum_recommendation_rate,
                "minimum_reviews": minimum_reviews,
                "top_n": top_n,
            },
            "recommendations": recommendations,
        }), 200

    except (ValueError, TypeError) as error:
        return jsonify({
            "status": "error",
            "message": str(error),
        }), 400
