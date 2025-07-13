# crm/tasks.py
from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Order

@shared_task
def generate_crm_report():
    """Generate weekly CRM report with customer, order, and revenue statistics"""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # Using Django ORM for direct database queries (more reliable than GraphQL for this task)
        total_customers = Customer.objects.count()
        total_orders = Order.objects.count()
        total_revenue = sum(order.total_amount for order in Order.objects.all())
        
        # Alternative: Use GraphQL queries
        try:
            transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
            client = Client(transport=transport, fetch_schema_from_transport=True)
            
            # Query for customers count
            customers_query = gql("""
                query {
                    allCustomers {
                        edges {
                            node {
                                id
                            }
                        }
                    }
                }
            """)
            
            # Query for orders and revenue
            orders_query = gql("""
                query {
                    allOrders {
                        edges {
                            node {
                                id
                                totalAmount
                            }
                        }
                    }
                }
            """)
            
            customers_result = client.execute(customers_query)
            orders_result = client.execute(orders_query)
            
            # Process GraphQL results
            graphql_customers = len(customers_result.get('allCustomers', {}).get('edges', []))
            orders_data = orders_result.get('allOrders', {}).get('edges', [])
            graphql_orders = len(orders_data)
            graphql_revenue = sum(float(order['node']['totalAmount']) for order in orders_data)
            
            # Use GraphQL results if available, otherwise fall back to ORM
            if graphql_customers > 0:
                total_customers = graphql_customers
                total_orders = graphql_orders
                total_revenue = graphql_revenue
                
        except Exception as graphql_error:
            # If GraphQL fails, continue with ORM results
            pass
        
        # Format the report
        report_message = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, ${total_revenue:.2f} revenue"
        
        # Log to file
        with open('/tmp/crm_report_log.txt', 'a') as log_file:
            log_file.write(report_message + '\n')
            
        return {
            'timestamp': timestamp,
            'customers': total_customers,
            'orders': total_orders,
            'revenue': float(total_revenue),
            'message': 'Report generated successfully'
        }
        
    except Exception as e:
        error_message = f"{timestamp} - Error generating CRM report: {str(e)}"
        
        with open('/tmp/crm_report_log.txt', 'a') as log_file:
            log_file.write(error_message + '\n')
            
        return {
            'timestamp': timestamp,
            'error': str(e),
            'message': 'Report generation failed'
        }
