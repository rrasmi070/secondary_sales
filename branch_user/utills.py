import datetime

import dateutil
from branch_user.serializers import SKU_Master_ProductsSerializer
from master.models import SKU_Master_Product, Sales_Hierarchy_Master, SalesData, Sku_remarks, WdSkuCatagory
from django.db.models import Sum
import calendar
from wd.helper import week_checkbox_wd
from wd.serializers import Sku_remarksSerializer
import pandas
from dateutil.parser import parse
import base64

def base64_decode(decode_val):
    base64_bytes = decode_val.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    decode_val = sample_string.split("_")[0]
    return decode_val
    

def freeze_status_val_weekly(year, month,transaction_type):
    date_time_now = datetime.datetime.now()
    last_date_by_mo_yr = (calendar.monthrange(int(year),int(month)))[-1]
    # before_30_days_date = date_time_now.date() - datetime.timedelta(days= 30)
    before_30_days_date = ((date_time_now.date().replace(day=1))-datetime.timedelta(days=1)).replace(day=1)
    # date_as_per_m_y = parse(f"{year}-{month}-{last_date_by_mo_yr}").date()
    if transaction_type == "Week1":
        date = parse(f"{year}-{month}-07").date()
        date_range_li = pandas.date_range(start = before_30_days_date, end = date_time_now.date())
        freeze_status = False if str(date) in date_range_li else True
    elif transaction_type == "Week2":
        date = parse(f"{year}-{month}-14").date()
        # print(date,'*****************************')
        date_range_li = pandas.date_range(start = before_30_days_date, end = date_time_now.date())
        print(date_range_li,'!!!!!!!!!!!!!!')
        # print(False if str(date) in date_range_li else True,'@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        freeze_status = False if str(date) in date_range_li else True
    elif transaction_type == "Week3":
        date = parse(f"{year}-{month}-21").date()
        date_range_li = pandas.date_range(start = before_30_days_date, end = date_time_now.date())
        freeze_status = False if str(date) in date_range_li else True
    elif transaction_type == "Week4":
        date = parse(f"{year}-{month}-{last_date_by_mo_yr}").date()
        date_range_li = pandas.date_range(start = before_30_days_date, end = date_time_now.date())
        freeze_status = False if str(date) in date_range_li else True
        # freeze_status = True if date_time_now.date() < date < before_30_days_date else False
    print(freeze_status,date,"=====================pp")
    return freeze_status,date


def sku_remark(wd_id,date_f):
    Sku_Serializer = []
    week_num = None
    if wd_id:
        if week_num:
            pass
        else:
            skuremark_obj = Sku_remarks.objects.filter(
                wd_id=wd_id, sales_date_time=date_f)

            if skuremark_obj:
                remark = Sku_remarksSerializer(
                    skuremark_obj, many=True).data
                Sku_Serializer.append(remark)
            else:
                Sku_Serializer
    return Sku_Serializer



