# crm/cron.py
import os
import django
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

def log_crm_heartbeat():
    """Log heartbeat message every 5 minutes to confirm CRM health"""
    
    # Format timestamp as DD/MM/YYYY-HH:MM:SS
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    
    # Basic heartbeat message
    heartbeat_msg = f"{timestamp} CRM is alive\n"
    
    try:
        # Optional: Query GraphQL hello field to verify endpoint
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        query = gql("""
            query {
                hello
            }
        """)
        
        result = client.execute(query)
        hello_response = result.get('hello', 'No response')
        
        # Enhanced heartbeat with GraphQL response
        heartbeat_msg = f"{timestamp} CRM is alive - GraphQL response: {hello_response}\n"
        
    except Exception as e:
        # Fallback to basic heartbeat if GraphQL fails
        heartbeat_msg = f"{timestamp} CRM is alive - GraphQL check failed: {str(e)}\n"
    
    # Append to log file
    with open('/tmp/crm_heartbeat_log.txt', 'a') as log_file:
        log_file.write(heartbeat_msg)
