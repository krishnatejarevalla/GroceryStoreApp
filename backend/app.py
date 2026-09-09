from flask import Flask, jsonify, request
from db import get_connection

app = Flask(__name__)

def validate_product_data(data):

    if not data:
        return "Request body is required!"

    if "Name" not in data:
        return "Name is required!"

    if "Price" not in data:
        return "Price is required!"

    if "UOM" not in data:
        return "UOM is required!"

    if not isinstance(data["Name"], str) or not data["Name"].strip():
        return "Name cannot be empty!"

    if not isinstance(data["UOM"], str) or not data["UOM"].strip():
        return "UOM cannot be empty!"

    try:
        price = float(data["Price"])
    except (ValueError, TypeError):
        return "Price must be a number!"

    if price <= 0:
        return "Price must be greater than 0!"

    if "CategoryID" in data and data["CategoryID"] is not None:
        try:
            category_id = int(data["CategoryID"])
        except (ValueError, TypeError):
            return "CategoryID must be a number!"

        if category_id <= 0:
            return "CategoryID must be greater than 0!"

    return None

def validate_order_data(data):

    if not data:
        return "Request body is required!"

    if "CustomerName" not in data:
        return "CustomerName is required!"

    if "Items" not in data:
        return "Items are required!"

    customer_name = data["CustomerName"]
    items = data["Items"]

    if not isinstance(customer_name, str) or not customer_name.strip():
        return "CustomerName cannot be empty!"

    if not isinstance(items, list):
        return "Items must be a list!"

    if len(items) == 0:
        return "Items cannot be empty!"
    product_ids = set()

    for item in items:

        if not isinstance(item, dict):
            return "Each item must be an object!"

        if "ProductID" not in item:
            return "ProductID is required!"

        if "Quantity" not in item:
            return "Quantity is required!"

        try:
            product_id = int(item["ProductID"])

            if isinstance(item["ProductID"], float) and not item["ProductID"].is_integer():
                return "ProductID must be a whole number!"

        except (ValueError, TypeError):
            return "ProductID must be a number!"

        if product_id <= 0:
            return "ProductID must be greater than 0!"

        if product_id in product_ids:
            return "Duplicate ProductID is not allowed!"

        product_ids.add(product_id)

        try:
            quantity = float(item["Quantity"])
        except (ValueError, TypeError):
            return "Quantity must be a number!"

        if quantity <= 0:
            return "Quantity must be greater than 0!"

    return None

    

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

    validation_error = validate_product_data(data)

    if validation_error:
        return jsonify({"message": validation_error}), 400

    name = data["Name"]
    price = float(data["Price"])
    uom = data["UOM"]
    category_id = data.get("CategoryID")

    connection = get_connection()
    cursor = connection.cursor()

    if category_id is not None:
        cursor.execute(
            """
            SELECT CategoryID
            FROM Categories
            WHERE CategoryID = ? AND IsActive = 1
            """,
            (category_id,)
        )

        category = cursor.fetchone()

        if category is None:
            cursor.close()
            connection.close()

            return jsonify({
                "message": "Category not found!"
            }), 400

    cursor.execute(
        """
        INSERT INTO Products (Name, Price, UOM, IsActive, CategoryID)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name.strip(), price, uom.strip(), True, category_id)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Product added successfully!"
    }), 201

@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):

    data = request.json

    validation_error = validate_product_data(data)

    if validation_error:
        return jsonify({"message": validation_error}), 400

    name = data["Name"]
    price = float(data["Price"])
    uom = data["UOM"]
    category_id = data.get("CategoryID")

    connection = get_connection()
    cursor = connection.cursor()

    if category_id is not None:
        cursor.execute(
            """
            SELECT CategoryID
            FROM Categories
            WHERE CategoryID = ? AND IsActive = 1
            """,
            (category_id,)
        )

        category = cursor.fetchone()

        if category is None:
            cursor.close()
            connection.close()

            return jsonify({
                "message": "Category not found!"
            }), 400

    cursor.execute(
        """
        UPDATE Products
        SET Name = ?, Price = ?, UOM = ?, CategoryID = ?
        WHERE ProductID = ?
        """,
        (name.strip(), price, uom.strip(), category_id, product_id)
    )

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()

        return jsonify({
            "message": "Product not found!"
        }), 404

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Product updated successfully!"
    }), 200

@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE Products
        SET IsActive = 0
        WHERE ProductID = ? AND IsActive = 1
        """,
        (product_id,)
    )

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()

        return jsonify({
            "message": "Product not found or already inactive!"
        }), 404

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Product deactivated successfully!"
    }), 200

@app.route("/api/categories", methods=["GET"])
def get_categories():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            CategoryID,
            CategoryName,
            IsActive
        FROM Categories
        """
    )

    categories = cursor.fetchall()

    cursor.close()
    connection.close()

    categories_list = []

    for category in categories:
        categories_list.append({
            "CategoryID": category.CategoryID,
            "CategoryName": category.CategoryName,
            "IsActive": bool(category.IsActive)
        })

    return jsonify(categories_list), 200

@app.route("/api/categories/<int:category_id>", methods=["GET"])
def get_category_by_id(category_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            CategoryID,
            CategoryName,
            IsActive
        FROM Categories
        WHERE CategoryID = ?
        """,
        (category_id,)
    )

    category = cursor.fetchone()

    cursor.close()
    connection.close()

    if category is None:
        return jsonify({
            "message": "Category not found!"
        }), 404

    return jsonify({
        "CategoryID": category.CategoryID,
        "CategoryName": category.CategoryName,
        "IsActive": bool(category.IsActive)
    }), 200

