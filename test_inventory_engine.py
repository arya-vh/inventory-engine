import pandas as pd
import pytest
from inventory_engine import reconcile_inventory

@pytest.fixture
def sample_inventory():
    """Fixture for sample inventory data."""
    inventory_data = {
        'product_id': ['P1', 'P2', 'P3', 'P4'],
        'product_name': ['A', 'B', 'C', 'D'],
        'current_stock': [100, 15, 5, 50],
        'unit_price': [10, 20, 30, 40],
        'category': ['Cat1', 'Cat1', 'Cat2', 'Cat2']
    }
    return pd.DataFrame(inventory_data)

@pytest.fixture
def sample_aggregated_sales():
    """Fixture for sample aggregated sales data."""
    sales_data = {
        'product_id': ['P1', 'P2', 'P3'],
        'total_sold_quantity': [20, 10, 10]
    }
    return pd.DataFrame(sales_data).set_index('product_id')['total_sold_quantity']

def test_inventory_reduction(sample_inventory, sample_aggregated_sales):
    """Tests that final_stock is calculated correctly."""
    reconciled_df = reconcile_inventory(sample_inventory, sample_aggregated_sales)
    
    # P1: 100 - 20 = 80
    assert reconciled_df.loc[reconciled_df['product_id'] == 'P1', 'final_stock'].iloc[0] == 80
    # P4: 50 - 0 = 50 (no sales)
    assert reconciled_df.loc[reconciled_df['product_id'] == 'P4', 'final_stock'].iloc[0] == 50

def test_inventory_not_negative(sample_inventory, sample_aggregated_sales):
    """Tests that final_stock is floored at 0 and not negative."""
    reconciled_df = reconcile_inventory(sample_inventory, sample_aggregated_sales)
    
    # P3: 5 - 10 = -5, should be 0
    assert reconciled_df.loc[reconciled_df['product_id'] == 'P3', 'final_stock'].iloc[0] == 0

def test_zero_stock_status(sample_inventory, sample_aggregated_sales):
    """Tests that stock status is OUT_OF_STOCK for zero stock."""
    # This test case is covered by test_out_of_stock_status, but implemented as requested.
    # P3's final stock will be 0.
    reconciled_df = reconcile_inventory(sample_inventory, sample_aggregated_sales)
    assert reconciled_df.loc[reconciled_df['product_id'] == 'P3', 'stock_status'].iloc[0] == 'OUT_OF_STOCK'

def test_available_status(sample_inventory, sample_aggregated_sales):
    """Tests that stock status is AVAILABLE for stock > 10."""
    reconciled_df = reconcile_inventory(sample_inventory, sample_aggregated_sales)
    
    # P1: final_stock is 80
    assert reconciled_df.loc[reconciled_df['product_id'] == 'P1', 'stock_status'].iloc[0] == 'AVAILABLE'

def test_low_stock_status(sample_inventory, sample_aggregated_sales):
    """Tests that stock status is LOW_STOCK for stock between 1 and 10."""
    reconciled_df = reconcile_inventory(sample_inventory, sample_aggregated_sales)
    
    # P2: 15 - 10 = 5
    assert reconciled_df.loc[reconciled_df['product_id'] == 'P2', 'stock_status'].iloc[0] == 'LOW_STOCK'

def test_out_of_stock_status(sample_inventory, sample_aggregated_sales):
    """Tests that stock status is OUT_OF_STOCK for zero or negative calculated stock."""
    reconciled_df = reconcile_inventory(sample_inventory, sample_aggregated_sales)
    
    # P3: 5 - 10 = -5 -> final_stock 0
    assert reconciled_df.loc[reconciled_df['product_id'] == 'P3', 'stock_status'].iloc[0] == 'OUT_OF_STOCK'

def test_total_sales_value_calculation(sample_inventory, sample_aggregated_sales):
    """Tests the calculation of total_sales_value."""
    reconciled_df = reconcile_inventory(sample_inventory, sample_aggregated_sales)
    
    # P1: 20 sold * 10 unit_price = 200
    assert reconciled_df.loc[reconciled_df['product_id'] == 'P1', 'total_sales_value'].iloc[0] == 200
    # P4: 0 sold * 40 unit_price = 0
    assert reconciled_df.loc[reconciled_df['product_id'] == 'P4', 'total_sales_value'].iloc[0] == 0