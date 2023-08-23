from doctest import master
from apscheduler.schedulers.background import BackgroundScheduler
from .views import Schedule_Week_Generate, Schedule_Week_update_code, Create_Update_Weekly_Sales
import datetime
# create weekly scheduler=============================>>
def start():
  scheduler = BackgroundScheduler()
  now_dt = datetime.datetime.now()
  cretae_weekly_sale_datetime  = [
    datetime.datetime(now_dt.date().year, now_dt.date().month, 1, 10, 1),
    datetime.datetime(now_dt.date().year, now_dt.date().month, 8, 10, 1),
    datetime.datetime(now_dt.date().year, now_dt.date().month, 15, 10, 1),
    datetime.datetime(now_dt.date().year, now_dt.date().month, 22, 10, 1),
    #.....on freez update
    datetime.datetime(now_dt.date().year, now_dt.date().month, 2, 23, 30),
    datetime.datetime(now_dt.date().year, now_dt.date().month, 3, 10, 1),
    datetime.datetime(now_dt.date().year, now_dt.date().month, 9, 10, 1),
    datetime.datetime(now_dt.date().year, now_dt.date().month, 10, 10, 1),
    datetime.datetime(now_dt.date().year, now_dt.date().month, 16, 10, 1),
    datetime.datetime(now_dt.date().year, now_dt.date().month, 17, 10, 1),
    datetime.datetime(now_dt.date().year, now_dt.date().month, 23, 10, 1),
    datetime.datetime(now_dt.date().year, now_dt.date().month, 24, 10, 1),
    
    
   
  ]
  master = Create_Update_Weekly_Sales()
  scheduler.add_job(master.get_queryset, 'date', run_date=cretae_weekly_sale_datetime[0]),
  scheduler.add_job(master.get_queryset, 'date', run_date=cretae_weekly_sale_datetime[1]),
  scheduler.add_job(master.get_queryset, 'date', run_date=cretae_weekly_sale_datetime[2]),
  scheduler.add_job(master.get_queryset, 'date', run_date=cretae_weekly_sale_datetime[3]),
  # scheduler.add_job(master.get_queryset, "interval", minutes=1)
  
  update_master = Create_Update_Weekly_Sales()
  scheduler.add_job(update_master.get_queryset, 'date', run_date=cretae_weekly_sale_datetime[4]),
  # scheduler.add_job(update_master.get_queryset, 'date', run_date=cretae_weekly_sale_datetime[5]),
  scheduler.add_job(update_master.get_queryset, 'date', run_date=cretae_weekly_sale_datetime[6]),
  # scheduler.add_job(update_master.get_queryset, 'date', run_date=cretae_weekly_sale_datetime[7]),
  scheduler.add_job(update_master.get_queryset, 'date', run_date=cretae_weekly_sale_datetime[8]),
  # scheduler.add_job(update_master.get_queryset, 'date', run_date=cretae_weekly_sale_datetime[9]),
  scheduler.add_job(update_master.get_queryset, 'date', run_date=cretae_weekly_sale_datetime[10]),
  # scheduler.add_job(update_master.get_queryset, 'date', run_date=cretae_weekly_sale_datetime[11]),

  scheduler.start()