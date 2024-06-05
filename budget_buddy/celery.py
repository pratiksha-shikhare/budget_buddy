# from __future__ import absolute_import, unicode_literals
# import os
# from celery.schedules import crontab
# from celery import Celery

# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_buddy.settings')

# app = Celery('budget_buddy')

# # Using a string here means the worker will not have to serialize
# # the configuration object to child processes.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()


from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_buddy.settings')

app = Celery('budget_buddy')

# Using a string here means the worker will not have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure Celery to use Redis as the message broker
app.conf.broker_url = 'redis://localhost:6379/0'

app.conf.beat_schedule = {
    'initiate_payment': {
        'task': 'expenses.tasks.send_email_task',
        'schedule': crontab(hour=21, minute=00)
    }
}
