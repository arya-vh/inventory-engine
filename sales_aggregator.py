import pandas as pd
import logging

def aggregate_sales(sales_df: pd.DataFrame, inventory_product_ids: set) -> tuple[pd.Series, int]:
    """
    Filters, cleans, and aggregates sales data.

    Args:
        sales_df (pd.DataFrame): DataFrame of sales transactions.
        inventory_product_ids (set): A set of valid product IDs from the inventory.

    Returns:
        tuple[pd.Series, int]: A tuple containing:
            - A pandas Series with aggregated sales per product_id.
            - An integer count of processed (valid) transactions.
    """
    # Make a copy to avoid SettingWithCopyWarning
    df = sales_df.copy()

    # --- Data Cleaning and Filtering ---

    # Negative quantities
    negative_quantity_mask = df['quantity_sold'] < 0
    if negative_quantity_mask.any():
        invalid_tx_ids = df[negative_quantity_mask]['transaction_id'].tolist()
        logging.warning(f"Ignoring transactions with negative quantity: {invalid_tx_ids}")
        df = df[~negative_quantity_mask]

    # Invalid dates
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    invalid_date_mask = df['transaction_date'].isna()
    if invalid_date_mask.any():
        invalid_tx_ids = df[invalid_date_mask]['transaction_id'].tolist()
        logging.warning(f"Ignoring transactions with invalid date format: {invalid_tx_ids}")
        df = df[~invalid_date_mask]

    # Filter for April 2024
    df = df[(df['transaction_date'].dt.year == 2024) & (df['transaction_date'].dt.month == 4)]

    # Unknown product IDs
    unknown_product_mask = ~df['product_id'].isin(inventory_product_ids)
    if unknown_product_mask.any():
        unknown_product_ids = df[unknown_product_mask]['product_id'].unique().tolist()
        logging.warning(f"Ignoring transactions with unknown product IDs: {unknown_product_ids}")
        df = df[~unknown_product_mask]

    processed_transactions_count = len(df)
    logging.info(f"Total valid transactions processed: {processed_transactions_count}")

    # --- Aggregation ---
    aggregated_sales = df.groupby('product_id')['quantity_sold'].sum()
    aggregated_sales.name = 'total_sold_quantity'

    return aggregated_sales, processed_transactions_count