CREATE DATABASE ECommerceDB;
GO

USE ECommerceDB;
GO

CREATE TABLE Customer (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(100) NOT NULL
);

CREATE TABLE Category (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(100) NOT NULL
);

CREATE TABLE Product (
    id INT PRIMARY KEY IDENTITY(1,1),
    category_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    discount_price DECIMAL(10,2) NULL,

    FOREIGN KEY (category_id) REFERENCES Category(id)
);

CREATE TABLE Cart (
    id INT PRIMARY KEY IDENTITY(1,1),
    cust_id INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    coupon_code VARCHAR(50) NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,

    FOREIGN KEY (cust_id) REFERENCES Customer(id)
);

CREATE TABLE Cart_Item (
    id INT PRIMARY KEY IDENTITY(1,1),
    cart_id INT NOT NULL,
    prod_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,

    FOREIGN KEY (cart_id) REFERENCES Cart(id),
    FOREIGN KEY (prod_id) REFERENCES Product(id)
);

CREATE TABLE Wishlist (
    id INT PRIMARY KEY IDENTITY(1,1),
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (customer_id) REFERENCES Customer(id),
    FOREIGN KEY (product_id) REFERENCES Product(id)
);