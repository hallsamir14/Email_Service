-- Switch to the new database
USE ecommerce;

-- Create the users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the products table
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the orders table
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Insert mock data into the users table
INSERT INTO users (username, email, password) VALUES
('john_doe', 'john@example.com', 'password123'),
('jane_smith', 'jane@example.com', 'password456'),
('alice_jones', 'alice@example.com', 'password789');

-- Insert mock data into the products table
INSERT INTO products (name, description, price) VALUES
('Laptop', 'A high-performance laptop', 999.99),
('Smartphone', 'A latest model smartphone', 699.99),
('Headphones', 'Noise-cancelling headphones', 199.99),
('Microphone', 'Condenser Microphone', 149.99);
-- Insert mock data into the orders table
INSERT INTO orders (user_id, product_id, quantity) VALUES
(1, 1, 1),  -- John Doe orders 1 Laptop
(2, 2, 2),  -- Jane Smith orders 2 Smartphones
(3, 3, 3);  -- Alice Jones orders 3 Headphones