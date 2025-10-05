#!/usr/bin/env python

import os
import sys
from datetime import datetime, timedelta

# --- Add project root to sys.path ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

# --- Set Django settings module ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")

import django
django.setup()

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# --- GraphQL client setup ---
transport = RequestsHTTPTransport(
    url="http://127.0.0.1:8000/graphql",
    verify=True,
    retries=3,
)
client = Client(transport=transport, fetch_schema_from_transport=True)

# --- Compute date range for last 7 days ---
today = datetime.today().date()
one_week_ago = today - timedelta(days=7)

# --- GraphQL query using correct filter names ---
query = gql("""
query GetRecentOrders($start: Date, $end: Date) {
  allOrders(filter: {orderDateGte: $start, orderDateLte: $end}) {
    edges {
      node {
        id
        customer {
          email
        }
      }
    }
  }
}
""")

params = {"start": one_week_ago, "end": today}

# --- Log results ---
log_file = os.path.join(os.path.dirname(__file__), "order_reminders_log.txt")

try:
    result = client.execute(query, variable_values=params)
    orders = result["allOrders"]["edges"]

    with open(log_file, "a") as f:
        for order in orders:
            node = order["node"]
            f.write(f"{datetime.now()} | Order ID: {node['id']} | Customer Email: {node['customer']['email']}\n")

    print("Order reminders processed!")

except Exception as e:
    print(f"Error executing GraphQL query: {e}")
