from flask import Flask, jsonify, request
from db import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    return "Grocery Store App is running!"

@app.route("/api/products")
def get_products():
    active = request.args.get("active")

    connection = get_connection()
    cursor = connection.cursor()

    if active is None:
        cursor.execute("""
            SELECT
                p.ProductID,
                p.Name,
                p.Price,
                p.UOM,
                p.IsActive,
                p.CategoryID,
                c.CategoryName
            FROM Products p
            LEFT JOIN Categories c
                ON p.CategoryID = c.CategoryID
        """)
    elif active.lower() == "true":
        cursor.execute("""
            SELECT
                p.ProductID,
                p.Name,
                p.Price,
                p.UOM,
                p.IsActive,
                p.CategoryID,
                c.CategoryName
            FROM Products p
            LEFT JOIN Categories c
                ON p.CategoryID = c.CategoryID
            WHERE p.IsActive = 1
        """)
    elif active.lower() == "false":
        cursor.execute("""
            SELECT
                p.ProductID,
                p.Name,
                p.Price,
                p.UOM,
                p.IsActive,
                p.CategoryID,
                c.CategoryName
            FROM Products p
            LEFT JOIN Categories c
                ON p.CategoryID = c.CategoryID
            WHERE p.IsActive = 0
        """)
    else:
        cursor.close()
        connection.close()
        return jsonify({"message": "active must be true or false"}), 400

    products = cursor.fetchall()

    products_list = []

    for product in products:
       products_list.append({
        "ProductID": product.ProductID,
        "Name": product.Name,
        "Price": float(product.Price),
        "UOM": product.UOM,
        "IsActive": bool(product.IsActive),
        "CategoryID": product.CategoryID,
        "CategoryName": product.CategoryName
        })

    cursor.close()
    connection.close()

    return jsonify(products_list)

@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            p.ProductID,
            p.Name,
            p.Price,
            p.UOM,
            p.IsActive,
            p.CategoryID,
            c.CategoryName
        FROM Products p
        LEFT JOIN Categories c
            ON p.CategoryID = c.CategoryID
        WHERE p.ProductID = ?
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    cursor.close()
    connection.close()

    if product is None:
        return jsonify({"message": "Product not found!"}), 404

    return jsonify({
        "ProductID": product.ProductID,
        "Name": product.Name,
        "Price": float(product.Price),
        "UOM": product.UOM,
        "IsActive": bool(product.IsActive),
        "CategoryID": product.CategoryID,
        "CategoryName": product.CategoryName
    }), 200

@app.route("/api/products/search", methods=["GET"])
def search_products():
    name = request.args.get("name")

    if not name:
        return jsonify({"message": "Search name is required!"}), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
    """
    SELECT
        p.ProductID,
        p.Name,
        p.Price,
        p.UOM,
        p.IsActive,
        p.CategoryID,
        c.CategoryName
    FROM Products p
    LEFT JOIN Categories c
        ON p.CategoryID = c.CategoryID
    WHERE p.Name LIKE ? AND p.IsActive = 1
    """,
    (f"%{name}%",)
    )

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    products_list = []

    for product in products:
        products_list.append({
        "ProductID": product[0],
        "Name": product[1],
        "Price": float(product[2]),
        "UOM": product[3],
        "IsActive": bool(product[4]),
        "CategoryID": product[5],
        "CategoryName": product[6]
    })

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
    category_id = data.get("CategoryID")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO Products (Name, Price, UOM, IsActive, CategoryID)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, price, uom, True, category_id)
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
    category_id = data.get("CategoryID")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE Products
        SET Name = ?, Price = ?, UOM = ?, CategoryID = ?
        WHERE ProductID = ?
        """,
        (name, price, uom, category_id, product_id)
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