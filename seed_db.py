import os
import django
import random
from decimal import Decimal
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order

def seed_customers():
    customers_data = [
        {"name": "Alice Johnson", "email": "alice@example.com", "phone": "+1234567890"},
        {"name": "Bob Smith", "email": "bob@example.com", "phone": "123-456-7890"},
        {"name": "Carol Brown", "email": "carol@example.com", "phone": None},
        {"name": "David Lee", "email": "david@example.com", "phone": "+9876543210"},
    ]

    customers = []
    for data in customers_data:
        customer, _ = Customer.objects.get_or_create(**data)
        customers.append(customer)
    print(f"Seeded {len(customers)} customers.")


def seed_products():
    products_data = [
        {"name": "Laptop", "price": Decimal("999.99"), "stock": 10},
        {"name": "Smartphone", "price": Decimal("499.99"), "stock": 25},
        {"name": "Headphones", "price": Decimal("79.99"), "stock": 50},
        {"name": "Mouse", "price": Decimal("29.99"), "stock": 100},
    ]

    products = []
    for data in products_data:
        product, _ = Product.objects.get_or_create(**data)
        products.append(product)
    print(f"Seeded {len(products)} products.")


def seed_orders():
    customers = list(Customer.objects.all())
    products = list(Product.objects.all())

    if not customers or not products:
        print("Skipping orders — make sure customers and products are seeded first.")
        return

    for i in range(3):
        customer = random.choice(customers)
        order = Order.objects.create(customer=customer)
        selected_products = random.sample(products, k=random.randint(1, 3))
        order.products.set(selected_products)
        order.calculate_total()
        print(f"Created Order #{order.id} for {customer.name} with {len(selected_products)} products.")


if __name__ == "__main__":
    print("Starting database seeding...")
    seed_customers()
    seed_products()
    seed_orders()
    print("Done seeding the CRM database!")
