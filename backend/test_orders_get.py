import requests

base_url = "http://127.0.0.1:5000/api/orders"


# ============================================================
# 1. GET ALL ORDERS
# ============================================================

print("\n--- GET ALL ORDERS ---")

response = requests.get(base_url)

print(response.status_code)
print(response.json())


# ============================================================
# 2. GET ORDER BY ID
# ============================================================

print("\n--- GET ORDER BY ID ---")

response = requests.get(
    base_url + "/48"
)

print(response.status_code)
print(response.json())


# ============================================================
# 3. GET NON-EXISTENT ORDER
# ============================================================

print("\n--- GET NON-EXISTENT ORDER ---")

response = requests.get(
    base_url + "/99999"
)

print(response.status_code)
print(response.json())