import pandas as pd
from sales_aggregator import aggregate_sales

def test_multiple_sales_aggregation():
    """Tests if sales for the same product are aggregated correctly."""
    sales_data = {
        'transaction_id': ['T1', 'T2', 'T3'],
        'product_id': ['P1', 'P1', 'P2'],
        'transaction_date': ['2024-04-05', '2024-04-06', '2024-04-05'],
        'quantity_sold': [10, 5, 8]
    }
    sales_df = pd.DataFrame(sales_data)
    inventory_ids = {'P1', 'P2'}
    
    agg_sales, _ = aggregate_sales(sales_df, inventory_ids)
    
    assert agg_sales.loc['P1'] == 15
    assert agg_sales.loc['P2'] == 8

def test_invalid_transaction_date():
    """Tests that transactions with invalid dates are ignored."""
    sales_data = {
        'transaction_id': ['T1', 'T2', 'T3'],
        'product_id': ['P1', 'P1', 'P2'],
        'transaction_date': ['2024-04-05', 'invalid-date', '2024-04-07'],
        'quantity_sold': [10, 5, 8]
    }
    sales_df = pd.DataFrame(sales_data)
    inventory_ids = {'P1', 'P2'}
    
    agg_sales, processed_count = aggregate_sales(sales_df, inventory_ids)
    
    assert agg_sales.loc['P1'] == 10 # Only T1 is valid for P1
    assert processed_count == 2

def test_negative_quantity_ignored():
    """Tests that transactions with negative quantities are ignored."""
    sales_data = {
        'transaction_id': ['T1', 'T2', 'T3'],
        'product_id': ['P1', 'P1', 'P2'],
        'transaction_date': ['2024-04-05', '2024-04-06', '2024-04-07'],
        'quantity_sold': [10, -5, 8]
    }
    sales_df = pd.DataFrame(sales_data)
    inventory_ids = {'P1', 'P2'}
    
    agg_sales, processed_count = aggregate_sales(sales_df, inventory_ids)
    
    assert agg_sales.loc['P1'] == 10
    assert processed_count == 2

def test_unknown_product_id_ignored():
    """Tests that transactions with product_id not in inventory are ignored."""
    sales_data = {
        'transaction_id': ['T1', 'T2'],
        'product_id': ['P1', 'P99'], # P99 is not in inventory
        'transaction_date': ['2024-04-05', '2024-04-06'],
        'quantity_sold': [10, 5]
    }
    sales_df = pd.DataFrame(sales_data)
    inventory_ids = {'P1'}
    
    agg_sales, processed_count = aggregate_sales(sales_df, inventory_ids)
    
    assert 'P99' not in agg_sales.index
    assert len(agg_sales) == 1
    assert processed_count == 1

def test_date_outside_april_2024_ignored():
    """Tests that transactions outside of April 2024 are ignored."""
    sales_data = {
        'transaction_id': ['T1', 'T2', 'T3'],
        'product_id': ['P1', 'P1', 'P1'],
        'transaction_date': ['2024-04-05', '2024-05-01', '2023-04-10'],
        'quantity_sold': [10, 5, 8]
    }
    sales_df = pd.DataFrame(sales_data)
    inventory_ids = {'P1'}
    
    agg_sales, processed_count = aggregate_sales(sales_df, inventory_ids)
    
    assert agg_sales.loc['P1'] == 10
    assert processed_count == 1