import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
import os

def connect_snowflake():
    """
    Establishes a connection to Snowflake.
    :return: Snowflake connection object, cursor object
    """
    conn = snowflake.connector.connect(
        user="BINITAROY",
        password="Binita13225290/",
        account="iupzzwu-rh32299",
        warehouse="COMPUTE_WH",
        database="walmart_sales_db",
        schema="sales_schema"
    )
    cur = conn.cursor()
    print("✅ Connected to Snowflake!")
    return conn, cur

def load_data_to_snowflake(conn, cur, df):
    """
    Loads the transformed data into Snowflake.
    """
    # Explicitly set the correct database and schema
    cur.execute("USE DATABASE walmart_sales_db;")
    cur.execute("USE SCHEMA sales_schema;")

    # Ensure table exists
    cur.execute("SHOW TABLES LIKE 'WEEKLY_SALES' IN SCHEMA SALES_SCHEMA;")
    table_exists = cur.fetchall()
    if not table_exists:
        raise Exception("❌ Table does not exist in Snowflake. Aborting data load.")

    # Ensure column names are uppercase before inserting
    df.columns = df.columns.str.upper()

    # Load data using write_pandas
    success, nchunks, nrows, _ = write_pandas(conn, df, "WEEKLY_SALES", schema="SALES_SCHEMA")

    if success:
        print(f"✅ Data Loaded Successfully! Rows Inserted: {nrows}")
    else:
        raise Exception("❌ Data load failed. Check schema and table structure.")

if __name__ == "__main__":
    data_dir = "F:\\Portfolio Projects\\walmart_etl_project\\data"
    transformed_file_path = os.path.join(data_dir, "Walmart_Store_sales_transformed.csv")  # Read transformed file

    # Load the transformed dataset
    df_transformed = pd.read_csv(transformed_file_path)

    conn, cur = connect_snowflake()
    load_data_to_snowflake(conn, cur, df_transformed)
    
    print("✅ Snowflake setup and data loading complete!")
