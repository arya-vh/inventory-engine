import smtplib
import ssl
import logging
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_stock_alert(df: pd.DataFrame, sender_email: str, receiver_email: str, password: str):
    """
    Sends an HTML email alert if there are items with low or out of stock status.

    Args:
        df (pd.DataFrame): The reconciled inventory DataFrame.
        sender_email (str): The email address sending the alert.
        receiver_email (str): The email address receiving the alert.
        password (str): The app password for the sender email.
    """
    # 1. Filter for stock issues
    # Change thresholds to match YOUR data
    out_of_stock = df[df['final_stock'] == 0]
    low_stock = df[df['final_stock'] < 100]  # Changed from 10 to 100
    critical_stock = df[df['final_stock'] < 50]

    # 2. Check if alerts are needed
    if out_of_stock.empty and low_stock.empty:
        logging.info("Stock healthy, no alert sent.")
        return

    # 3. Build HTML Content
    html_body = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
            th { background-color: #f4f4f4; }
            .header { color: #333; }
            .out-stock { color: #d32f2f; font-weight: bold; }
            .low-stock { color: #f57c00; font-weight: bold; }
        </style>
    </head>
    <body>
        <h2 class="header">Inventory Stock Alert — Action Required</h2>
        <p>The following products require immediate attention:</p>
    """

    if not out_of_stock.empty:
        html_body += "<h3>🔴 Out of Stock</h3><table><tr><th>Product ID</th><th>Product Name</th><th>Status</th></tr>"
        for _, row in out_of_stock.iterrows():
            html_body += f"<tr><td>{row['product_id']}</td><td>{row['product_name']}</td><td class='out-stock'>OUT_OF_STOCK</td></tr>"
        html_body += "</table>"

    if not low_stock.empty:
        html_body += "<h3>🟠 Low Stock</h3><table><tr><th>Product ID</th><th>Product Name</th><th>Units Remaining</th><th>Status</th></tr>"
        for _, row in low_stock.iterrows():
            html_body += f"<tr><td>{row['product_id']}</td><td>{row['product_name']}</td><td>{row['final_stock']}</td><td class='low-stock'>LOW_STOCK</td></tr>"
        html_body += "</table>"

    html_body += "<p><em>Please restock these items to avoid sales loss.</em></p></body></html>"

    # 4. Email Setup
    message = MIMEMultipart("alternative")
    message["Subject"] = "Inventory Stock Alert — Action Required"
    message["From"] = sender_email
    message["To"] = receiver_email

    part = MIMEText(html_body, "html")
    message.attach(part)

    # 5. Send Email via Gmail SMTP
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        logging.info(f"Stock alert email sent successfully to {receiver_email}")
    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")