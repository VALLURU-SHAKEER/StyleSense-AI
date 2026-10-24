
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

import app

client = app.app.test_client()
tests_passed = 0
tests_failed = 0


def check(name, response, expected_status=200):
    global tests_passed, tests_failed

    if response.status_code == expected_status:
        print(f"PASS: {name} (HTTP {response.status_code})")
        tests_passed += 1
    else:
        print(
            f"FAIL: {name} "
            f"(expected HTTP {expected_status}, got {response.status_code})"
        )
        tests_failed += 1


check("Homepage", client.get("/"))
check("CSS resource", client.get("/style.css"))
check("JavaScript resource", client.get("/app.js"))

health = client.get("/api/health")
check("Health endpoint", health)

if health.is_json:
    print("Health response:", health.get_json())
    if health.get_json().get("status") == "ok":
        print("PASS: Health status is OK")
        tests_passed += 1
    else:
        print("FAIL: Health status is not OK")
        tests_failed += 1
else:
    print("FAIL: Health endpoint did not return JSON")
    tests_failed += 1

recommendations = client.get("/api/recommendations")
check("Default recommendations endpoint", recommendations)

filtered = client.get(
    "/api/recommendations?department=Tops&class=Knits&top_n=5"
)
check("Filtered Tops/Knits recommendations", filtered)

print(f"\nRESULT: {tests_passed} passed, {tests_failed} failed.")

if tests_failed:
    raise SystemExit(1)

print("PASS: Clean-environment Flask integration test completed.")
