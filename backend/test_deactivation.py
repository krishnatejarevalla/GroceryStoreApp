import requests

base_url = "http://127.0.0.1:5000/api/products"


# ============================================================
# 1. DEACTIVATE PRODUCT
# ============================================================

print("\n--- DEACTIVATE PRODUCT ---")

response = requests.delete(
    f"{base_url}/4"
)

print(response.status_code)
print(response.json())


# ============================================================
# 2. CHECK ACTIVE PRODUCTS
# ============================================================

print("\n--- CHECK ACTIVE PRODUCTS ---")

response = requests.get(
    base_url,
    params={"active": "true"}
)

print(response.status_code)
print(response.json())


# ============================================================
# 3. CHECK INACTIVE PRODUCTS
# ============================================================

print("\n--- CHECK INACTIVE PRODUCTS ---")

response = requests.get(
    base_url,
    params={"active": "false"}
)

print(response.status_code)
print(response.json())


# ============================================================
# 4. DEACTIVATE ALREADY INACTIVE PRODUCT
# ============================================================

print("\n--- DEACTIVATE ALREADY INACTIVE PRODUCT ---")

response = requests.delete(
    f"{base_url}/4"
)

print(response.status_code)
print(response.json())


# ============================================================
# 5. DEACTIVATE INVALID PRODUCT
# ============================================================

print("\n--- DEACTIVATE INVALID PRODUCT ---")

response = requests.delete(
    f"{base_url}/999"
)

print(response.status_code)
print(response.json())