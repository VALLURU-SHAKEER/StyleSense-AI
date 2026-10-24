
import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:5000"

tests = [
    (
        "No matching department",
        "/api/recommendations?department=NoSuchDepartment",
        0,
    ),
    (
        "Limit to one recommendation",
        "/api/recommendations?department=Tops&class=Knits&minimum_rating=4&minimum_recommendation_rate=80&top_n=1",
        1,
    ),
    (
        "Limit to three recommendations",
        "/api/recommendations?top_n=3",
        3,
    ),
]

passed = 0

print("=== STEP 17.4: API EDGE-CASE TESTS ===")

for name, path, limit in tests:
    try:
        request = urllib.request.Request(BASE_URL + path)
        with urllib.request.urlopen(request, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            count = data.get("count", -1)
            recommendations = data.get("recommendations", [])

            if limit == 0:
                valid = count == 0
            else:
                valid = 0 < count <= limit

            valid = (
                valid
                and response.status == 200
                and data.get("status") == "ok"
                and len(recommendations) == count
            )

            if valid:
                passed += 1

            print(
                f'{"PASS" if valid else "FAIL"} | '
                f"{name} | HTTP {response.status} | "
                f"count={count}"
            )

    except Exception as error:
        print(f"FAIL | {name} | {error}")

print("=" * 45)
print(f"SUMMARY: {passed} of {len(tests)} tests passed")
