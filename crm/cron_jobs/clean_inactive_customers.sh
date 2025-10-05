#!/bin/bash
# Script to delete customers with no orders in the past year and log the count

# Path to virtual environment
VENV_PATH="alx_backend_graphql_crm/venv"

# Activate virtual environment
source "$VENV_PATH/Scripts/activate"

LOG_FILE="crm/cron_jobs/customer_cleanup_crontab.txt"

echo "Starting cleanup at $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"

# Run Django shell command
python manage.py shell -c "
from crm.models import Customer
from datetime import datetime, timedelta

one_year_ago = datetime.now() - timedelta(days=365)

# Find customers with no orders in the past year
inactive_customers = Customer.objects.filter(order__isnull=True)  # or adjust based on your model relation

deleted_count = inactive_customers.count()
inactive_customers.delete()

print(f'Deleted {deleted_count} inactive customers.')
" >> "$LOG_FILE" 2>&1

echo "Cleanup finished at $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"

# Deactivate virtual environment
deactivate
