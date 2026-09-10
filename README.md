# Grocery Store App

A Python Flask-based Grocery Store application with a Microsoft SQL Server database and a simple web-based frontend.

## Features

- View available products
- Search products by name
- Filter active products
- Add products to a cart
- Update product quantities
- Calculate cart totals
- Create customer orders
- View order details
- Product validation and management
- Product activation/deactivation
- Category management
- Order validation
- Database transaction handling

## Technologies

- Python
- Flask
- Microsoft SQL Server Express
- PyODBC
- HTML
- CSS
- JavaScript

## Project Structure

```text
GroceryStoreApp/
│
├── backend/
│   ├── app.py
│   ├── db.py
│   ├── test_categories.py
│   ├── test_db.py
│   ├── test_deactivation.py
│   ├── test_integration.py
│   ├── test_orders.py
│   ├── test_orders_get.py
│   └── test_validation.py
│
├── database/
│   └── grocery_store.sql
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── test_api.py
├── .gitignore
└── README.md
```

## Database

The application uses Microsoft SQL Server Express with the database:

```text
GroceryStoreDB
```

The database contains the following tables:

- `Categories`
- `Products`
- `Orders`
- `OrderDetails`

The database schema can be created using:

```text
database/grocery_store.sql
```

## Running the Application

Make sure SQL Server Express is running and the database connection details in:

```text
backend/db.py
```

match your local SQL Server setup.

Start the Flask application from the project directory:

```bash
python backend/app.py
```

Then open:

```text
http://127.0.0.1:5000/
```

## API Endpoints

### Products

```text
GET    /api/products
GET    /api/products/<id>
POST   /api/products
PUT    /api/products/<id>
DELETE /api/products/<id>
```

### Categories

```text
GET    /api/categories
GET    /api/categories/<id>
POST   /api/categories
PUT    /api/categories/<id>
DELETE /api/categories/<id>
```

### Orders

```text
GET  /api/orders
GET  /api/orders/<id>
POST /api/orders
```

## Testing

Backend functionality is tested using the Python test scripts in the `backend` folder.

```bash
python backend/test_db.py
python backend/test_categories.py
python backend/test_validation.py
python backend/test_deactivation.py
python backend/test_orders.py
python backend/test_orders_get.py
python backend/test_integration.py
```

The integration test verifies the main backend flow including product creation, category handling, order creation, order retrieval, and product deactivation.

## Author

Developed as part of an internship project.
