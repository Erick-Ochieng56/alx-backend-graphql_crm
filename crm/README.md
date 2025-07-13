# CRM System with Celery Integration

This CRM system includes automated task scheduling using both django-crontab and Celery with Redis as the message broker.

## Prerequisites

- Python 3.8+
- Django 5.2.3
- Redis server
- PostgreSQL or SQLite (SQLite is used by default)

## Setup Instructions

### 1. Install Redis and Dependencies

#### Install Redis (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### Install Redis (macOS):
```bash
brew install redis
brew services start redis
```

#### Install Redis (Windows):
Download and install Redis from the official website or use Docker:
```bash
docker run -d -p 6379:6379 redis:latest
```

#### Install Python Dependencies:
```bash
pip install -r requirements.txt
```

### 2. Database Setup

Run Django migrations to set up the database:
```bash
python manage.py migrate
```

Create a superuser (optional):
```bash
python manage.py createsuperuser
```

Seed the database with sample data:
```bash
python seed_db.py
```

### 3. Start the Django Development Server

```bash
python manage.py runserver
```

The GraphQL endpoint will be available at: `http://localhost:8000/graphql`

### 4. Start Celery Worker

In a new terminal window, start the Celery worker:
```bash
celery -A crm worker -l info
```

### 5. Start Celery Beat (Scheduler)

In another terminal window, start Celery Beat for periodic tasks:
```bash
celery -A crm beat -l info
```

### 6. Configure django-crontab (Optional)

To set up system cron jobs for django-crontab:
```bash
python manage.py crontab add
```

To remove cron jobs:
```bash
python manage.py crontab remove
```

## Scheduled Tasks

### Django-Crontab Tasks:
- **Heartbeat Logging**: Every 5 minutes → `/tmp/crm_heartbeat_log.txt`
- **Low Stock Updates**: Every 12 hours → `/tmp/low_stock_updates_log.txt`

### Celery Tasks:
- **CRM Report Generation**: Every Monday at 6:00 AM → `/tmp/crm_report_log.txt`

### Custom Scripts:
- **Customer Cleanup**: Weekly (Sunday 2:00 AM) → `/tmp/customer_cleanup_log.txt`
- **Order Reminders**: Daily (8:00 AM) → `/tmp/order_reminders_log.txt`

## Log Files

All automated tasks log their activities to files in `/tmp/`:

- `/tmp/crm_heartbeat_log.txt` - System health checks
- `/tmp/low_stock_updates_log.txt` - Product stock updates
- `/tmp/crm_report_log.txt` - Weekly CRM reports
- `/tmp/customer_cleanup_log.txt` - Customer cleanup operations
- `/tmp/order_reminders_log.txt` - Order reminder notifications

## Verify Setup

### Check Redis Connection:
```bash
redis-cli ping
```
Should return `PONG`

### Check Celery Tasks:
```bash
celery -A crm inspect active
```

### Check CRM Report Logs:
```bash
tail -f /tmp/crm_report_log.txt
```

### Test GraphQL Endpoint:
Visit `http://localhost:8000/graphql` and run a test query:
```graphql
query {
  hello
  allCustomers {
    edges {
      node {
        id
        name
        email
      }
    }
  }
}
```

## Troubleshooting

1. **Redis Connection Issues**: Ensure Redis is running on `localhost:6379`
2. **Celery Worker Not Starting**: Check that Redis is accessible and all dependencies are installed
3. **Django-Crontab Issues**: Ensure proper permissions and that the Django environment is accessible
4. **GraphQL Endpoint Not Responding**: Verify Django server is running and GraphQL is properly configured

## Manual Task Execution

You can manually execute tasks for testing:

### Run Celery Task:
```bash
python manage.py shell
>>> from crm.tasks import generate_crm_report
>>> generate_crm_report.delay()
```

### Run Cron Functions:
```bash
python manage.py shell
>>> from crm.cron import log_crm_heartbeat, update_low_stock
>>> log_crm_heartbeat()
>>> update_low_stock()
```

## Production Notes

For production deployment:
1. Use a process manager like Supervisor or systemd for Celery workers
2. Configure Redis with persistence and proper security
3. Use environment variables for sensitive settings
4. Set up proper logging and monitoring
5. Consider using a more robust message broker like RabbitMQ for high-volume scenarios