def branch_user_time_validation_for_daily_sales(sale_date):
    print("===type===","user")
    sale_date = parse(sale_date).date()
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
    print(week_4th,"====================================================week_4th")
    #fixed date assigned for week==================
    weekend_dates = (
        datetime.datetime(now_dt.date().year, now_dt.date().month, 7).date(),
        datetime.datetime(now_dt.date().year, now_dt.date().month, 14).date(),
        datetime.datetime(now_dt.date().year, now_dt.date().month, 21).date(),
        last_date_month
    )

    # current week as per reng====
    week_1st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 7).date(),datetime.datetime(now_dt.date().year, now_dt.date().month,11).date()]
    week_2st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 14).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 18).date()]
    week_3st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 21).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 25).date()]
    last_date_month = datetime.datetime(now_dt.date().year, now_dt.date().month, calendar.monthrange(now_dt.date().year,now_dt.date().month)[1]).date()
    week_4st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 1).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 3).date()]
    
    previus_day = now_dt.replace(day=1) - datetime.timedelta(days=1)
    last_date_month_last = datetime.datetime(previus_day.date().year, previus_day.date().month, calendar.monthrange(previus_day.date().year,previus_day.date().month)[1]).date()
    week_4th_rng = [datetime.datetime(previus_day.date().year, previus_day.date().month, 22).date(),last_date_month_last]
    
    if  week_1st_gng[0] <= sale_date <= week_1st[1] and week_1st[1] >= sale_date and week_1st[1] >= now_dt.date():
        print("----------------------1")
        freez_status = {'freeze_status':False,'update_status': True}
        
    elif week_2nd_gng[0] <= sale_date <= week_2st[1] and week_2st[1] >= sale_date and week_2st[1] >= now_dt.date():
        print("----------------------2")
        freez_status = {'freeze_status':False,'update_status': True}
        
    elif week_3rd_gng[0] <= sale_date <= week_3st[1] and week_3st[1] >= sale_date and week_3st[1] >= now_dt.date():
        print("----------------------3")
        freez_status = {'freeze_status':False,'update_status': True}
    elif week_3rd_gng[1] < sale_date <= last_date_month and now_dt.date() <= last_date_month:
        print("----------------------4")
        freez_status = {'freeze_status':False,'update_status': True}
        
    elif (week_4th_rng[0] <= sale_date <= week_4th_rng[1]) and week_4th_rng[0] <= now_dt.date() <= week_4st[1]:
        print("----------------------7new")
        freez_status = {'freeze_status':False,'update_status': True}
        
    # Week 4 Validation.
    # elif ((week_4st[0] == now_dt.date() or week_4st[0] - datetime.timedelta(days=1) == now_dt.date()) or week_4st[0]-datetime.timedelta(days=1) <= now_dt.date() <= week_4st[1]):
    #     print("----------------------5")
    #     previus_day = now_dt.replace(day=1) - datetime.timedelta(days=1)
    #     last_date_month = datetime.datetime(previus_day.date().year, previus_day.date().month, calendar.monthrange(previus_day.date().year,previus_day.date().month)[1]).date()
    #     week_4th = [datetime.datetime(previus_day.date().year, previus_day.date().month, 22).date(),last_date_month]
    #     week_reng = week_4st
    #     weekly = "Week4"
    #     week_rng_val = week_4th
    #     freez_status = {'freeze_status':False,'update_status': True}
        
        
    # elif week_4th[1] <= sale_date or (now_dt.date() == last_date_month):
    #     print("----------------------6")
    #     week_reng = week_4st
    #     weekly = "Week4"
    #     week_rng_val = [week_4th[0],last_date_month]
    #     freez_status = {'freeze_status':False,'update_status': True}
    else:
        print("-------------------------------------------------its else")
        freez_status = {'freeze_status':True,'update_status': False}
    
    return freez_status
        
        

