
import json
import urllib.request

URL = (
    "http://127.0.0.1:5000/api/recommendations"
    "?department=Tops&class=Knits&minimum_rating=4"
    "&minimum_recommendation_rate=80"
    "&minimum_reviews=1&top_n=5"
)

print("=== STEP 17.5: RECOMMENDATION QUALITY TESTS ===")

with urllib.request.urlopen(URL, timeout=10) as response:
    data = json.loads(response.read().decode("utf-8"))

products = data.get("recommendations", [])
scores = [p.get("Final_Robust_Score") for p in products]

tests = [
    (
        "API returns successful response",
        data.get("status") == "ok",
    ),
    (
        "At most five products returned",
        len(products) <= 5,
    ),
    (
        "Every product has required fields",
        all(
            all(
                key in p
                for key in [
                    "Clothing ID",
                    "Department_Name",
                    "Class_Name",
                    "Average_Rating",
                    "Recommendation_Rate",
                    "Final_Robust_Score",
                ]
            )
            for p in products
        ),
    ),
    (
        "All products match selected categories",
        all(
            p.get("Department_Name") == "Tops"
            and p.get("Class_Name") == "Knits"
            for p in products
        ),
    ),
    (
        "All products meet rating and recommendation filters",
        all(
            p.get("Average_Rating", 0) >= 4
            and p.get("Recommendation_Rate", 0) >= 80
            and p.get("Review_Count", 0) >= 1
            for p in products
        ),
    ),
    (
        "Scores are in descending order",
        scores == sorted(scores, reverse=True),
    ),
]

passed = 0

for name, valid in tests:
    print(f'{"PASS" if valid else "FAIL"} | {name}')
    passed += valid

print("-" * 45)
print(f"SUMMARY: {passed} of {len(tests)} tests passed")
print("Products checked:", len(products))
