"""Quick end-to-end test for all three candidate API endpoints."""
import json
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8000"

def req(method, path, body=None):
    data = json.dumps(body).encode() if body else None
    r = urllib.request.Request(
        BASE + path, data=data, method=method,
        headers={"Content-Type": "application/json"} if data else {}
    )
    try:
        resp = urllib.request.urlopen(r)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

# 1. POST /candidates
status, body = req("POST", "/candidates", {
    "name": "Jane Doe", "email": "jane@example.com",
    "skill": "Python", "status": "applied"
})
assert status == 201, f"Expected 201, got {status}: {body}"
cid = body["id"]
print(f"[PASS] POST /candidates  → 201  id={cid}")

# 2. Duplicate email → 409
status, body = req("POST", "/candidates", {
    "name": "Jane D", "email": "jane@example.com",
    "skill": "Go", "status": "applied"
})
assert status == 409, f"Expected 409, got {status}: {body}"
print(f"[PASS] Duplicate email   → 409")

# 3. GET /candidates
status, body = req("GET", "/candidates")
assert status == 200 and body["total"] >= 1
print(f"[PASS] GET /candidates   → 200  total={body['total']}")

# 4. GET /candidates?status=applied
status, body = req("GET", "/candidates?status=applied")
assert status == 200 and all(c["status"] == "applied" for c in body["candidates"])
print(f"[PASS] GET ?status=applied → 200  total={body['total']}")

# 5. PUT /candidates/{id}/status
status, body = req("PUT", f"/candidates/{cid}/status", {"status": "interview"})
assert status == 200 and body["status"] == "interview"
print(f"[PASS] PUT /{cid}/status → 200  status={body['status']}")

# 6. PUT with unknown id → 404
status, body = req("PUT", "/candidates/00000000-0000-0000-0000-000000000000/status", {"status": "selected"})
assert status == 404
print(f"[PASS] PUT unknown id   → 404")

# 7. Invalid status → 422
status, body = req("POST", "/candidates", {
    "name": "X", "email": "x@x.com", "skill": "JS", "status": "unknown"
})
assert status == 422
print(f"[PASS] Invalid status   → 422")

print("\nAll tests passed!")