def editable_status(request_user, transaction_type, month = None, year = None, sale_date = None):
    status_data_value = {}
    today_date = datetime.datetime.now()
    till_time = datetime.datetime(2009, 10, 5, 14, 59, 59)
    sale_date_parse = parse(sale_date)
    week_details = week_checkbox_wd(request_user.user_type) 
    if request_user.user_type == "BRANCH USER":
        if transaction_type == "DAILY":
            print("--------------------------bu--------------------daily")
            status_data_value = branch_user_time_validation_for_daily_sales(sale_date)
        else:
            # if transaction type is WEELY
            freeze_status_val = freeze_status_val_weekly(year, month, transaction_type)
            status_data_value = freeze_status_val[0]
            update_status =  False if status_data_value == True else True
            status_data_value = {'freeze_status':status_data_value,'update_status':update_status}
            

    elif request_user.user_type == "WD":
        if transaction_type == "DAILY":
            week_details = week_checkbox_wd(request_user.user_type)
            print(week_details,"---------------------------------------------------ll")
            # print(parse(sale_date).date() < (week_details[2][1] - datetime.timedelta(days=1)),"============/////////////////====week_details")
            previous_date = (today_date - datetime.timedelta(days=1)).date()

            # if request_user.user_type == "WD" and week_details[1]:
            #     start_time = datetime.datetime(2009, 10, 5, 0, 0, 1)
            #     combine_0_time = datetime.datetime.combine(week_details[2][1], start_time.time())
            #     combine_3pm_time = datetime.datetime.combine(week_details[2][1] + datetime.timedelta(days=2), till_time.time())
            #     print(week_details[1] == 'Week1' ,'and', combine_3pm_time.date() <= today_date.date() ,'and', sale_date_parse.date() == week_details[2][1] ,'and', today_date.time() < till_time.time(),"============>>>>")
            #     if (today_date.date()-datetime.timedelta(days=2)) == sale_date_parse.date() and str(sale_date_parse.date().strftime('%A')) == 'Saturday' and today_date.time() < till_time.time():
            #         print('------------------------for Saturday condition')
                    
            #         status_data_value = {'freeze_status': False, 'update_status': True, 'user_lock_unlock': request_user.lock_unlock}
                    
            #     elif (parse(sale_date).date() <= (week_details[2][1] - datetime.timedelta(days=2))) and str(sale_date_parse.date().strftime('%A')) != 'Saturday':
            #         print("-----------------222222")
            #         status_data_value = {'freeze_status': True, 'update_status': False, 'user_lock_unlock': request_user.lock_unlock}
                    
            #     # elif (parse(sale_date).date() <= (week_details[2][1] - datetime.timedelta(days=1)) and today_date.time() <= till_time.time()):   #  or parse(sale_date).date() < week_details[2][1]
            #     #     print("-----------------kkkk")
            #     #     status_data_value = {'freeze_status': False, 'update_status': True, 'user_lock_unlock': request_user.lock_unlock}
            #     elif (parse(sale_date).date() <= (week_details[2][1] - datetime.timedelta(days=1)) and today_date.time() <= till_time.time()) and week_details[0][1] + datetime.timedelta(days=1) == today_date.date():
            #         print("-----------------kkkk")
            #         status_data_value = {'freeze_status': False, 'update_status': True, 'user_lock_unlock': request_user.lock_unlock}

            #     elif parse(sale_date).date() < week_details[2][1] and week_details[1] and week_details[0][1] - datetime.timedelta(days=1) == today_date.date():
            #         print('this condition will run when sale date lessthan previous month lass than and today datetime is weekend range last day after 3 pm')
            #         status_data_value = {'freeze_status': True, 'update_status': False, 'user_lock_unlock': request_user.lock_unlock}
                    
            #     elif combine_0_time <=today_date <= combine_3pm_time - datetime.timedelta(days=1) and week_details[2][1]== parse(sale_date).date():
            #         print("-----------------444")
            #         status_data_value = {'freeze_status': False, 'update_status': True, 'user_lock_unlock': request_user.lock_unlock}
            #     elif combine_0_time <=today_date >= combine_3pm_time and week_details[2][1]== parse(sale_date).date():
            #         print("-----------------555")
            #         status_data_value = {'freeze_status': True, 'update_status': False, 'user_lock_unlock': request_user.lock_unlock}
            #     elif previous_date >= sale_date_parse.date() and today_date.time() > till_time.time():
            #         print("-----------------666")
            #         status_data_value = {'freeze_status': True, 'update_status': False, 'user_lock_unlock': request_user.lock_unlock}
            #     else:
            #         print("-----------------777")
            #         status_data_value = {'freeze_status': False, 'update_status': True, 'user_lock_unlock': request_user.lock_unlock}
            print(sale_date_parse.date() == today_date.date(),"---------------------------------------------hh")
            if previous_date == sale_date_parse.date() and today_date.time() < till_time.time():
                print("-----------------------------1")
                status_data_value = {'freeze_status': False, 'update_status': True, 'user_lock_unlock': request_user.lock_unlock}
            elif (today_date.date()-datetime.timedelta(days=2)) == sale_date_parse.date() and str(sale_date_parse.date().strftime('%A')) == 'Saturday' and today_date.time() < till_time.time():
                print("-----------------------------2")
                status_data_value = {'freeze_status': False, 'update_status': True, 'user_lock_unlock': request_user.lock_unlock}
            elif sale_date_parse.date() == today_date.date():
                print("-----------------------------4")
                
                status_data_value = {'freeze_status': False, 'update_status': True, 'user_lock_unlock': request_user.lock_unlock}
            elif week_details[1]:
                start_time = datetime.datetime(2009, 10, 5, 0, 0, 1)
                till_date = datetime.datetime(2009, 10, 5, 14, 59, 59)
                combine_0_time = datetime.datetime.combine(week_details[2][1], start_time.time())
                combine_3pm_time = datetime.datetime.combine(week_details[2][1] + datetime.timedelta(days=3), till_date.time())
                print("----------------------enter-------3")
                if combine_0_time <=today_date <= combine_3pm_time and week_details[2][1]== sale_date_parse.date():
                    print("-----------------------------3")
                    status_data_value = {'freeze_status': False, 'update_status': True, 'user_lock_unlock': request_user.lock_unlock}
                else:
                    print("-----------------------------5 -----else")
                    status_data_value = {'freeze_status': True, 'update_status': False, 'user_lock_unlock': request_user.lock_unlock}
                
            # elif sale_date_parse.date() == today_date.date():
            #     print("-----------------------------4")
            #     status_data_value = {'freeze_status': False, 'update_status': True, 'user_lock_unlock': request_user.lock_unlock}
            else:
                print("-----------------------------6 -----else")
                status_data_value = {'freeze_status': True, 'update_status': False, 'user_lock_unlock': request_user.lock_unlock}
            
        else:
            # if transaction type is WEELY
            status_data_value = {'freeze_status': False, 'update_status': True, 'user_lock_unlock': request_user.lock_unlock}
    return status_data_value



