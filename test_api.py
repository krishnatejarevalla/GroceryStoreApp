import requests

base_url = "http://127.0.0.1:5000/api/products"


# ============================================================
# 1. GET ALL PRODUCTS
# ============================================================

print("\n--- GET ALL PRODUCTS ---")

response = requests.get(base_url)

print(response.status_code)
print(response.json())


# ============================================================
# 2. GET ACTIVE PRODUCTS
# ============================================================

print("\n--- GET ACTIVE PRODUCTS ---")

response = requests.get(
    base_url,
    params={"active": "true"}
)

print(response.status_code)
print(response.json())


# ============================================================
# 3. GET INACTIVE PRODUCTS
# ============================================================

print("\n--- GET INACTIVE PRODUCTS ---")

response = requests.get(
    base_url,
    params={"active": "false"}
)

print(response.status_code)
print(response.json())


# ============================================================
# 4. GET PRODUCTS - INVALID ACTIVE VALUE
# ============================================================

print("\n--- INVALID ACTIVE VALUE ---")

response = requests.get(
    base_url,
    params={"active": "yes"}
)

print(response.status_code)
print(response.json())


# ============================================================
# 5. SEARCH PRODUCT - FOUND
# ============================================================

print("\n--- SEARCH PRODUCT - FOUND ---")

response = requests.get(
    f"{base_url}/search",
    params={"name": "rice"}
)

print(response.status_code)
print(response.json())


# ============================================================
# 6. SEARCH PRODUCT - NOT FOUND
# ============================================================

print("\n--- SEARCH PRODUCT - NOT FOUND ---")

response = requests.get(
    f"{base_url}/search",
    params={"name": "xyz"}
)

print(response.status_code)
print(response.json())


# ============================================================
# 7. SEARCH PRODUCT - NAME MISSING
# ============================================================

print("\n--- SEARCH PRODUCT - NAME MISSING ---")

response = requests.get(
    f"{base_url}/search"
)

print(response.status_code)
print(response.json())


# ============================================================
# 8. ADD PRODUCT WITH CATEGORY
# ============================================================

print("\n--- ADD PRODUCT ---")

response = requests.post(
    base_url,
    json={
        "Name": "Sugar",
        "Price": 45,
        "UOM": "Kg",
        "CategoryID": 1
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 9. GET PRODUCT BY ID
# ============================================================

print("\n--- GET PRODUCT BY ID ---")

response = requests.get(
    f"{base_url}/1"
)

print(response.status_code)
print(response.json())


# ============================================================
# 10. GET PRODUCT BY INVALID ID
# ============================================================

print("\n--- GET INVALID PRODUCT ID ---")

response = requests.get(
    f"{base_url}/999"
)

print(response.status_code)
print(response.json())


# ============================================================
# 11. UPDATE PRODUCT
# ============================================================

print("\n--- UPDATE PRODUCT ---")

response = requests.put(
    f"{base_url}/1",
    json={
        "Name": "Premium Basmati Rice",
        "Price": 90,
        "UOM": "Kg",
        "CategoryID": 1
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 12. UPDATE INVALID PRODUCT
# ============================================================

print("\n--- UPDATE INVALID PRODUCT ---")

response = requests.put(
    f"{base_url}/999",
    json={
        "Name": "Test Product",
        "Price": 50,
        "UOM": "Kg"
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 13. DELETE INVALID PRODUCT
# ============================================================

print("\n--- DELETE INVALID PRODUCT ---")

response = requests.delete(
    f"{base_url}/999"
)

print(response.status_code)
print(response.json())