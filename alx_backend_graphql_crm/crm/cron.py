import os
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Logs a heartbeat message to /tmp/crm_heartbeat_log.txt
    Optionally checks GraphQL endpoint.
    """
    log_file = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Optional: Check GraphQL 'hello' query
    try:
        transport = RequestsHTTPTransport(
            url="http://127.0.0.1:8000/graphql/",
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql("""
        query {
            hello
        }
        """)
        result = client.execute(query)
        status = f" | GraphQL hello: {result.get('hello')}"
    except Exception as e:
        status = f" | GraphQL error: {e}"

    with open(log_file, "a") as f:
        f.write(f"{timestamp} CRM is alive{status}\n")