def top_sku_sales_new(wd_id,category,wd_town_id_list,last_date, till_date):
    
    sku_id_list = WdSkuCatagory.objects.filter(status = True,wd_town_id__in=wd_town_id_list).values_list('sku_id', flat=True)
    topsqu_list = SalesData.objects.filter(sku_id__in=sku_id_list, town_id__in=wd_town_id_list, brand_category=category, sales_date_time__gte=last_date, transaction_type="DAILY").values_list(
    'sku_id', flat=True).annotate(sku_totalsale=Sum('grand_total')).order_by('-sku_totalsale')
    sku_list_top = []
    freeze_obj = None
    sku_id_list3 = list(set(list(sku_id_list)))
    for i in topsqu_list:
        if i in sku_id_list3:
            sku_list_top.append(i)
            sku_id_list3.remove(i)
    sku_lists = sku_list_top + sku_id_list3
    #
    list1 = []
    sku_id_list = []
    for k in sku_lists:
        sku = SKU_Master_Product.objects.filter(
            sku_id=k, effective_from__lte=till_date, category_code=category).last()
        if sku:
            list1.append(sku)
            sku_id_list.append(sku_id_list.sku_id)
    sku_serializars = SKU_Master_ProductsSerializer(list1, many=True)
    sku_serializars_v = sku_serializars.data
    return sku_serializars_v


def top_sku_sales(wd_id,category,wd_town_id_list,last_date, till_date):
    
    sku_id_list = WdSkuCatagory.objects.filter(status = True,wd_town_id__in=wd_town_id_list).values_list('sku_id', flat=True)
    topsqu_list = SalesData.objects.filter(sku_id__in=sku_id_list, town_id__in=wd_town_id_list, brand_category=category, sales_date_time__gte=last_date, transaction_type="DAILY").values_list(
    'sku_id', flat=True).annotate(sku_totalsale=Sum('grand_total')).order_by('-sku_totalsale')
    sku_list_top = []
    freeze_obj = None
    sku_id_list3 = list(set(list(sku_id_list)))
    for i in topsqu_list:
        if i in sku_id_list3:
            sku_list_top.append(i)
            sku_id_list3.remove(i)
    sku_lists = sku_list_top + sku_id_list3
    #
    list1 = []
    for k in sku_lists:
        sku = SKU_Master_Product.objects.filter(
            sku_id=k, effective_from__lte=till_date, category_code=category).last()
        if sku:
            list1.append(sku)
    sku_serializars = SKU_Master_ProductsSerializer(list1, many=True)
    sku_serializars_v = sku_serializars.data
    return sku_serializars_v



