-- 0-uniq_users.sql
-- Task 0: We are all unique!

-- Create table users with required attributes
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
