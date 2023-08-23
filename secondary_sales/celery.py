from __future__ import absolute_import
from asyncio import tasks
import os

# from pytz import timezone
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secondary_sales.settings')
app = Celery('secondary_sales',backend='amqp',broker='redis://localhost:6379/')
app.conf.enable_utc = False


# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

app.conf.beat_schedule = {
    'SFA-API-9_30-AM':{
        'task' : 'master.task.Sfa_api',
        # 'schedule': crontab(hour= 9, minute = 29),
        'schedule': crontab(hour= 10, minute = 4)
        # 'schedule': crontab(hour=0, minute=46, day_of_month=19, month_of_year = 6),
        #'args': (2,)

    },
    'SURYA-API-9_30-AM':{
        'task' : 'master.task.Surya_api',
        # 'schedule': crontab(hour= 9, minute=31),
        'schedule': crontab(hour=10, minute=46)
        # 'schedule': crontab(hour=0, minute=46, day_of_month=19, month_of_year = 6),
        #'args': (2,)

    }
}
app.config_from_object(settings, namespace = 'CELERY')
app.conf.update(timezone = 'Asia/Kolkata')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))