@app.route("/api/categories", methods=["POST"])
def add_category():

    data = request.json

    if not data:
        return jsonify({
            "message": "Request body is required!"
        }), 400

    if "CategoryName" not in data:
        return jsonify({
            "message": "CategoryName is required!"
        }), 400

    category_name = data["CategoryName"]

    if not isinstance(category_name, str) or not category_name.strip():
        return jsonify({
            "message": "CategoryName cannot be empty!"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT CategoryID
        FROM Categories
        WHERE CategoryName = ?
        """,
        (category_name.strip(),)
    )

    existing_category = cursor.fetchone()

    if existing_category is not None:
        cursor.close()
        connection.close()

        return jsonify({
            "message": "Category already exists!"
        }), 400

    cursor.execute(
        """
        INSERT INTO Categories (CategoryName, IsActive)
        VALUES (?, ?)
        """,
        (category_name.strip(), True)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Category added successfully!"
    }), 201

@app.route("/api/categories/<int:category_id>", methods=["PUT"])
def update_category(category_id):

    data = request.json

    if not data:
        return jsonify({
            "message": "Request body is required!"
        }), 400

    if "CategoryName" not in data:
        return jsonify({
            "message": "CategoryName is required!"
        }), 400

    category_name = data["CategoryName"]

    if not isinstance(category_name, str) or not category_name.strip():
        return jsonify({
            "message": "CategoryName cannot be empty!"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT CategoryID
        FROM Categories
        WHERE CategoryName = ?
        AND CategoryID != ?
        """,
        (category_name.strip(), category_id)
    )

    existing_category = cursor.fetchone()

    if existing_category is not None:
        cursor.close()
        connection.close()

        return jsonify({
            "message": "Category already exists!"
        }), 400

    cursor.execute(
        """
        UPDATE Categories
        SET CategoryName = ?
        WHERE CategoryID = ?
        AND IsActive = 1
        """,
        (category_name.strip(), category_id)
    )

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()

        return jsonify({
            "message": "Category not found or inactive!"
        }), 404

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Category updated successfully!"
    }), 200

@app.route("/api/categories/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE Categories
        SET IsActive = 0
        WHERE CategoryID = ? AND IsActive = 1
        """,
        (category_id,)
    )

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()

        return jsonify({
            "message": "Category not found or already inactive!"
        }), 404

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Category deactivated successfully!"
    }), 200

@app.route("/api/orders", methods=["POST"])
def create_order():

    data = request.json

    validation_error = validate_order_data(data)

    if validation_error:
        return jsonify({
            "message": validation_error
        }), 400

    customer_name = data["CustomerName"]
    items = data["Items"]

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ------------------------------------------------
        # 1. Create the order
        # ------------------------------------------------

        cursor.execute(
            """
            INSERT INTO Orders (CustomerName, TotalAmount)
            OUTPUT INSERTED.OrderID
            VALUES (?, ?)
            """,
            (customer_name.strip(), 0)
        )

        # ------------------------------------------------
        # 2. Get the newly created OrderID
        # ------------------------------------------------

        order_id = int(cursor.fetchone()[0])

        total_amount = 0

        # ------------------------------------------------
        # 3. Add each product to OrderDetails
        # ------------------------------------------------

        for item in items:

            product_id = int(item["ProductID"])
            quantity = float(item["Quantity"])

            cursor.execute(
                """
                SELECT Price, UOM
                FROM Products
                WHERE ProductID = ?
                AND IsActive = 1
                """,
                (product_id,)
            )

            product = cursor.fetchone()

            if product is None:
                connection.rollback()

                return jsonify({
                    "message": f"Product {product_id} not found or inactive!"
                }), 400

            unit_price = float(product.Price)

            uom = product.UOM

            if uom.lower() not in ["kg"] and not quantity.is_integer():
                connection.rollback()

                return jsonify({
                    "message": f"Fractional quantity is not allowed for {uom} products!"
                }), 400

            item_total = unit_price * quantity

            total_amount += item_total

            cursor.execute(
            """
            INSERT INTO OrderDetails
            (OrderID, ProductID, Quantity, UnitPrice)
            VALUES (?, ?, ?, ?)
            """,
            (
                order_id,
                product_id,
                quantity,
                unit_price
            )
        )

        # ------------------------------------------------
        # 4. Update the order total
        # ------------------------------------------------

        cursor.execute(
            """
            UPDATE Orders
            SET TotalAmount = ?
            WHERE OrderID = ?
            """,
            (total_amount, order_id)
        )

        # ------------------------------------------------
        # 5. Save everything
        # ------------------------------------------------

        connection.commit()

        return jsonify({
            "message": "Order created successfully!",
            "OrderID": order_id,
            "TotalAmount": total_amount
        }), 201

    except Exception as e:

        connection.rollback()

        return jsonify({
            "message": "Failed to create order!",
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()

if __name__ == "__main__":
    app.run(debug=True)