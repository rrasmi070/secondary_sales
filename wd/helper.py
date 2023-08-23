import datetime
import calendar
from unicodedata import category
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from django.db.models import Sum


def week_sele_before_date(user):
    print("===type===",user)
    user_type = user
    now_dt = datetime.datetime.now()
    # now_dt = utils.now_date
    now_day=str(now_dt.date())
    splited = now_day.split('-')
    till_date = datetime.datetime(2009, 10, 5, 15, 00, 00)
    anot_data={}
    
    
    last_date_month = datetime.datetime(now_dt.date().year, now_dt.date().month, calendar.monthrange(now_dt.date().year,now_dt.date().month)[1]).date()
    
    # week_4st1 = [datetime.datetime(now_dt.date().year, now_dt.date().month, 1).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 3).date()]
       
    # =======================================================================================================
    # print(week_3st[0]<= now_dt.date()<= week_3st[0]-datetime.timedelta(days=1),"======pp=====")
    week_1st_gng = [datetime.datetime(now_dt.date().year, now_dt.date().month, 1).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 7).date()]
    week_2nd_gng = [datetime.datetime(now_dt.date().year, now_dt.date().month, 8).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 14).date()]
    week_3rd_gng = [datetime.datetime(now_dt.date().year, now_dt.date().month, 15).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 21).date()]
    last_date_month = datetime.datetime(now_dt.date().year, now_dt.date().month, calendar.monthrange(now_dt.date().year,now_dt.date().month)[1]).date()
    week_4th = [datetime.datetime(now_dt.date().year, now_dt.date().month, 22).date(),last_date_month]
    # week_4_weekly_gng=[week_4th[0] - relativedelta(months=1),now_dt.date().today().replace(day=1) - datetime.timedelta(days=1)]

    #fixed date assigned for week==================
    weekend_dates = (
        datetime.datetime(now_dt.date().year, now_dt.date().month, 7).date(),
        datetime.datetime(now_dt.date().year, now_dt.date().month, 14).date(),
        datetime.datetime(now_dt.date().year, now_dt.date().month, 21).date(),
        last_date_month
    )

    # current week as per reng====
    week_1st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 7).date(),datetime.datetime(now_dt.date().year, now_dt.date().month,10).date()]
    week_2st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 14).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 17).date()]
    week_3st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 21).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 24).date()]
    last_date_month = datetime.datetime(now_dt.date().year, now_dt.date().month, calendar.monthrange(now_dt.date().year,now_dt.date().month)[1]).date()
    week_4st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 1).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 3).date()]
    
    if  week_1st[0] <= now_dt.date() <= week_1st[1] and user_type == "BRANCH USER":
        week_reng =  week_1st
        weekly = "Week1"
        week_rng_val = week_1st_gng
    elif week_2st[0] <= now_dt.date() <= week_2st[1] and user_type == "BRANCH USER":
        week_reng = week_2st
        weekly = "Week2"
        week_rng_val = week_2nd_gng
    elif week_3st[0] <= now_dt.date() <= week_3st[1] and user_type == "BRANCH USER":
        week_reng = week_3st
        weekly = "Week3"
        week_rng_val = week_3rd_gng
    # Week 4 Validation.
    elif ((week_4st[0] == now_dt.date() or week_4st[0] - datetime.timedelta(days=1) == now_dt.date()) or week_4st[0]-datetime.timedelta(days=1) <= now_dt.date() <= week_4st[1]) and user_type == "BRANCH USER":
        previus_day = now_dt.replace(day=1) - datetime.timedelta(days=1)
        last_date_month = datetime.datetime(previus_day.date().year, previus_day.date().month, calendar.monthrange(previus_day.date().year,previus_day.date().month)[1]).date()
        week_4th = [datetime.datetime(previus_day.date().year, previus_day.date().month, 22).date(),last_date_month]
        week_reng = week_4st
        weekly = "Week4"
        week_rng_val = week_4th
        
        
    elif (now_dt.date() == last_date_month) and user_type == "BRANCH USER":
        week_reng = week_4st
        weekly = "Week4"
        week_rng_val = [week_4th[0],last_date_month]
    # Close Week 4 Validation.
    
    # For WD Type User Weekly oprn fixed days 7 and 8 only.
    elif (week_1st[0] == now_dt.date() or week_1st[0] + datetime.timedelta(days=1) == now_dt.date() or week_1st[0] + datetime.timedelta(days=2) == now_dt.date()) and  user_type == "WD":
        week_reng =  week_1st
        weekly = "Week1"
        week_rng_val = week_1st_gng
        
    elif (week_2st[0] == now_dt.date() or week_2st[0] + datetime.timedelta(days=1) == now_dt.date() or week_2st[0] + datetime.timedelta(days=2) == now_dt.date()) and user_type == "WD":
        week_reng = week_2st
        weekly = "Week2"
        week_rng_val = week_2nd_gng
        
    elif (week_3st[0] == now_dt.date() or week_3st[0] + datetime.timedelta(days=1) == now_dt.date() or week_3st[0] + datetime.timedelta(days=2) == now_dt.date()) and user_type == "WD":
        week_reng = week_3st
        weekly = "Week3"
        week_rng_val = week_3rd_gng
        
    
    elif (week_4st[0] == now_dt.date() or week_4st[0] + datetime.timedelta(days=1) == now_dt.date()) and  user_type == "WD":
        previus_day = now_dt.replace(day=1) - datetime.timedelta(days=1)
        last_date_month = datetime.datetime(previus_day.date().year, previus_day.date().month, calendar.monthrange(previus_day.date().year,previus_day.date().month)[1]).date()
        week_4th = [datetime.datetime(previus_day.date().year, previus_day.date().month, 22).date(),last_date_month]
        week_reng = week_4st
        weekly = "Week4"
        week_rng_val = week_4th
       
       
    
    elif now_dt.date() == last_date_month and  user_type == "WD":
        week_reng = week_4st
        weekly = "Week4"
        week_rng_val = week_4th
        
    else:
        week_reng = None
        weekly = ""
        week_rng_val = None
    return week_reng, weekly, week_rng_val



