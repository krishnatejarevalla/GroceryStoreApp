import requests

base_url = "http://127.0.0.1:5000/api/products"


# Test search - product found
response = requests.get(
    f"{base_url}/search",
    params={"name": "rice"}
)

print(response.status_code)
print(response.json())


# Test search - product not found
response = requests.get(
    f"{base_url}/search",
    params={"name": "xyz"}
)

print(response.status_code)
print(response.json())


# Test search - missing name
response = requests.get(
    f"{base_url}/search"
)

print(response.status_code)
print(response.json())