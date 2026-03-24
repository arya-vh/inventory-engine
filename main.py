import os
import logging
from dotenv import load_dotenv
from loader import load_csv_to_dataframe
from sales_aggregator import aggregate_sales
from inventory_engine import reconcile_inventory
from reporter import generate_csv_report, generate_json_summary
from alerter import send_stock_alert

def setup_logging():
    """Configures the logging for the application."""
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'inventory.log'), mode='w'),
            logging.StreamHandler()
        ]
    )

def main():
    """Main function to run the inventory reconciliation process."""
    setup_logging()
    logging.info("Starting Inventory Reconciliation & Sales Analysis Engine.")

    # Define file paths
    INVENTORY_FILE = os.path.join('data', 'inventory.csv')
    SALES_FILE = os.path.join('data', 'sales_transactions.csv')
    RECONCILIATION_OUTPUT_FILE = 'inventory_reconciliation.csv'
    SUMMARY_OUTPUT_FILE = 'sales_summary.json'

    # 1. Load data
    inventory_df = load_csv_to_dataframe(INVENTORY_FILE)
    sales_df = load_csv_to_dataframe(SALES_FILE)

    if inventory_df is None or sales_df is None:
        logging.error("Halting execution due to file loading errors.")
        return

    # 2. Aggregate sales
    inventory_product_ids = set(inventory_df['product_id'])
    aggregated_sales, processed_transactions_count = aggregate_sales(sales_df, inventory_product_ids)

    # 3. Reconcile inventory
    reconciled_inventory_df = reconcile_inventory(inventory_df, aggregated_sales)

    # 4. Generate reports
    reconciliation_columns = [
        'product_id', 'product_name', 'category', 'current_stock',
        'total_sold_quantity', 'final_stock', 'stock_status', 'total_sales_value'
    ]
    generate_csv_report(reconciled_inventory_df, reconciliation_columns, RECONCILIATION_OUTPUT_FILE)
    generate_json_summary(reconciled_inventory_df, processed_transactions_count, SUMMARY_OUTPUT_FILE)

    # 5. Send Stock Alert
    load_dotenv()
    sender = os.getenv("SENDER_EMAIL")
    receiver = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    if sender and receiver and password:
        send_stock_alert(reconciled_inventory_df, sender, receiver, password)
    else:
        logging.warning("Skipping email alert: Missing environment variables.")

    logging.info("Process completed successfully.")

if __name__ == "__main__":
    main()