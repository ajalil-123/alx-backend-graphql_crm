import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    """Logs a heartbeat message every 5 minutes and checks GraphQL health"""
    # Log heartbeat
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{timestamp} CRM is alive\n")

    # Optionally query the GraphQL 'hello' endpoint
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql/",
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("""
            query {
                hello
            }
        """)
        result = client.execute(query)
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"GraphQL hello response: {result.get('hello', 'No response')}\n")
    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"GraphQL check failed: {e}\n")


import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def update_low_stock():
    """Runs every 12 hours to restock low-stock products"""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    try:
        # GraphQL client setup
        transport = RequestsHTTPTransport(
            url="http://127.0.0.1:8000/graphql/",
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # GraphQL mutation
        mutation = gql("""
            mutation {
                updateLowStockProducts {
                    message
                    updatedProducts {
                        name
                        stock
                    }
                }
            }
        """)

        result = client.execute(mutation)
        updates = result.get("updateLowStockProducts", {})

        # Log the result
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"{timestamp} - {updates.get('message')}\n")
            for product in updates.get("updatedProducts", []):
                log_file.write(f"Updated: {product['name']} → {product['stock']}\n")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"{timestamp} - GraphQL error: {e}\n")
