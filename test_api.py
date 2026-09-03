import requests

url = "http://127.0.0.1:5000/api/products"

product = {
    "Name": "Rice",
    "Price": 60,
    "UOM": "Kg"
}

response = requests.post(url, json=product)

print(response.status_code)
print(response.json())