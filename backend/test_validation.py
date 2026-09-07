import requests

base_url = "http://127.0.0.1:5000/api/products"
# ============================================================
# 14. ADD PRODUCT - MISSING NAME
# ============================================================

print("\n--- ADD PRODUCT - MISSING NAME ---")

response = requests.post(
    base_url,
    json={
        "Price": 50,
        "UOM": "Kg",
        "CategoryID": 1
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 15. ADD PRODUCT - INVALID PRICE
# ============================================================

print("\n--- ADD PRODUCT - INVALID PRICE ---")

response = requests.post(
    base_url,
    json={
        "Name": "Test Product",
        "Price": "abc",
        "UOM": "Kg",
        "CategoryID": 1
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 16. ADD PRODUCT - NEGATIVE PRICE
# ============================================================

print("\n--- ADD PRODUCT - NEGATIVE PRICE ---")

response = requests.post(
    base_url,
    json={
        "Name": "Test Product",
        "Price": -10,
        "UOM": "Kg",
        "CategoryID": 1
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 17. ADD PRODUCT - INVALID CATEGORY
# ============================================================

print("\n--- ADD PRODUCT - INVALID CATEGORY ---")

response = requests.post(
    base_url,
    json={
        "Name": "Test Product",
        "Price": 50,
        "UOM": "Kg",
        "CategoryID": 999
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 18. UPDATE PRODUCT - MISSING NAME
# ============================================================

print("\n--- UPDATE PRODUCT - MISSING NAME ---")

response = requests.put(
    f"{base_url}/1",
    json={
        "Price": 90,
        "UOM": "Kg",
        "CategoryID": 1
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 19. UPDATE PRODUCT - INVALID PRICE
# ============================================================

print("\n--- UPDATE PRODUCT - INVALID PRICE ---")

response = requests.put(
    f"{base_url}/1",
    json={
        "Name": "Premium Basmati Rice",
        "Price": "abc",
        "UOM": "Kg",
        "CategoryID": 1
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 20. UPDATE PRODUCT - INVALID CATEGORY
# ============================================================

print("\n--- UPDATE PRODUCT - INVALID CATEGORY ---")

response = requests.put(
    f"{base_url}/1",
    json={
        "Name": "Premium Basmati Rice",
        "Price": 90,
        "UOM": "Kg",
        "CategoryID": 999
    }
)

print(response.status_code)
print(response.json())