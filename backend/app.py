from flask import Flask, jsonify, request
from db import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    return "Grocery Store App is running!"
@app.route("/api/products")
def get_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()

    columns = [column[0] for column in cursor.description]

    products_list = []

    for product in products:
        product_dict = dict(zip(columns, product))
        products_list.append(product_dict)

    cursor.close()
    connection.close()

    return jsonify(products_list)
@app.route("/api/products", methods = ["POST"])
def add_products():
    data = request.json

    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    name = data["Name"]
    price = data["Price"]
    uom = data["UOM"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO Products (Name, Price, UOM, IsActive)
        VALUES (?, ?, ?, ?)
    """,
        (name, price, uom, True)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Products added Successfully!"}), 201


if __name__ == "__main__":
    app.run(debug=True)