import requests

base_url = "http://127.0.0.1:5000/api"


# ============================================================
# 1. CREATE CATEGORY
# ============================================================

print("\n--- 1. CREATE CATEGORY ---")

category_name = "Integration Test Category"

response = requests.post(
    f"{base_url}/categories",
    json={
        "CategoryName": category_name
    }
)

print(response.status_code)
print(response.json())

assert response.status_code in [201, 400]


# ============================================================
# 2. FIND CATEGORY
# ============================================================

print("\n--- 2. FIND CATEGORY ---")

response = requests.get(
    f"{base_url}/categories"
)

print(response.status_code)

assert response.status_code == 200

categories = response.json()

category_id = None

for category in categories:
    if category["CategoryName"] == category_name:
        category_id = category["CategoryID"]
        break

assert category_id is not None

print("CategoryID:", category_id)


# ============================================================
# 3. CREATE PRODUCT
# ============================================================

print("\n--- 3. CREATE PRODUCT ---")

product_name = "Integration Test Product"

response = requests.post(
    f"{base_url}/products",
    json={
        "Name": product_name,
        "Price": 25,
        "UOM": "Packet",
        "CategoryID": category_id
    }
)

print(response.status_code)
print(response.json())

assert response.status_code == 201


# ============================================================
# 4. FIND PRODUCT
# ============================================================

print("\n--- 4. FIND PRODUCT ---")

response = requests.get(
    f"{base_url}/products/search",
    params={
        "name": product_name
    }
)

print(response.status_code)
print(response.json())

assert response.status_code == 200

products = response.json()

product_id = None

for product in products:
    if (
        product["Name"] == product_name
        and product["IsActive"]
    ):
        product_id = product["ProductID"]
        break

assert product_id is not None

print("ProductID:", product_id)


# ============================================================
# 5. VERIFY PRODUCT CATEGORY
# ============================================================

print("\n--- 5. VERIFY PRODUCT CATEGORY ---")

response = requests.get(
    f"{base_url}/products/{product_id}"
)

print(response.status_code)
print(response.json())

assert response.status_code == 200

product = response.json()

assert product["CategoryID"] == category_id
assert product["CategoryName"] == category_name


# ============================================================
# 6. UPDATE PRODUCT
# ============================================================

print("\n--- 6. UPDATE PRODUCT ---")

response = requests.put(
    f"{base_url}/products/{product_id}",
    json={
        "Name": product_name,
        "Price": 30,
        "UOM": "Packet",
        "CategoryID": category_id
    }
)

print(response.status_code)
print(response.json())

assert response.status_code == 200


# ============================================================
# 7. CREATE ORDER
# ============================================================

print("\n--- 7. CREATE ORDER ---")

response = requests.post(
    f"{base_url}/orders",
    json={
        "CustomerName": "Integration Test Customer",
        "Items": [
            {
                "ProductID": product_id,
                "Quantity": 2
            }
        ]
    }
)

print(response.status_code)
print(response.json())

assert response.status_code == 201

created_order = response.json()

order_id = created_order["OrderID"]

assert created_order["TotalAmount"] == 60.0


# ============================================================
# 8. RETRIEVE ORDER
# ============================================================

print("\n--- 8. RETRIEVE ORDER ---")

response = requests.get(
    f"{base_url}/orders/{order_id}"
)

print(response.status_code)
print(response.json())

assert response.status_code == 200

order = response.json()

assert order["OrderID"] == order_id
assert order["CustomerName"] == "Integration Test Customer"
assert order["TotalAmount"] == 60.0

assert len(order["Items"]) == 1

assert order["Items"][0]["ProductID"] == product_id
assert order["Items"][0]["Quantity"] == 2.0
assert order["Items"][0]["UnitPrice"] == 30.0
assert order["Items"][0]["TotalPrice"] == 60.0


# ============================================================
# 9. DEACTIVATE PRODUCT
# ============================================================

print("\n--- 9. DEACTIVATE PRODUCT ---")

response = requests.delete(
    f"{base_url}/products/{product_id}"
)

print(response.status_code)
print(response.json())

assert response.status_code == 200


# ============================================================
# 10. VERIFY PRODUCT IS INACTIVE
# ============================================================

print("\n--- 10. VERIFY PRODUCT IS INACTIVE ---")

response = requests.get(
    f"{base_url}/products/{product_id}"
)

print(response.status_code)
print(response.json())

assert response.status_code == 200

product = response.json()

assert product["IsActive"] is False


# ============================================================
# FINAL RESULT
# ============================================================

print("\n========================================")
print("ALL BACKEND INTEGRATION TESTS PASSED")
print("========================================")