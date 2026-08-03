-- ==========================================
-- Customer Retention & Revenue Intelligence Platform
-- Database Schema
-- ==========================================

-- Drop tables if they already exist
DROP TABLE IF EXISTS customers CASCADE;

-- Create Customers Table
CREATE TABLE customers (

    customer_id VARCHAR(50) PRIMARY KEY,

    customer_unique_id VARCHAR(50) NOT NULL,

    customer_zip_code_prefix INTEGER,

    customer_city VARCHAR(100),

    customer_state VARCHAR(5)

);