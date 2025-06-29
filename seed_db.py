# seed_db.py
import os
import django
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order

def seed_database():
    """Seed the database with sample data"""
    
    # Create sample customers
    customers_data = [
        {'name': 'Alice Johnson', 'email': 'alice@example.com', 'phone': '+1234567890'},
        {'name': 'Bob Smith', 'email': 'bob@example.com', 'phone': '123-456-7890'},
        {'name': 'Carol Williams', 'email': 'carol@example.com', 'phone': '(555) 123-4567'},
        {'name': 'David Brown', 'email': 'david@example.com'},
        {'name': 'Eve Davis', 'email': 'eve@example.com', 'phone': '+9876543210'},
    ]
    
    customers = []
    for customer_data in customers_data:
        customer, created = Customer.objects.get_or_create(
            email=customer_data['email'],
            defaults=customer_data
        )
        customers.append(customer)
        if created:
            print(f"Created customer: {customer.name}")
    
    # Create sample products
    products_data = [
        {'name': 'Laptop', 'price': Decimal('999.99'), 'stock': 10},
        {'name': 'Smartphone', 'price': Decimal('599.99'), 'stock': 25},
        {'name': 'Tablet', 'price': Decimal('299.99'), 'stock': 15},
        {'name': 'Headphones', 'price': Decimal('199.99'), 'stock': 50},
        {'name': 'Monitor', 'price': Decimal('349.99'), 'stock': 8},
        {'name': 'Keyboard', 'price': Decimal('79.99'), 'stock': 30},
        {'name': 'Mouse', 'price': Decimal('39.99'), 'stock': 45},
    ]
    
    products = []
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        products.append(product)
        if created:
            print(f"Created product: {product.name}")
    
    # Create sample orders
    orders_data = [
        {'customer_index': 0, 'product_indices': [0, 3]},  # Alice: Laptop + Headphones
        {'customer_index': 1, 'product_indices': [1]},     # Bob: Smartphone
        {'customer_index': 2, 'product_indices': [2, 5, 6]}, # Carol: Tablet + Keyboard + Mouse
        {'customer_index': 3, 'product_indices': [4, 5]},  # David: Monitor + Keyboard
        {'customer_index': 4, 'product_indices': [1, 3]},  # Eve: Smartphone + Headphones
    ]
    
    for order_data in orders_data:
        customer = customers[order_data['customer_index']]
        order_products = [products[i] for i in order_data['product_indices']]
        
        # Check if order already exists for this customer with same products
        existing_order = Order.objects.filter(customer=customer).first()
        if not existing_order:
            order = Order.objects.create(customer=customer)
            order.products.set(order_products)
            
            # Calculate total amount
            total = sum(product.price for product in order_products)
            order.total_amount = total
            order.save()
            
            print(f"Created order for {customer.name}: {[p.name for p in order_products]}")

if __name__ == '__main__':
    print("Seeding database...")
    seed_database()
    print("Database seeded successfully!")