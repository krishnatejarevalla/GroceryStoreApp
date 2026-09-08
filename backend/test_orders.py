import requests

base_url = "http://127.0.0.1:5000/api/orders"
product_url = "http://127.0.0.1:5000/api/products"


# ============================================================
# 1. CREATE ORDER
# ============================================================

print("\n--- CREATE ORDER ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Teja",
        "Items": [
            {
                "ProductID": 1,
                "Quantity": 2
            },
            {
                "ProductID": 3,
                "Quantity": 3
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 2. CREATE ORDER - MISSING CUSTOMER NAME
# ============================================================

print("\n--- CREATE ORDER - MISSING CUSTOMER NAME ---")

response = requests.post(
    base_url,
    json={
        "Items": [
            {
                "ProductID": 1,
                "Quantity": 2
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 3. CREATE ORDER - EMPTY CUSTOMER NAME
# ============================================================

print("\n--- CREATE ORDER - EMPTY CUSTOMER NAME ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "",
        "Items": [
            {
                "ProductID": 1,
                "Quantity": 2
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 4. CREATE ORDER - MISSING ITEMS
# ============================================================

print("\n--- CREATE ORDER - MISSING ITEMS ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Teja"
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 5. CREATE ORDER - ITEMS NOT A LIST
# ============================================================

print("\n--- CREATE ORDER - ITEMS NOT A LIST ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Teja",
        "Items": "Product 1"
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 6. CREATE ORDER - EMPTY ITEMS
# ============================================================

print("\n--- CREATE ORDER - EMPTY ITEMS ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Teja",
        "Items": []
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 7. CREATE ORDER - ITEM IS NOT AN OBJECT
# ============================================================

print("\n--- CREATE ORDER - ITEM IS NOT AN OBJECT ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Teja",
        "Items": [
            "Product 1"
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 8. CREATE ORDER - MISSING PRODUCT ID
# ============================================================

print("\n--- CREATE ORDER - MISSING PRODUCT ID ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Teja",
        "Items": [
            {
                "Quantity": 2
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 9. CREATE ORDER - MISSING QUANTITY
# ============================================================

print("\n--- CREATE ORDER - MISSING QUANTITY ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Teja",
        "Items": [
            {
                "ProductID": 1
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 10. CREATE ORDER - INVALID PRODUCT ID
# ============================================================

print("\n--- CREATE ORDER - INVALID PRODUCT ID ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Teja",
        "Items": [
            {
                "ProductID": "abc",
                "Quantity": 2
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 11. CREATE ORDER - INVALID QUANTITY
# ============================================================

print("\n--- CREATE ORDER - INVALID QUANTITY ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Teja",
        "Items": [
            {
                "ProductID": 1,
                "Quantity": "abc"
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 12. CREATE ORDER - ZERO QUANTITY
# ============================================================

print("\n--- CREATE ORDER - ZERO QUANTITY ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Teja",
        "Items": [
            {
                "ProductID": 1,
                "Quantity": 0
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 13. CREATE ORDER - NEGATIVE QUANTITY
# ============================================================

print("\n--- CREATE ORDER - NEGATIVE QUANTITY ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Teja",
        "Items": [
            {
                "ProductID": 1,
                "Quantity": -2
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 14. CREATE ORDER - NON-EXISTENT PRODUCT
# ============================================================

print("\n--- CREATE ORDER - NON-EXISTENT PRODUCT ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Teja",
        "Items": [
            {
                "ProductID": 99999,
                "Quantity": 2
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 15. CREATE ORDER - INACTIVE PRODUCT
# ============================================================

print("\n--- CREATE ORDER - INACTIVE PRODUCT ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Teja",
        "Items": [
            {
                "ProductID": 4,
                "Quantity": 2
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 16. CREATE ORDER - ROLLBACK TEST
# ============================================================

print("\n--- CREATE ORDER - ROLLBACK TEST ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Rollback Test",
        "Items": [
            {
                "ProductID": 1,
                "Quantity": 2
            },
            {
                "ProductID": 99999,
                "Quantity": 3
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 17. CREATE ORDER - DUPLICATE PRODUCT
# ============================================================

print("\n--- CREATE ORDER - DUPLICATE PRODUCT ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Teja",
        "Items": [
            {
                "ProductID": 1,
                "Quantity": 2
            },
            {
                "ProductID": 1,
                "Quantity": 3
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 18. CREATE ORDER - DECIMAL QUANTITY
# ============================================================

print("\n--- CREATE ORDER - DECIMAL QUANTITY ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Decimal Quantity Test",
        "Items": [
            {
                "ProductID": 1,
                "Quantity": 1.50
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# SETUP - FIND OR CREATE PACKET PRODUCT
# ============================================================

print("\n--- SETUP - FIND OR CREATE PACKET PRODUCT ---")

# Search for an existing Test Chips product
response = requests.get(
    product_url + "/search",
    params={
        "name": "Test Chips"
    }
)

print("Search status:", response.status_code)

products = response.json()

packet_product_id = None

# Look for an active Packet product
if response.status_code == 200:

    for product in products:
        if (
            product["Name"] == "Test Chips"
            and product["UOM"].lower() == "packet"
            and product["IsActive"] == 1
        ):
            packet_product_id = product["ProductID"]
            break


# If no suitable product exists, create one
if packet_product_id is None:

    print("No active Packet test product found. Creating one...")

    response = requests.post(
        product_url,
        json={
            "Name": "Test Chips",
            "Price": 50,
            "UOM": "Packet",
            "CategoryID": 1
        }
    )

    print("Create status:", response.status_code)
    print(response.json())

    # Search again to get the generated ProductID
    response = requests.get(
        product_url + "/search",
        params={
            "name": "Test Chips"
        }
    )

    products = response.json()

    for product in products:
        if (
            product["Name"] == "Test Chips"
            and product["UOM"].lower() == "packet"
            and product["IsActive"] == 1
        ):
            packet_product_id = product["ProductID"]
            break


print("Temporary Packet ProductID:", packet_product_id)


# ============================================================
# 19. CREATE ORDER - FRACTIONAL PACKET QUANTITY
# ============================================================

print("\n--- CREATE ORDER - FRACTIONAL PACKET QUANTITY ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Packet Decimal Test",
        "Items": [
            {
                "ProductID": packet_product_id,
                "Quantity": 1.50
            }
        ]
    }
)

print(response.status_code)
print(response.json())


# ============================================================
# 20. CREATE ORDER - WHOLE PACKET QUANTITY
# ============================================================

print("\n--- CREATE ORDER - WHOLE PACKET QUANTITY ---")

response = requests.post(
    base_url,
    json={
        "CustomerName": "Packet Whole Test",
        "Items": [
            {
                "ProductID": packet_product_id,
                "Quantity": 2
            }
        ]
    }
)

print(response.status_code)
print(response.json())
