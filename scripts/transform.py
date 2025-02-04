import pandas as pd
import os

def transform_data(file_path, save_path):
    """
    Cleans and transforms the data for Snowflake compatibility.
    :param file_path: str - Path to the raw dataset
    :param save_path: str - Path to save the transformed dataset
    :return: pandas DataFrame - Transformed dataset
    """
    df = pd.read_csv(file_path)
    
    # Rename columns to match Snowflake schema (UPPERCASE)
    df.rename(columns={
        "Store": "STORE_ID",
        "Date": "SALES_DATE",
        "Weekly_Sales": "WEEKLY_SALES",
        "Holiday_Flag": "IS_HOLIDAY",
        "Temperature": "TEMPERATURE",
        "Fuel_Price": "FUEL_PRICE",
        "CPI": "CPI",
        "Unemployment": "UNEMPLOYMENT"
    }, inplace=True)

    # Convert sales_date to datetime format
    df["SALES_DATE"] = pd.to_datetime(df["SALES_DATE"], format="%d-%m-%Y")

    # Ensure correct data types
    df["STORE_ID"] = df["STORE_ID"].astype(int)
    df["IS_HOLIDAY"] = df["IS_HOLIDAY"].astype(bool)

    # Save transformed data to a new file
    df.to_csv(save_path, index=False)
    print(f"✅ Transformed Data Saved to: {save_path}")

    return df

if __name__ == "__main__":
    data_dir = "F:\\Portfolio Projects\\walmart_etl_project\\data"
    raw_file_path = os.path.join(data_dir, "Walmart_Store_sales.csv")
    transformed_file_path = os.path.join(data_dir, "Walmart_Store_sales_transformed.csv")

    df_transformed = transform_data(raw_file_path, transformed_file_path)
    print(df_transformed.head())
