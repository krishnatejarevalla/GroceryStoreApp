import requests

url = "http://127.0.0.1:5000/api/products/1"

response = requests.get(url)

print(response.status_code)
print(response.json())


# Test product not found
url = "http://127.0.0.1:5000/api/products/999"

response = requests.get(url)

print(response.status_code)
print(response.json())