import pyodbc

def get_connection():
    connection = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=KRISHNATEJA\\SQLEXPRESS;"
        "DATABASE=GroceryStoreDB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"

    )

    return connection