def branch_user_weekly(unique_top_sku_li,wd_id,town_id,wd_town_id_list,category,transaction_type,month,year):
    # branch_user_weekly(unique_top_sku_li,wd_id,town_id,wd_town_id_list,category,transaction_type,month,year)
    print(type(month),"===mm===11")
    Salesobj = SalesData.objects.filter(wd_id=wd_id, town_id__in=wd_town_id_list,brand_category=category, transaction_type = transaction_type, town_code__in=town_id,sales_date_time__month = month,sales_date_time__year = year).values()
    print(Salesobj,"=========================77=============")
    # if Salesobj:
    freeze_status_val = freeze_status_val_weekly(year, month, transaction_type)
    print("--------------88",freeze_status_val)
    for i in unique_top_sku_li:
        sku_id = i.get('sku_id')
        sale_data = Salesobj.filter(sku_id = sku_id).values()
        # print(sku_id,"sku=======================",sale_data)
        if sale_data:
            sale_data[0]['freeze_status'] = freeze_status_val[0]
            i["SalesData"] = sale_data
        else:
            # i["SalesData"] = [{"freeze_status": True}]
        # , sales_date_time=date_f
    # else:
            i["SalesData"] = [{"freeze_status": freeze_status_val[0]}]
    
    # print(i,"=====================================================")
    # pass
    return unique_top_sku_li , freeze_status_val[0]


def adminapiweekly(wd_id, category, town_id, date_f, week_num, month, year, week):
    today_date = datetime.datetime.now()
    # print(date_f)
    last_date = date_f
    # breakpoint()
    # week_details = week_sele_before_date("BRANCH USER")
    freeze_status_val = freeze_status_val_weekly(year, month, week)
    

    if week_num is not None:  # this will exicute for BRANCH_USER Weekly data
        if wd_id:
            wo_4th = [1, 2, 3]
            # print(wd_id,"======")
            # if x in wo_4th:
            #     week_sale_date = today_date.date() - relativedelta(months=1)
            # else:
            #     week_sale_date = today_date.date()
            wd_town_id_list = Sales_Hierarchy_Master.objects.filter(
                wd_id=wd_id).values_list('wd_town_id', flat=True)
            
            sku_id_list = WdSkuCatagory.objects.filter(status = True,
                wd_town_id__in=wd_town_id_list).values_list('sku_id', flat=True)
            topsqu_list = SalesData.objects.filter(sku_id__in=sku_id_list, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, sales_date_time__gte=last_date, transaction_type=week_num).values_list(
                'sku_id', flat=True).annotate(sku_totalsale=Sum('grand_total')).order_by('-sku_totalsale')
            sku_list_top = []
            sku_id_list3 = list(set(list(sku_id_list)))
            for i in topsqu_list:
                if i in sku_id_list3:
                    sku_list_top.append(i)
                    sku_id_list3.remove(i)
            sku_lists = sku_list_top + sku_id_list3
            list1 = []
            for k in sku_lists:
                sku = SKU_Master_Product.objects.filter(
                    sku_id=k, effective_from__lte=date_f, category_code=category).last()
                if sku:
                    list1.append(sku)
            sku_serializars = SKU_Master_ProductsSerializer(
                list1, many=True)
            sku_serializars_v = sku_serializars.data
            for i in sku_serializars_v:
                sku_id = i.get('sku_id')
                if category:
                    Salesobj = SalesData.objects.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time = freeze_status_val[1], brand_category=category, transaction_type=week, town_code__in=town_id).values()
                else:
                    Salesobj = SalesData.objects.filter(
                        sku_id=sku_id, sales_date_time=freeze_status_val[1], wd_id=wd_id, town_id__in=wd_town_id_list, transaction_type=week, town_code__in=town_id).values()
                if Salesobj:
                    i["SalesData"] = Salesobj

                else:
                    i["SalesData"] = [{}]
        return sku_serializars_v
        # return Response({"message": "Successful", "status_data": "[status_data_val]", "remarks":" Sku_Serializer", "data": sku_serializars_v, 'status': True})

