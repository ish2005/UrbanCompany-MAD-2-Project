broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

beat_schedule = {
    'test-every-5-seconds': {
        'task': 'celery_app.test_task',
        'schedule': 5.0,
    },
    'daily-reminders': {
        'task': 'celery_app.send_daily_reminders',
        'schedule': 5.0,  # Run once per day (24 hours * 60 minutes * 60 seconds)
    },
    'monthly-reports': {
        'task': 'celery_app.send_monthly_report',
        'schedule': 5.0,  # Run once per month (30 days * 24 hours * 60 minutes * 60 seconds)
    },
} 