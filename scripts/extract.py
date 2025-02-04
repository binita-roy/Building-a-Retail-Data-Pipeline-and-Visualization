import kagglehub
import pandas as pd
import os
import shutil

def extract_data():
    """
    Downloads dataset from Kaggle API and saves it to the local project directory.
    :return: str - Path to the saved CSV file
    """
    # Define storage path
    data_dir = "F:\\Portfolio Projects\\walmart_etl_project\\data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Download dataset from Kaggle
    dataset_path = kagglehub.dataset_download("rutuspatel/walmart-dataset-retail")
    print("✅ Dataset Downloaded from Kaggle!")

    # List all files in the extracted folder to check the exact filename
    print(f"📂 Checking files in: {dataset_path}")
    files = os.listdir(dataset_path)
    print("📃 Files found:", files)

    # Ensure the expected file is in the folder
    csv_files = [file for file in files if file.endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError("❌ No CSV files found in the downloaded dataset. Check Kaggle dataset structure.")

    # Assume the first CSV file is the required dataset
    source_file_path = os.path.join(dataset_path, csv_files[0])
    destination_file_path = os.path.join(data_dir, "Walmart_Store_sales.csv")

    # Move file to project data directory
    shutil.move(source_file_path, destination_file_path)
    print(f"✅ Data Saved to: {destination_file_path}")

    return destination_file_path

if __name__ == "__main__":
    file_path = extract_data()
    df = pd.read_csv(file_path)
    print(df.head())
