from doctest import master
from apscheduler.schedulers.background import BackgroundScheduler
from master.sfa_view import roolover_day_sale
from .views import Schedule_Surya

def start():
  scheduler = BackgroundScheduler()
  master = Schedule_Surya()
  scheduler.add_job(master.get_queryset, 'cron', hour=8, minute=10)
  scheduler.add_job(roolover_day_sale, 'cron', hour=13, minute=12)
  scheduler.start()