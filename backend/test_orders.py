import requests

base_url = "http://127.0.0.1:5000/api/orders"


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