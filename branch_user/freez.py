from apscheduler.schedulers.background import BackgroundScheduler
from .views import Auto_freez

def start():
  scheduler = BackgroundScheduler()
  manager = Auto_freez()
  # scheduler.add_job(manager.get_queryset, "interval", minutes=1)
  scheduler.add_job(manager.get_queryset,"interval", minutes=1)
  #scheduler.start()