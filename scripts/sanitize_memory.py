
import json
import os

def sanitize():
    staging_path = "memory/patterns_staging.json"
    dirty_id = "6e817ea8-ac2e-469c-982e-1491336184e9"
    duplicate_request = "Crea una esfera azul"
    
    if not os.path.exists(staging_path):
        print("Staging file not found.")
        return

    with open(staging_path, 'r', encoding='utf-8') as f:
        patterns = json.load(f)

    original_count = len(patterns)
    # Filter out:
    # 1. The specific dirty ID
    # 2. Any pattern that is a duplicate of "Crea una esfera azul" (since it is already in Verified)
    sanitized = [
        p for p in patterns 
        if p['pattern_id'] != dirty_id and p['user_request'] != duplicate_request
    ]

    with open(staging_path, 'w', encoding='utf-8') as f:
        json.dump(sanitized, f, indent=2)

    print(f"Sanitization complete. Records before: {original_count}, after: {len(sanitized)}.")

if __name__ == "__main__":
    sanitize()
