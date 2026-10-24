
import urllib.request

BASE_URL = "http://127.0.0.1:5000"

def fetch(path):
    with urllib.request.urlopen(BASE_URL + path, timeout=5) as response:
        return response.status, response.read().decode("utf-8", errors="replace")

print("=== STEP 17.6: FRONTEND INTEGRATION TESTS ===")

html_status, html = fetch("/")
css_status, css = fetch("/style.css")
js_status, js = fetch("/app.js")

tests = [
    ("Homepage loads successfully", html_status == 200),
    ("Stylesheet loads successfully", css_status == 200),
    ("JavaScript loads successfully", js_status == 200),
    ("Preference form exists", 'id="preference-form"' in html),
    ("Product results container exists", 'id="product-grid"' in html),
    ("Message container exists", 'id="message"' in html),
    ("JavaScript calls recommendation API", "/api/recommendations" in js),
    ("Form submit handler exists", 'addEventListener("submit"' in js),
    ("Department change handler exists", 'addEventListener("change"' in js),
    ("Success and error messages are handled", '"success"' in js and '"error"' in js),
    ("Fashion category visual styling exists", ".product-visual" in css),
]

passed = 0

for name, valid in tests:
    print(f'{"PASS" if valid else "FAIL"} | {name}')
    passed += valid

print("-" * 45)
print(f"SUMMARY: {passed} of {len(tests)} tests passed")
