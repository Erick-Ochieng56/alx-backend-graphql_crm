#!/bin/bash

# Customer cleanup script - removes customers with no orders in the past year
# Script path: crm/cron_jobs/clean_inactive_customers.sh

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate to the Django project root (two levels up from cron_jobs)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Check if we can change to project directory
if cd "$PROJECT_ROOT"; then
    echo "Changed to project directory: $(pwd)"
else
    echo "Error: Could not change to project directory: $PROJECT_ROOT"
    exit 1
fi

# Store current working directory
cwd="$(pwd)"

# Execute Django shell command to delete inactive customers
DELETED_COUNT=$(python manage.py shell << 'EOF'
import django
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

# Calculate date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# Find customers with no orders in the past year
inactive_customers = Customer.objects.filter(
    orders__isnull=True
) | Customer.objects.exclude(
    orders__order_date__gte=one_year_ago
).distinct()

# Count and delete inactive customers
count = inactive_customers.count()
inactive_customers.delete()

print(count)
EOF
)

# Log the cleanup results with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TIMESTAMP] Customer cleanup completed. Deleted $DELETED_COUNT inactive customers." >> /tmp/customer_cleanup_log.txt