def adminapidaily(wd_id,category,town_id,date_f):
    # week_details = week_sele_before_date("BRANCH USER")
    
    today_date = datetime.datetime.now()
    
    last_date = today_date + \
                dateutil.relativedelta.relativedelta(months=-6)

    # print("hello")
    wd_town_id_list = Sales_Hierarchy_Master.objects.filter(
        wd_id=wd_id).values_list('wd_town_id', flat=True)
    sku_id_list = WdSkuCatagory.objects.filter(status = True,
        wd_town_id__in=wd_town_id_list).values_list('sku_id', flat=True)
    topsqu_list = SalesData.objects.filter(sku_id__in=sku_id_list, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, sales_date_time__gte=last_date, transaction_type="DAILY").values_list(
        'sku_id', flat=True).annotate(sku_totalsale=Sum('grand_total')).order_by('-sku_totalsale')
    sku_list_top = []
    freeze_obj = None
    sku_id_list3 = list(set(list(sku_id_list)))
    for i in topsqu_list:
        if i in sku_id_list3:
            sku_list_top.append(i)
            sku_id_list3.remove(i)
    sku_lists = sku_list_top + sku_id_list3
#
    list1 = []
    for k in sku_lists:
        sku = SKU_Master_Product.objects.filter(
            sku_id=k, effective_from__lte=date_f, category_code=category).last()
        if sku:
            list1.append(sku)
    sku_serializars = SKU_Master_ProductsSerializer(
        list1, many=True)
    sku_serializars_v = sku_serializars.data
    for i in sku_serializars_v:
        sku_id = i.get('sku_id')
        if category:

            # if  Salesobj :
            #     SalesData.objects.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list,
            #                                         brand_category=category, sales_date_time=date_f, transaction_type="DAILY", town_code__in=town_id).values()
            # else:
            #     Salesobj = SalesData.objects.filter(
            #         sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time=date_f, transaction_type="DAILY", town_code__in=town_id).values()
            #     sku_serializars_v=Salesobj
        
        
            if category:
                Salesobj = SalesData.objects.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time = date_f, brand_category=category, transaction_type='DAILY', town_code__in=town_id).values()
            else:
                Salesobj = SalesData.objects.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list,
                                                    sales_date_time=date_f, transaction_type="DAILY", town_code__in=town_id).values()

            if Salesobj:
                i["SalesData"] = Salesobj

            else:
                i["SalesData"] = [{}]

               
    return  sku_serializars_v
    # return Response({"message": "Successful", "status_data": "[status_data_val]", "remarks":" Sku_Serializer", "data": sku_serializars_v, 'status': True})


def sale_data_obj_with_sequence(sku_sequence,salesdf=None,sales_objects = None,user_type=None, weekly_sale=None, freeze_status = None):
    skusales_obj = []
    if user_type and weekly_sale:
        for sku in sku_sequence:
            skusales_obj.append(sku)
            if not salesdf.empty:
                print('------------------------------1111')
                data = salesdf[(salesdf.sku_code == sku['sku_code'])]
                freeze_status = freeze_status
                sale_data = data.to_dict('records') if data.to_dict('records') else [{'freeze_status':freeze_status}]
                sale_data[0]['freeze_status'] = freeze_status
                print(sale_data)
                sku['SalesData'] = sale_data
            else:
                print('------------------------------222')
                # data = [{}]
                sku['SalesData'] = [{'freeze_status':freeze_status}]
        
        return skusales_obj
    else:
        for sku in sku_sequence:
            print("----------------------------others")
            skusales_obj.append(sku)
            if not salesdf.empty:
                data = salesdf[(salesdf.sku_code == sku['sku_code'])]
                sku['SalesData'] = data.to_dict('records') if data.to_dict('records') else [{}]
            else:
                # data = [{}]
                sku['SalesData'] = [{}]
        
        return skusales_obj



def appendSFA(ls,wd_data):
    for i in ls:
        i["wd_type"]=wd_data
    return ls