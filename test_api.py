import requests

url = "http://127.0.0.1:5000/api/products/1"

product = {
    "Name": "Basmati Rice",
    "Price": 80,
    "UOM": "Kg"
}

response = requests.put(url, json=product)

print(response.status_code)
print(response.json())