def week_checkbox_wd(user):
    print("===type===",user)
    user_type = user
    now_dt = datetime.datetime.now()
    # now_dt = utils.now_date
    # now_dt = parse("2023-03-09 15:29:09")
    now_day=str(now_dt.date())
    splited = now_day.split('-')
    till_date = datetime.datetime(2009, 10, 5, 15, 00, 00)
    anot_data={}
    
    
    last_date_month = datetime.datetime(now_dt.date().year, now_dt.date().month, calendar.monthrange(now_dt.date().year,now_dt.date().month)[1]).date()
    
    # week_4st1 = [datetime.datetime(now_dt.date().year, now_dt.date().month, 1).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 3).date()]
       
    # =======================================================================================================
    # print(week_3st[0]<= now_dt.date()<= week_3st[0]-datetime.timedelta(days=1),"======pp=====")
    week_1st_gng = [datetime.datetime(now_dt.date().year, now_dt.date().month, 1).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 7).date()]
    week_2nd_gng = [datetime.datetime(now_dt.date().year, now_dt.date().month, 8).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 14).date()]
    week_3rd_gng = [datetime.datetime(now_dt.date().year, now_dt.date().month, 15).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 21).date()]
    last_date_month = datetime.datetime(now_dt.date().year, now_dt.date().month, calendar.monthrange(now_dt.date().year,now_dt.date().month)[1]).date()
    week_4th = [datetime.datetime(now_dt.date().year, now_dt.date().month, 22).date(),last_date_month]
    # week_4_weekly_gng=[week_4th[0] - relativedelta(months=1),now_dt.date().today().replace(day=1) - datetime.timedelta(days=1)]

    #fixed date assigned for week==================
    weekend_dates = (
        datetime.datetime(now_dt.date().year, now_dt.date().month, 7).date(),
        datetime.datetime(now_dt.date().year, now_dt.date().month, 14).date(),
        datetime.datetime(now_dt.date().year, now_dt.date().month, 21).date(),
        last_date_month
    )

    # current week as per reng====
    week_1st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 7).date(),datetime.datetime(now_dt.date().year, now_dt.date().month,10).date()]
    week_2st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 14).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 17).date()]
    week_3st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 21).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 24).date()]
    last_date_month = datetime.datetime(now_dt.date().year, now_dt.date().month, calendar.monthrange(now_dt.date().year,now_dt.date().month)[1]).date()
    week_4st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 1).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 3).date()]
    
    # if  week_1st[0] <= now_dt.date() <= week_1st[1] and user_type == "BRANCH USER":
    #     week_reng =  week_1st
    #     weekly = "Week1"
    #     week_rng_val = week_1st_gng
    # elif week_2st[0] <= now_dt.date() <= week_2st[1] and user_type == "BRANCH USER":
    #     week_reng = week_2st
    #     weekly = "Week2"
    #     week_rng_val = week_2nd_gng
    # elif week_3st[0] <= now_dt.date() <= week_3st[1] and user_type == "BRANCH USER":
    #     week_reng = week_3st
    #     weekly = "Week3"
    #     week_rng_val = week_3rd_gng
    # # Week 4 Validation.
    # elif ((week_4st[0] == now_dt.date() or week_4st[0] - datetime.timedelta(days=1) == now_dt.date()) or week_4st[0]-datetime.timedelta(days=1) <= now_dt.date() <= week_4st[1]) and user_type == "BRANCH USER":
    #     previus_day = now_dt.replace(day=1) - datetime.timedelta(days=1)
    #     last_date_month = datetime.datetime(previus_day.date().year, previus_day.date().month, calendar.monthrange(previus_day.date().year,previus_day.date().month)[1]).date()
    #     week_4th = [datetime.datetime(previus_day.date().year, previus_day.date().month, 22).date(),last_date_month]
    #     week_reng = week_4st
    #     weekly = "Week4"
    #     week_rng_val = week_4th
        
        
    # elif (now_dt.date() == last_date_month) and user_type == "BRANCH USER":
    #     week_reng = week_4st
    #     weekly = "Week4"
    #     week_rng_val = [week_4th[0],last_date_month]
    # Close Week 4 Validation.
    print(week_4st[0],"----------------------hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    # For WD Type User Weekly oprn fixed days 7 and 8 only.
    if (week_1st[0] == now_dt.date() or week_1st[0] + datetime.timedelta(days=1) == now_dt.date() or week_1st[0] + datetime.timedelta(days=2) == now_dt.date()) and  user_type == "WD":
        week_reng =  week_1st
        weekly = "Week1"
        week_rng_val = week_1st_gng
        
    elif (week_2st[0] == now_dt.date() or week_2st[0] + datetime.timedelta(days=1) == now_dt.date() or week_2st[0] + datetime.timedelta(days=2) == now_dt.date()) and user_type == "WD":
        week_reng = week_2st
        weekly = "Week2"
        week_rng_val = week_2nd_gng
        
    elif (week_3st[0] == now_dt.date() or week_3st[0] + datetime.timedelta(days=1) == now_dt.date() or week_3st[0] + datetime.timedelta(days=2) == now_dt.date()) and user_type == "WD":
        week_reng = week_3st
        weekly = "Week3"
        week_rng_val = week_3rd_gng
        
    
    elif week_4st[0] == now_dt.date() or week_4st[0] + datetime.timedelta(days=1) == now_dt.date() and  user_type == "WD":
        previus_day = now_dt.replace(day=1) - datetime.timedelta(days=1)
        last_date_month = datetime.datetime(previus_day.date().year, previus_day.date().month, calendar.monthrange(previus_day.date().year,previus_day.date().month)[1]).date()
        week_4th = [datetime.datetime(previus_day.date().year, previus_day.date().month, 22).date(),last_date_month]
        week_reng = week_4st
        weekly = "Week4"
        week_rng_val = week_4th
       
       
    
    elif now_dt.date() == last_date_month and  user_type == "WD":
        week_reng = week_4st
        weekly = "Week4"
        week_rng_val = week_4th
        
    else:
        week_reng = None
        weekly = ""
        week_rng_val = None
    return week_reng, weekly, week_rng_val