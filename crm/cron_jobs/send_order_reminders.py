#!/usr/bin/env python3

import os
import sys
import django
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

def send_order_reminders():
    """Send order reminders for orders within the last 7 days"""
    
    # Calculate date 7 days ago
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    # GraphQL endpoint
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    # GraphQL query for orders within last 7 days
    query = gql("""
        query GetRecentOrders {
            allOrders {
                edges {
                    node {
                        id
                        orderDate
                        customer {
                            email
                            name
                        }
                        totalAmount
                    }
                }
            }
        }
    """)
    
    try:
        # Execute the query
        result = client.execute(query)
        
        # Process orders
        orders = result.get('allOrders', {}).get('edges', [])
        reminder_count = 0
        
        # Current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Open log file
        with open('/tmp/order_reminders_log.txt', 'a') as log_file:
            for order_edge in orders:
                order = order_edge['node']
                order_date = datetime.fromisoformat(order['orderDate'].replace('Z', '+00:00'))
                
                # Check if order is within last 7 days
                if order_date >= seven_days_ago:
                    log_message = f"[{timestamp}] Order ID: {order['id']}, Customer Email: {order['customer']['email']}, Customer Name: {order['customer']['name']}, Amount: ${order['totalAmount']}\n"
                    log_file.write(log_message)
                    reminder_count += 1
            
            # Log summary
            summary_message = f"[{timestamp}] Processed {reminder_count} order reminders\n"
            log_file.write(summary_message)
        
        print("Order reminders processed!")
        
    except Exception as e:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('/tmp/order_reminders_log.txt', 'a') as log_file:
            log_file.write(f"[{timestamp}] Error processing order reminders: {str(e)}\n")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    send_order_reminders()
