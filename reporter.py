import pandas as pd
import json
import logging

def generate_csv_report(df: pd.DataFrame, columns: list, file_path: str):
    """
    Generates and saves a CSV report from a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to report.
        columns (list): The list of columns to include in the report.
        file_path (str): The path to save the CSV file.
    """
    try:
        df[columns].to_csv(file_path, index=False)
        logging.info(f"Successfully generated CSV report at {file_path}")
    except Exception as e:
        logging.error(f"Failed to generate CSV report: {e}")

def generate_json_summary(df: pd.DataFrame, processed_transactions_count: int, file_path: str):
    """
    Generates and saves a JSON summary report.

    Args:
        df (pd.DataFrame): The reconciled inventory DataFrame.
        processed_transactions_count (int): The count of valid transactions.
        file_path (str): The path to save the JSON file.
    """
    try:
        total_sales_value = df['total_sales_value'].sum()
        low_stock_products = df[df['stock_status'] == 'LOW_STOCK']['product_id'].tolist()
        out_of_stock_products = df[df['stock_status'] == 'OUT_OF_STOCK']['product_id'].tolist()

        summary = {
            "total_products": len(df),
            "total_transactions_processed": processed_transactions_count,
            "total_sales_value": float(total_sales_value),
            "low_stock_products": low_stock_products,
            "out_of_stock_products": out_of_stock_products
        }

        with open(file_path, 'w') as f:
            json.dump(summary, f, indent=4)
        
        logging.info(f"Successfully generated JSON summary at {file_path}")
    except Exception as e:
        logging.error(f"Failed to generate JSON summary: {e}")