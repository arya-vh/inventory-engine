# 📦 Inventory Reconciliation & Sales Analysis Engine

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Latest-green?style=flat-square&logo=pandas)
![Pytest](https://img.shields.io/badge/Pytest-Passing-brightgreen?style=flat-square&logo=pytest)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

A Python-based inventory reconciliation system for e-commerce operations. Processes raw inventory and sales transaction data, applies business rules, detects stock issues, and generates detailed reports — all with full unit test coverage.

---

## Project Structure

```
project/
├── data/
│   ├── inventory.csv              # Master product inventory
│   └── sales_transactions.csv    # Daily sales transactions
│
├── main.py                       # Entry point
├── loader.py                     # CSV file loader
├── sales_aggregator.py           # Sales filtering & aggregation
├── inventory_engine.py           # Stock reconciliation logic
├── reporter.py                   # CSV & JSON report generator
├── alerter.py                    # Email alert system
│
├── tests/
│   ├── test_sales_aggregator.py  # Sales aggregation unit tests
│   └── test_inventory_engine.py  # Inventory engine unit tests
│
├── logs/
│   └── inventory.log             # Auto-generated execution logs
│
├── inventory_reconciliation.csv  # Output: Reconciled inventory
├── sales_summary.json            # Output: Sales summary
├── .env                          # Email configuration
├── requirements.txt
└── README.md
```

---

## Business Rules

### Sales Filtering
| Rule | Action |
|---|---|
| Only April 2024 transactions | All others ignored |
| Invalid/unparseable dates | Skipped + logged |
| Negative `quantity_sold` | Skipped + logged |
| Unknown `product_id` | Skipped + logged |

### Stock Status Classification
| Final Stock | Status |
|---|---|
| `0` | `OUT_OF_STOCK` |
| `1 – 10` | `LOW_STOCK` |
| `> 10` | `AVAILABLE` |

### Key Calculations
```
final_stock       = current_stock - total_sold_quantity
total_sales_value = total_sold_quantity × unit_price
```
> If `final_stock < 0` → set to `0` and log `STOCK_ERROR`

---

## Getting Started

### Prerequisites
- Python 3.9+
- pip

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/inventory-reconciliation.git
cd inventory-reconciliation
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Data Files
Place your CSV files in the `data/` folder:
```
data/inventory.csv
data/sales_transactions.csv
```

---

## Running the Application

```bash
python main.py
```

### Expected Terminal Output
```
INFO - Starting Inventory Reconciliation & Sales Analysis Engine
INFO - Successfully loaded data from data\inventory.csv
INFO - Successfully loaded data from data\sales_transactions.csv
WARNING - Ignoring transactions with negative quantity: ['T033']
WARNING - Ignoring transactions with invalid date format: ['T031']
WARNING - Ignoring transactions with unknown product IDs: ['P999']
INFO - Total valid transactions processed: 30
INFO - Inventory reconciliation complete.
INFO - Successfully generated CSV report at inventory_reconciliation.csv
INFO - Successfully generated JSON summary at sales_summary.json
INFO - Process completed successfully.
```

### Generated Output Files
| File | Description |
|---|---|
| `inventory_reconciliation.csv` | Full reconciled inventory with stock status |
| `sales_summary.json` | High-level sales & stock metrics |
| `logs/inventory.log` | Detailed execution logs |

---

## 📊 Output Format

### inventory_reconciliation.csv
```
product_id | product_name | category | current_stock | 
total_sold_quantity | final_stock | stock_status | total_sales_value
```

### sales_summary.json
```json
{
    "total_products": 10,
    "total_transactions_processed": 30,
    "total_sales_value": 3589.48,
    "low_stock_products": ["P002"],
    "out_of_stock_products": ["P003", "P005"]
}
```

---

## Running Tests

```bash
# Run all tests
pytest test_sales_aggregator.py test_inventory_engine.py -v

# Run with coverage report
pytest test_sales_aggregator.py test_inventory_engine.py -v --cov=src --cov-report=term-missing
```

### Test Coverage
| Test File | Tests | Status |
|---|---|---|
| `test_sales_aggregator.py` | 5 tests | Passing |
| `test_inventory_engine.py` | 7 tests | Passing |
| **Total** | **12 tests** | **12/12 Passing** |

### Test Cases
**Sales Aggregation Tests**
- `test_multiple_sales_aggregation`
- `test_invalid_transaction_date`
- `test_negative_quantity_ignored`
- `test_unknown_product_id_ignored`
- `test_date_outside_april_2024_ignored`

**Inventory Calculation Tests**
- `test_inventory_reduction`
- `test_inventory_not_negative`
- `test_total_sales_value_calculation`

**Stock Status Tests**
- `test_zero_stock_status`
- `test_available_status`
- `test_low_stock_status`
- `test_out_of_stock_status`

---

## Bonus: Streamlit Dashboard

An interactive dashboard to visualize reconciliation results.

```bash
pip install streamlit
streamlit run dashboard.py
```
Opens at `http://localhost:8501`

---

## Input Data Format

### inventory.csv
| Column | Type | Description |
|---|---|---|
| `product_id` | string | Unique product identifier |
| `product_name` | string | Product name |
| `current_stock` | int | Current stock quantity |
| `unit_price` | float | Price per unit |
| `category` | string | Product category |

### sales_transactions.csv
| Column | Type | Description |
|---|---|---|
| `transaction_id` | string | Unique transaction ID |
| `product_id` | string | Product reference |
| `transaction_date` | date | Date of transaction |
| `quantity_sold` | int | Units sold |

---

## Assumptions & Edge Cases

- **No Sales for a Product** → `total_sold_quantity = 0`, stock unchanged
- **Overselling** → `final_stock` floored at `0`, STOCK_ERROR logged
- **Invalid Dates** → Row skipped, transaction ID logged
- **Negative Quantities** → Row skipped, transaction ID logged
- **Unknown Product IDs** → Row skipped, product ID logged
- **Memory** → Pandas in-memory processing; suitable for standard dataset sizes

---

## Dependencies

```
pandas
pytest
pytest-cov
streamlit
```

Install all:
```bash
pip install -r requirements.txt
```

---

## Author

**Arya Vinayaka Harwadekar**
- GitHub: [@arya-vh](https://github.com/arya-vh)
- Email: aryavh04@gmail.com

---

## License

This project is open source and available under the [MIT License](LICENSE).
