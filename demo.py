"""
Simple demo: POST → GET → UPDATE candidate
Run: python demo.py   (while server is running)
"""

import json
import time
import urllib.request

BASE = "http://127.0.0.1:8000"


def call(method, path, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        BASE + path,
        data=data,
        headers={"Content-Type": "application/json"},
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def pretty(label, status, data):
    print(f"\n{'='*50}")
    print(f"  {label}  [{status}]")
    print("="*50)
    print(json.dumps(data, indent=2, default=str))


# ── 1. POST — create a candidate ─────────────────────
unique_email = f"alice_{int(time.time())}@example.com"
status, candidate = call("POST", "/candidates", {
    "name": "Alice Smith",
    "email": unique_email,
    "skill": "Python",
    "status": "applied"
})
pretty("1. CREATE CANDIDATE", status, candidate)

if status != 201:
    print("\n❌ Failed to create candidate. Is the server running?")
    print("   Start it with:  python -m uvicorn app.main:app --reload")
    exit(1)

candidate_id = candidate["id"]
print(f"\n✅ Candidate created! ID = {candidate_id}")


# ── 2. GET — fetch all candidates ────────────────────
status, result = call("GET", "/candidates")
pretty("2. GET ALL CANDIDATES", status, result)
print(f"\n✅ Total candidates in system: {result['total']}")


# ── 3. PUT — update status ───────────────────────────
status, updated = call("PUT", f"/candidates/{candidate_id}/status", {
    "status": "interview"
})
pretty("3. UPDATE STATUS → interview", status, updated)

if status == 200:
    print(f"\n✅ Status updated: {updated['status']}")
else:
    print(f"\n❌ Update failed: {updated}")

print("\n" + "="*50)
print("  ALL DONE! 🎉")
print("="*50)
