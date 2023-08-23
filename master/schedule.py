from cgi import test
from doctest import master
from apscheduler.schedulers.background import BackgroundScheduler
from master.sfa_view import recent_day_sale, roolover_day_sale
from .views import Schedule,Test_Sch,SFA_API_valid_V2, LogoutallUser

def start():
  scheduler = BackgroundScheduler()
  master = Schedule()
  test_sch = Test_Sch()
  test_sfa = SFA_API_valid_V2()
  logout_scheduler = LogoutallUser()
  scheduler.add_job(logout_scheduler.get_queryset, 'cron', hour = 23, minute=30)
  scheduler.add_job(logout_scheduler.get_queryset, 'cron', hour = 23, minute=31)
  scheduler.add_job(logout_scheduler.get_queryset, 'cron', hour = 23, minute=32)
  scheduler.add_job(logout_scheduler.get_queryset, 'cron', hour = 23, minute=34)
  scheduler.add_job(logout_scheduler.get_queryset, 'cron', hour = 23, minute=35)
  
  # scheduler.add_job(master.get_queryset, "interval", seconds=5)
  scheduler.add_job(test_sfa.get_queryset, 'cron', hour = 10, minute=48)
  # scheduler.add_job(test_sfa.get_queryset, 'cron', hour = 2, minute=13)
  
  # scheduler.add_job(test_sfa.get_queryset, 'cron', hour = 9, minute=10) # prod & UAT=================
  # scheduler.add_job(master.get_queryset, 'cron', hour=9, minute=1) #old one==========================
  scheduler.add_job(test_sch.get_queryset, 'cron', hour=0, minute=27)
  scheduler.add_job(recent_day_sale, 'cron', hour=13, minute=12)
  # scheduler.add_job(roolover_day_sale, 'cron', hour=12, minute=25)
  
  scheduler.start()
  
# def start():
#   scheduler = BackgroundScheduler()
  
#   scheduler.add_job(roolover_day_sale, 'cron', hour=13, minute=3)
#   # scheduler.add_job(roolover_day_sale, 'cron', hour=12, minute=25)
  
#   scheduler.start()