import requests

base_url = "http://127.0.0.1:5000/api/categories"


# ============================================================
# 1. GET ALL CATEGORIES
# ============================================================

print("\n--- GET ALL CATEGORIES ---")

response = requests.get(base_url)

print(response.status_code)
print(response.json())

# ============================================================
# 2. GET CATEGORY BY ID
# ============================================================

print("\n--- GET CATEGORY BY ID ---")

response = requests.get(
    f"{base_url}/1"
)

print(response.status_code)
print(response.json())


# ============================================================
# 3. GET INVALID CATEGORY ID
# ============================================================

print("\n--- GET INVALID CATEGORY ID ---")

response = requests.get(
    f"{base_url}/999"
)

print(response.status_code)
print(response.json())

# ============================================================
# 4. ADD CATEGORY
# ============================================================

print("\n--- ADD CATEGORY ---")

response = requests.post(
    base_url,
    json={
        "CategoryName": "Snacks"
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 5. ADD DUPLICATE CATEGORY
# ============================================================

print("\n--- ADD DUPLICATE CATEGORY ---")

response = requests.post(
    base_url,
    json={
        "CategoryName": "Snacks"
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 6. ADD CATEGORY - MISSING NAME
# ============================================================

print("\n--- ADD CATEGORY - MISSING NAME ---")

response = requests.post(
    base_url,
    json={}
)

print(response.status_code)
print(response.json())


# ============================================================
# 7. ADD CATEGORY - EMPTY NAME
# ============================================================

print("\n--- ADD CATEGORY - EMPTY NAME ---")

response = requests.post(
    base_url,
    json={
        "CategoryName": "   "
    }
)

print(response.status_code)
print(response.json())

# ============================================================
# 8. UPDATE CATEGORY
# ============================================================

print("\n--- UPDATE CATEGORY ---")

response = requests.put(
    f"{base_url}/6",
    json={
        "CategoryName": "Packaged Snacks"
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 9. GET UPDATED CATEGORY
# ============================================================

print("\n--- GET UPDATED CATEGORY ---")

response = requests.get(
    f"{base_url}/6"
)

print(response.status_code)
print(response.json())


# ============================================================
# 10. UPDATE INVALID CATEGORY
# ============================================================

print("\n--- UPDATE INVALID CATEGORY ---")

response = requests.put(
    f"{base_url}/999",
    json={
        "CategoryName": "Test Category"
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 11. UPDATE CATEGORY - MISSING NAME
# ============================================================

print("\n--- UPDATE CATEGORY - MISSING NAME ---")

response = requests.put(
    f"{base_url}/6",
    json={}
)

print(response.status_code)
print(response.json())


# ============================================================
# 12. UPDATE CATEGORY - EMPTY NAME
# ============================================================

print("\n--- UPDATE CATEGORY - EMPTY NAME ---")

response = requests.put(
    f"{base_url}/6",
    json={
        "CategoryName": "   "
    }
)

print(response.status_code)
print(response.json())

# ============================================================
# 13. DEACTIVATE CATEGORY
# ============================================================

print("\n--- DEACTIVATE CATEGORY ---")

response = requests.delete(
    f"{base_url}/6"
)

print(response.status_code)
print(response.json())


# ============================================================
# 14. GET INACTIVE CATEGORY
# ============================================================

print("\n--- GET DEACTIVATED CATEGORY ---")

response = requests.get(
    f"{base_url}/6"
)

print(response.status_code)
print(response.json())


# ============================================================
# 15. DEACTIVATE ALREADY INACTIVE CATEGORY
# ============================================================

print("\n--- DEACTIVATE ALREADY INACTIVE CATEGORY ---")

response = requests.delete(
    f"{base_url}/6"
)

print(response.status_code)
print(response.json())


# ============================================================
# 16. DEACTIVATE INVALID CATEGORY
# ============================================================

print("\n--- DEACTIVATE INVALID CATEGORY ---")

response = requests.delete(
    f"{base_url}/999"
)

print(response.status_code)
print(response.json())