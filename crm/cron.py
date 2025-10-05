from datetime import datetime

def log_crm_heartbeat():
    """Logs a heartbeat message for the CRM system."""
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"
    with open("/tmp/crm_heartbeat_log.txt", "a") as file:
        file.write(message)
