import requests

base_url = "http://127.0.0.1:5000/api/orders"


# ============================================================
# 1. GET ALL ORDERS
# ============================================================

print("\n--- GET ALL ORDERS ---")

response = requests.get(base_url)

print("Status:", response.status_code)
print("Response:", response.json())

assert response.status_code == 200

orders = response.json()

assert isinstance(orders, list)
assert len(orders) > 0

for order in orders:
    assert "OrderID" in order
    assert "CustomerName" in order
    assert "TotalAmount" in order

print("GET ALL ORDERS: PASS")


# ============================================================
# 2. CHECK ORDER LIST SORTING
# ============================================================

print("\n--- CHECK ORDER SORTING ---")

order_ids = [order["OrderID"] for order in orders]

assert order_ids == sorted(order_ids, reverse=True)

print("Orders are sorted by OrderID descending: PASS")


# ============================================================
# 3. GET ORDER BY ID
# ============================================================

print("\n--- GET ORDER BY ID ---")

order_id = 48

response = requests.get(
    f"{base_url}/{order_id}"
)

print("Status:", response.status_code)
print("Response:", response.json())

assert response.status_code == 200

order = response.json()

assert order["OrderID"] == order_id
assert order["CustomerName"] == "Teja"
assert "TotalAmount" in order
assert "Items" in order

assert isinstance(order["Items"], list)
assert len(order["Items"]) > 0

print("GET ORDER BY ID: PASS")


# ============================================================
# 4. GET NON-EXISTENT ORDER
# ============================================================

print("\n--- GET NON-EXISTENT ORDER ---")

response = requests.get(
    f"{base_url}/99999"
)

print("Status:", response.status_code)
print("Response:", response.json())

assert response.status_code == 404
assert response.json()["message"] == "Order not found!"

print("GET NON-EXISTENT ORDER: PASS")


# ============================================================
# FINAL RESULT
# ============================================================

print("\n========================================")
print("ALL ORDER LISTING TESTS PASSED")
print("========================================")