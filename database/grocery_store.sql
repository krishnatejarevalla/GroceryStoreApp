-- Create the Grocery Store database
IF NOT EXISTS (
    SELECT name
    FROM sys.databases
    WHERE name = 'GroceryStoreDB'
)
BEGIN
    CREATE DATABASE GroceryStoreDB;
END;
GO

-- Use the Grocery Store database
USE GroceryStoreDB;
GO


-- ============================================
-- Categories Table
-- ============================================
CREATE TABLE Categories
(
    CategoryID INT IDENTITY(1,1) PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1
);
GO


-- ============================================
-- Products Table
-- ============================================
CREATE TABLE Products
(
    ProductID INT IDENTITY(1,1) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    UOM VARCHAR(20) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    CategoryID INT NULL,

    CONSTRAINT FK_Products_Categories
        FOREIGN KEY (CategoryID)
        REFERENCES Categories(CategoryID)
);
GO


-- ============================================
-- Orders Table
-- ============================================
CREATE TABLE Orders
(
    OrderID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerName VARCHAR(100) NOT NULL,
    OrderDate DATETIME NOT NULL DEFAULT GETDATE(),
    TotalAmount DECIMAL(10,2) NOT NULL DEFAULT 0
);
GO


-- ============================================
-- OrderDetails Table
-- ============================================
CREATE TABLE OrderDetails
(
    OrderDetailID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity DECIMAL(10,2) NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,
    TotalPrice AS (Quantity * UnitPrice) PERSISTED,

    CONSTRAINT FK_OrderDetails_Orders
        FOREIGN KEY (OrderID)
        REFERENCES Orders(OrderID),

    CONSTRAINT FK_OrderDetails_Products
        FOREIGN KEY (ProductID)
        REFERENCES Products(ProductID)
);
GO