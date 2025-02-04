-- Create Store Dimension
CREATE OR REPLACE TABLE sales_schema.dim_store (
    store_id INT PRIMARY KEY,
    store_name STRING,
    region_id INT
);

-- Create Date Dimension
CREATE OR REPLACE TABLE sales_schema.dim_date (
    date_id INT PRIMARY KEY AUTOINCREMENT,
    sales_date DATE UNIQUE,
    day INT,
    month INT,
    year INT,
    quarter INT,
    weekday STRING
);

-- Create Product Dimension
CREATE OR REPLACE TABLE sales_schema.dim_product (
    product_id INT PRIMARY KEY,
    product_name STRING,
    category STRING,
    price DECIMAL(10,2)
);

-- Create Region Dimension
CREATE OR REPLACE TABLE sales_schema.dim_region (
    region_id INT PRIMARY KEY,
    region_name STRING,
    country STRING
);

-- Create Fact Table

CREATE OR REPLACE TABLE sales_schema.fact_sales (
    sales_id INT PRIMARY KEY AUTOINCREMENT,
    store_id INT,
    date_id INT,
    product_id INT,
    weekly_sales DECIMAL(12,2),
    is_holiday BOOLEAN,
    temperature FLOAT,
    fuel_price FLOAT,
    cpi FLOAT,
    unemployment FLOAT,
    FOREIGN KEY (store_id) REFERENCES sales_schema.dim_store(store_id),
    FOREIGN KEY (date_id) REFERENCES sales_schema.dim_date(date_id),
    FOREIGN KEY (product_id) REFERENCES sales_schema.dim_product(product_id)
);

-- Populaing the Dimension Tables

-- dim_store

INSERT INTO sales_schema.dim_store (store_id, store_name, region_id)
SELECT DISTINCT store_id, CONCAT('Store ', store_id), NULL
FROM sales_schema.weekly_sales;

-- dim_date

INSERT INTO sales_schema.dim_date (sales_date, day, month, year, quarter, weekday)
SELECT DISTINCT sales_date,
       DAY(sales_date),
       MONTH(sales_date),
       YEAR(sales_date),
       QUARTER(sales_date),
       CASE WHEN DAYOFWEEK(sales_date) IN (1, 7) THEN 'Weekend' ELSE 'Weekday' END
FROM sales_schema.weekly_sales;

-- dim_region

INSERT INTO sales_schema.dim_region (region_id, region_name, country)
VALUES (1, 'North', 'USA'),
       (2, 'South', 'USA'),
       (3, 'East', 'USA'),
       (4, 'West', 'USA'),
       (5, 'Central', 'USA');

-- dim_product

INSERT INTO sales_schema.dim_product (product_id, product_name, category, price)
VALUES (1001, 'Electronics', 'Technology', 500.00),
       (1002, 'Groceries', 'Food', 20.00),
       (1003, 'Clothing', 'Fashion', 45.00);


-- Populating the Fact Table

INSERT INTO sales_schema.fact_sales (store_id, date_id, product_id, weekly_sales, is_holiday, temperature, fuel_price, cpi, unemployment)
SELECT ws.store_id,
       dd.date_id,
       dp.product_id,
       ws.weekly_sales,
       ws.is_holiday,
       ws.temperature,
       ws.fuel_price,
       ws.cpi,
       ws.unemployment
FROM sales_schema.weekly_sales ws
JOIN sales_schema.dim_date dd ON ws.sales_date = dd.sales_date
LEFT JOIN sales_schema.dim_product dp ON dp.product_id = 1001;  -- Assign a default product_id (modify based on real product mapping)

-- Check the Table Structure

DESC TABLE sales_schema.fact_sales;
DESC TABLE sales_schema.dim_store;
DESC TABLE sales_schema.dim_date;
DESC TABLE sales_schema.dim_product;
DESC TABLE sales_schema.dim_region;


-- Check Data in Tables

SELECT * FROM sales_schema.fact_sales LIMIT 5;
SELECT * FROM sales_schema.dim_store LIMIT 5;
SELECT * FROM sales_schema.dim_date LIMIT 5;
SELECT * FROM sales_schema.dim_product LIMIT 5;
SELECT * FROM sales_schema.dim_region LIMIT 5;



