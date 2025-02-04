import snowflake.connector

conn = snowflake.connector.connect(
    user="BINITAROY",
    password="Binita13225290/",
    account="iupzzwu-rh32299",  # ❌ No .snowflakecomputing.com
    warehouse="COMPUTE_WH",
    database="walmart_sales_db",
    schema="sales_schema"
)

print("✅ Connection Successful!")
conn.close()
