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
@app.route("/api/products", methods=["POST"])
def add_products():

    data = request.json

    if not data:
        return jsonify({"message": "Request body is required!"}), 400

    if "Name" not in data or "Price" not in data or "UOM" not in data:
        return jsonify({
            "message": "Name, Price and UOM are required!"
        }), 400

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

    return jsonify({"message": "Product added successfully!"}), 201

@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):

    data = request.json

    name = data["Name"]
    price = data["Price"]
    uom = data["UOM"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE Products
        SET Name = ?, Price = ?, UOM = ?
        WHERE ProductID = ?
        """,
        (name, price, uom, product_id)
    )

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()

        return jsonify({"message": "Product not found!"}), 404

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Product updated successfully!"}), 200

@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM Products WHERE ProductID = ?",
        (product_id,)
    )

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()

        return jsonify({"message": "Product not found!"}), 404

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Product deleted successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)