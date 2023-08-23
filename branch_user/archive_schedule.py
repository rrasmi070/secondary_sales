from doctest import master
from apscheduler.schedulers.background import BackgroundScheduler
from .views import Schedule_Archcrive

def start():
  scheduler = BackgroundScheduler()
  master = Schedule_Archcrive()
  scheduler.add_job(master.get_queryset, "interval", minutes=10)
  # scheduler.start()