import pandas as pd
import logging

def get_stock_status(stock: int) -> str:
    """Determines the stock status based on stock level."""
    if stock == 0:
        return "OUT_OF_STOCK"
    elif 1 <= stock <= 10:
        return "LOW_STOCK"
    else:
        return "AVAILABLE"

def reconcile_inventory(inventory_df: pd.DataFrame, aggregated_sales: pd.Series) -> pd.DataFrame:
    """
    Reconciles inventory levels based on aggregated sales data.

    Args:
        inventory_df (pd.DataFrame): The current inventory DataFrame.
        aggregated_sales (pd.Series): Aggregated sales data with product_id as index.

    Returns:
        pd.DataFrame: The reconciled inventory DataFrame with new calculated fields.
    """
    # Merge sales data with inventory
    df = inventory_df.merge(aggregated_sales, on='product_id', how='left')

    # Fill products with no sales with 0
    df['total_sold_quantity'] = df['total_sold_quantity'].fillna(0).astype(int)

    # Calculate final stock
    df['final_stock'] = df['current_stock'] - df['total_sold_quantity']

    # Handle stock errors (final_stock < 0)
    stock_error_mask = df['final_stock'] < 0
    if stock_error_mask.any():
        error_products = df[stock_error_mask]['product_id'].tolist()
        logging.error(f"Stock error: Final stock is negative for products {error_products}. Setting to 0.")
        df.loc[stock_error_mask, 'final_stock'] = 0

    # Determine stock status
    df['stock_status'] = df['final_stock'].apply(get_stock_status)

    # Calculate total sales value
    df['total_sales_value'] = df['total_sold_quantity'] * df['unit_price']

    logging.info("Inventory reconciliation complete.")
    return df