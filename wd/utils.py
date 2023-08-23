
import datetime
import re
from base.models import BranchMaster, WDmaster, User, Weeklysales_update_log
from master.models import SKU_Master_Product, Sales_Hierarchy_Master, SalesData, WdSkuCatagory
from .helper import week_sele_before_date
from .serializers import SalesDataCreateWeekSerializer
from django.db.models import Sum
from dateutil.parser import parse
import calendar
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings
from secondary_sales.settings import *
import json

# Manage datetime according daily and weekly
# now_date = parse("2022-06-21 15:29:09")
# now_date = datetime.datetime.now()  # set for global datetime.

def freeze_status_val_weekly_and_date(year, month,transaction_type):
    date_time_now = datetime.datetime.now()
    last_date_by_mo_yr = (calendar.monthrange(int(year),int(month)))[-1]
    # before_30_days_date = date_time_now.date() - datetime.timedelta(days= 30)
    before_30_days_date = ((date_time_now.date().replace(day=1))-datetime.timedelta(days=1)).replace(day=1)
    # date_as_per_m_y = parse(f"{year}-{month}-{last_date_by_mo_yr}").date()
    if transaction_type == "Week1":
        date = [parse(f"{year}-{month}-01").date(), parse(f"{year}-{month}-07").date()]
        freeze_status = True if date_time_now.date() < date[1] < before_30_days_date else False
    elif transaction_type == "Week2":
        date = [parse(f"{year}-{month}-08").date(), parse(f"{year}-{month}-14").date()]
        freeze_status = True if date_time_now.date() < date[1] < before_30_days_date else False
    elif transaction_type == "Week3":
        date = [parse(f"{year}-{month}-15").date(), parse(f"{year}-{month}-21").date()]
        freeze_status = True if date_time_now.date() < date[1] < before_30_days_date else False
    elif transaction_type == "Week4":
        date = [parse(f"{year}-{month}-{22}").date(), parse(f"{year}-{month}-{last_date_by_mo_yr}").date()]
        freeze_status = True if date_time_now.date() < date[1] < before_30_days_date else False
    return freeze_status,date


def sum_weekly_data(week_data_sums, json_data, help_week,wd_master,wd_town_code, userid):
  
    global_data = []
    for week_data_sum in week_data_sums:
        
        unit_value = SKU_Master_Product.objects.filter(sku_id=week_data_sum['sku_id']).last()
        wd_town_list =Sales_Hierarchy_Master.objects.filter(wd_id=json_data['wd_username'],town_code=json_data['town_code']).values_list('wd_town_id',flat=True)
        wdobj = WdSkuCatagory.objects.filter(wd_town_id__in=wd_town_list,sku_id=json_data['sku_id']).last()
        sale_data = SalesData.objects.filter(wd_id__icontains = week_data_sum['wd_id'],sku_id__icontains = week_data_sum['sku_id'],sales_date_time__icontains = help_week[2][1],transaction_type__icontains=help_week[1],town_id__icontains = week_data_sum['town_id'],town_code__icontains=wd_town_code,brand_category__icontains=week_data_sum['brand_category']).last()
        sele_week_obj = {}

        source_data = WDmaster.objects.filter(wd_ids=week_data_sum['wd_id']).last()
        if source_data:
            source_user = source_data.wd_type
        else:
            source_user = None
        sele_week_obj['town_id'] = week_data_sum['town_id']
        sele_week_obj['sku_id'] = week_data_sum['sku_id']
        sele_week_obj['wd_id'] = week_data_sum['wd_id']
        sele_week_obj['sales_date_time'] = help_week[2][1]
        sele_week_obj['statename'] = source_data.wd_state if source_data else None
        sele_week_obj['transaction_source'] = source_user
        sele_week_obj['created_by'] = userid # auto_secdulre.
        sele_week_obj['transaction_type'] = help_week[1]
        sele_week_obj['created_date'] = datetime.datetime.now()
        sele_week_obj['local_sales_retail'] = round(week_data_sum['local_sales_retail__sum'], 2)
        sele_week_obj['local_sales_dealer'] = round(week_data_sum['local_sales_dealer__sum'], 2)
        sele_week_obj['local_sales_modern_trade'] = round(week_data_sum['local_sales_modern_trade__sum'], 2)
        sele_week_obj['local_sales_hawker'] = round(week_data_sum['local_sales_hawker__sum'], 2)
        sele_week_obj['outstation_sales_reatil'] = round(week_data_sum['outstation_sales_reatil__sum'], 2)
        sele_week_obj['outstation_sales_dealer'] = round(week_data_sum['outstation_sales_dealer__sum'], 2)
        sele_week_obj['outstation_sales_modern_trade'] = round(week_data_sum['outstation_sales_modern_trade__sum'], 2)
        sele_week_obj['outstation_sales_hawker'] = round(week_data_sum['outstation_sales_hawker__sum'], 2)
        sele_week_obj['other_sales_retail'] = round(week_data_sum['other_sales_retail__sum'], 2)
        sele_week_obj['other_sales_dealer'] = round(week_data_sum['other_sales_dealer__sum'], 2)
        sele_week_obj['other_sales_modern_trade'] = round(week_data_sum['other_sales_modern_trade__sum'], 2)
        sele_week_obj['other_issues_other'] = round(week_data_sum['other_issues_other__sum'], 2)
        sele_week_obj['other_issues_damage'] = round(week_data_sum['other_issues_damage__sum'], 2)
        sele_week_obj['other_issues_return'] = round(week_data_sum['other_issues_return__sum'], 2)
        sele_week_obj['total_local_sales'] = round(week_data_sum['total_local_sales__sum'], 2)
        sele_week_obj['total_outstation_sales'] = round(week_data_sum['total_outstation_sales__sum'], 2)
        sele_week_obj['total_other_sales'] = round(week_data_sum['total_other_sales__sum'], 2)
        sele_week_obj['total_issue'] = round(week_data_sum['total_issue__sum'], 2)
        sele_week_obj['grand_total'] = round(week_data_sum['grand_total__sum'], 2)
        sele_week_obj['town_code'] = wd_town_code
        sele_week_obj['sku_short_name'] = unit_value.sku_short_name
        sele_week_obj['sku_code'] = unit_value.sku_code
        sele_week_obj['wd_name'] = wd_master.wd_name
        sele_week_obj['town_name'] = wd_master.wd_postal_code
        sele_week_obj['wd_type'] = wd_master.wd_type
        sele_week_obj['cnf_id'] = wdobj.cnf_id
        sele_week_obj['distrcode'] = str(week_data_sum['town_id'])+"-"+str(str(wd_town_code))
        sele_week_obj['brand_category'] = week_data_sum['brand_category']
        sele_week_obj.pop('transaction_source')     

        
        if unit_value:
           
            sele_week_obj['company'] = unit_value.company
        else:
           
            sele_week_obj['company'] = ""
        wdregion = User.objects.filter(user_id=week_data_sum['wd_id']).last()
        region = BranchMaster.objects.filter(branch_code=wdregion.locationcode).last()
        sele_week_obj['region'] = region.region
        sele_week_obj['unit_price'] = float(wdobj.last_price)
        sele_week_obj['value'] = float(sele_week_obj['grand_total']) * float(wdobj.last_price)
        global_data.append(sele_week_obj)
        
        
        if sale_data:
            print('sele_week_obj', sele_week_obj)
            print('-------------------------------------1111-')
            serializer = SalesDataCreateWeekSerializer(instance=sale_data,data=sele_week_obj, partial=True)
            if serializer.is_valid():
                serializer.save()
                
            print(serializer.errors)
        
        else:
            print('(((((((((((((((((((((((((')
            # sele_week_obj.pop('transaction_source')
            print(global_data)
            print('joooooooooooooooooooooooooo')
            serializer = SalesDataCreateWeekSerializer(data=sele_week_obj)
            if serializer.is_valid():
                serializer.save()
                
            print(serializer.errors)
   
    
    
def daily_sales_data_save(record, userid, location, help_week,user_type):
    weeks = ('Week1','Week2','Week3','Week4')
    record_length = len(record)
    count = 0
    data_changes=[]
    for row in record:
        count = count + 1
        tracationtype = 'DAILY' if row['week_num'].strip()=="" else row['week_num'].strip()
        wd_town_list =Sales_Hierarchy_Master.objects.filter(wd_id=row['wd_username'],town_code=row['town_code']).values_list('wd_town_id',flat=True)
        wdobj = WdSkuCatagory.objects.filter(wd_town_id__in=wd_town_list,sku_id=row['sku_id']).last()
       
        unit_value = SKU_Master_Product.objects.filter(sku_id = row['sku_id']).last()
        region = BranchMaster.objects.filter(branch_code=location).last()
        wd_master = WDmaster.objects.filter(wd_ids =row['wd_username']).last()
       
        if tracationtype == 'DAILY':
            print('daily')
            sale_data = SalesData.objects.filter(wd_id__icontains = row['wd_username'],sku_id__icontains = row['sku_id'],sales_date_time__icontains = row['sale_date_time'],transaction_type__icontains=tracationtype,town_id__icontains = wdobj.wd_town_id,town_code__icontains=row['town_code'],brand_category__icontains=row['brand_category']).last() 
        else :
            week_date_and_freeze_status = freeze_status_val_weekly_and_date(row['year'], row['month'],row['week_num'])
            print('weekly',week_date_and_freeze_status)
            # weeklastdate = help_week[2][1]
            # weekstartdate = help_week[2][0]
            weeklastdate = week_date_and_freeze_status[1][1]
            weekstartdate = week_date_and_freeze_status[1][0]
            freezestatus = SalesData.objects.filter(wd_id__icontains = row['wd_username'],sku_id__icontains = row['sku_id'],sales_date_time__gte=weekstartdate,sales_date_time__lte=weeklastdate,town_id__icontains = wdobj.wd_town_id,town_code__icontains=row['town_code'],brand_category__icontains=row['brand_category']).last()
           
            if freezestatus:
                if row['freeze_status'] == True:
                   
                    SalesData.objects.filter(wd_id__icontains = row['wd_username'],sku_id__icontains = row['sku_id'],sales_date_time__gte=weekstartdate,sales_date_time__lte=weeklastdate,town_id__icontains = wdobj.wd_town_id,town_code__icontains=row['town_code'],brand_category__icontains=row['brand_category']).update(freeze_status=True)
                    
                    
            sale_data = SalesData.objects.filter(wd_id__icontains = row['wd_username'],sku_id__icontains = row['sku_id'],sales_date_time__icontains = weeklastdate,transaction_type__icontains=tracationtype,town_id__icontains = wdobj.wd_town_id,town_code__icontains=row['town_code'],brand_category__icontains=row['brand_category']).last()    
        
        record_data = {}
    
        record_data['sku_id']=row['sku_id']
        record_data['wd_id']=row['wd_username']
        record_data['statename']=row
        record_data['town_id']=wdobj.wd_town_id
        record_data['statename']=wd_master.wd_state
        
        
        if tracationtype == 'DAILY':
            record_data['sales_date_time']= row['sale_date_time']
        else:
            # record_data['sales_date_time']= weeklastdate  week_date_and_freeze_status
            record_data['sales_date_time']= week_date_and_freeze_status[1][1]
        # print(row['local_sales_retail'],'ttttttttttttt')    
        
        
        # obj = SalesData.objects.filter(wd_id=row['wd_username'],sku_id=row['sku_id'],town_id=wdobj.wd_town_id,sales_date_time= row['sale_date_time']).last()
        # print(obj,'uuuuuuuuuuuuuuuuuuuuuu')
        
        
        branch = Sales_Hierarchy_Master.objects.filter(wd_id=wd_master.wd_ids).last()
        skuname = SKU_Master_Product.objects.filter(sku_id=row['sku_id']).last() #.sku_name
        skucode = SKU_Master_Product.objects.filter(sku_id=row['sku_id']).last().sku_code
        
        # print(str(branch),'jibeoyuvf79cvt79cdf7d5c7')
        # print(sale_data.local_sales_retail,'zzzzzzzzzzzzzzzz------eeeeeeeeeeeeeeeeee',row['local_sales_retail'])
        if tracationtype != 'DAILY' and user_type != 'WD':
            if ((sale_data.local_sales_retail if sale_data else 0) != float(row['local_sales_retail'])) or (not sale_data) :
                update_data_instance = Weeklysales_update_log()
                update_data_instance.sku_id=row['sku_id']
                update_data_instance.wd_id=row['wd_username']
                update_data_instance.wd_town_id=wdobj.wd_town_id
                update_data_instance.branch_id = branch.region
                
                update_data_instance.previous_quantity=str(sale_data.local_sales_retail if sale_data else 0) 
                update_data_instance.new_quantity=row['local_sales_retail']
                update_data_instance.year=str(row['year'])
                update_data_instance.month=row['month']
                update_data_instance.week=row['week_num']
                update_data_instance.transaction_type=tracationtype
                update_data_instance.brand_category=row['brand_category']
                update_data_instance.sku_name=str(skuname.sku_name)
                update_data_instance.sku_code=skucode
                update_data_instance.sales_type = str('local sales retail')
                if float(row['local_sales_retail']) != 0:
                    update_data_instance.save()
                data_changes.append({'key':'local_sales_retail','old_value':sale_data.local_sales_retail if sale_data else 0,'new_value':row['local_sales_retail']})
            record_data['local_sales_retail']=row['local_sales_retail']
            
            if ((sale_data.local_sales_dealer  if sale_data else 0) != float(row['local_sales_dealer'])) or (not sale_data) :
                update_data_instance = Weeklysales_update_log()
                update_data_instance.sku_id=row['sku_id']
                update_data_instance.wd_id=row['wd_username']
                update_data_instance.wd_town_id=wdobj.wd_town_id
                update_data_instance.branch_id = branch.region
                update_data_instance.previous_quantity=str(sale_data.local_sales_dealer  if sale_data else 0)
                update_data_instance.new_quantity=row['local_sales_dealer']
                update_data_instance.year=str(row['year'])
                update_data_instance.month=row['month']
                update_data_instance.week=row['week_num']
                update_data_instance.transaction_type=tracationtype
                update_data_instance.brand_category=row['brand_category']
                update_data_instance.sku_name=str(skuname.sku_name)
                
                update_data_instance.sku_code=skucode
                update_data_instance.sales_type = str('local sales dealer')
                print(update_data_instance.sales_type,'ooooooooooooo', str('local sales dealer'))
                if float(row['local_sales_dealer']) != 0:
                    update_data_instance.save()
                data_changes.append({'key':'local_sales_dealer','old_value':sale_data.local_sales_dealer  if sale_data else 0,'new_value':row['local_sales_dealer']})
            record_data['local_sales_dealer']= row['local_sales_dealer']
            
            if  ((sale_data.local_sales_modern_trade if sale_data else 0) != float(row['local_sales_modern_trade'])) or (not sale_data):
                update_data_instance = Weeklysales_update_log()
                update_data_instance.sku_id=row['sku_id']
                update_data_instance.wd_id=row['wd_username']
                update_data_instance.wd_town_id=wdobj.wd_town_id
                update_data_instance.branch_id = branch.region
                update_data_instance.previous_quantity=str(sale_data.local_sales_modern_trade if sale_data else 0)
                update_data_instance.new_quantity=row['local_sales_modern_trade']
                update_data_instance.year=str(row['year'])
                update_data_instance.month=row['month']
                update_data_instance.week=row['week_num']
                update_data_instance.transaction_type=tracationtype
                update_data_instance.brand_category=row['brand_category']
                update_data_instance.sku_name=str(skuname.sku_name)
                update_data_instance.sku_code=skucode
                update_data_instance.sales_type = str('local sales modern trade')
                if float(row['local_sales_modern_trade']) != 0:
                    update_data_instance.save()
                data_changes.append({'key':'local_sales_modern_trade','old_value':sale_data.local_sales_modern_trade if sale_data else 0,'new_value':row['local_sales_modern_trade']})
            record_data['local_sales_modern_trade']= row['local_sales_modern_trade']
            
            if ((sale_data.local_sales_hawker if sale_data else 0) !=float(row['local_sales_hawker'])) or (not sale_data):
                update_data_instance = Weeklysales_update_log()
                update_data_instance.sku_id=row['sku_id']
                update_data_instance.wd_id=row['wd_username']
                update_data_instance.wd_town_id=wdobj.wd_town_id
                update_data_instance.branch_id = branch.region
                update_data_instance.previous_quantity=str(sale_data.local_sales_hawker if sale_data else 0)
                update_data_instance.new_quantity=row['local_sales_hawker']
                update_data_instance.year=str(row['year'])
                update_data_instance.month=row['month']
                update_data_instance.week=row['week_num']
                update_data_instance.transaction_type=tracationtype
                update_data_instance.brand_category=row['brand_category']
                update_data_instance.sku_name=str(skuname.sku_name)
                update_data_instance.sku_code=skucode
                update_data_instance.sales_type = str('local sales hawker')
                if float(row['local_sales_hawker']) != 0:
                    update_data_instance.save()
                data_changes.append({'key':'local_sales_hawker','old_value':sale_data.local_sales_hawker if sale_data else 0,'new_value':row['local_sales_hawker']}) 
            record_data['local_sales_hawker']= row['local_sales_hawker']
            
            if  ((sale_data.outstation_sales_reatil  if sale_data else 0) !=float(row['outstation_sales_reatil']))  or (not sale_data):
                update_data_instance = Weeklysales_update_log()
                update_data_instance.sku_id=row['sku_id']
                update_data_instance.wd_id=row['wd_username']
                update_data_instance.wd_town_id=wdobj.wd_town_id
                update_data_instance.branch_id = branch.region
                update_data_instance.previous_quantity=str(sale_data.outstation_sales_reatil  if sale_data else 0)
                update_data_instance.new_quantity=row['outstation_sales_reatil']
                update_data_instance.year=str(row['year'])
                update_data_instance.month=row['month']
                update_data_instance.week=row['week_num']
                update_data_instance.transaction_type=tracationtype
                update_data_instance.brand_category=row['brand_category']
                update_data_instance.sku_name=str(skuname.sku_name)
                update_data_instance.sku_code=skucode
                update_data_instance.sales_type = str('outstation sales reatil')
                if float(row['outstation_sales_reatil']) != 0:
                    update_data_instance.save()
                data_changes.append({'key':'outstation_sales_reatil','old_value':sale_data.outstation_sales_reatil  if sale_data else 0,'new_value':row['outstation_sales_reatil']})
            record_data['outstation_sales_reatil']= row['outstation_sales_reatil']
            
            if ((sale_data.outstation_sales_dealer if sale_data else 0) !=float(row['outstation_sales_dealer'])) or (not sale_data):
                update_data_instance = Weeklysales_update_log()
                update_data_instance.sku_id=row['sku_id']
                update_data_instance.wd_id=row['wd_username']
                update_data_instance.wd_town_id=wdobj.wd_town_id
                update_data_instance.branch_id = branch.region
                update_data_instance.previous_quantity=str(sale_data.outstation_sales_dealer if sale_data else 0)
                update_data_instance.new_quantity=row['outstation_sales_dealer']
                update_data_instance.year=str(row['year'])
                update_data_instance.month=row['month']
                update_data_instance.week=row['week_num']
                update_data_instance.transaction_type=tracationtype
                update_data_instance.brand_category=row['brand_category']
                update_data_instance.sku_name=str(skuname.sku_name)
                update_data_instance.sku_code=skucode
                update_data_instance.sales_type = str('outstation sales dealer')
                if float(row['outstation_sales_dealer']) != 0:
                    update_data_instance.save()
                data_changes.append({'key':'outstation_sales_dealer','old_value':sale_data.outstation_sales_dealer if sale_data else 0,'new_value':row['outstation_sales_dealer']})
            record_data['outstation_sales_dealer']= row['outstation_sales_dealer']
            
            if ((sale_data.outstation_sales_modern_trade if sale_data else 0) !=float(row['outstation_sales_modern_trade'])) or (not sale_data):
                update_data_instance = Weeklysales_update_log()
                update_data_instance.sku_id=row['sku_id']
                update_data_instance.wd_id=row['wd_username']
                update_data_instance.wd_town_id=wdobj.wd_town_id
                update_data_instance.branch_id = branch.region
                update_data_instance.previous_quantity=str(sale_data.outstation_sales_modern_trade if sale_data else 0)
                update_data_instance.new_quantity=row['outstation_sales_modern_trade']
                update_data_instance.year=str(row['year'])
                update_data_instance.month=row['month']
                update_data_instance.week=row['week_num']
                update_data_instance.transaction_type=tracationtype
                update_data_instance.brand_category=row['brand_category']
                update_data_instance.sku_name=str(skuname.sku_name)
                update_data_instance.sku_code=skucode
                update_data_instance.sales_type = str('outstation sales modern trade')
                if float(row['outstation_sales_modern_trade']) != 0:
                    update_data_instance.save()
                data_changes.append({'key':'outstation_sales_modern_trade','old_value':sale_data.outstation_sales_modern_trade if sale_data else 0,'new_value':row['outstation_sales_modern_trade']})
            record_data['outstation_sales_modern_trade']=row['outstation_sales_modern_trade']
            
            if ((sale_data.outstation_sales_hawker  if sale_data else 0) !=float(row['outstation_sales_hawker'])) or (not sale_data):
                update_data_instance = Weeklysales_update_log()
                update_data_instance.sku_id=row['sku_id']
                update_data_instance.wd_id=row['wd_username']
                update_data_instance.wd_town_id=wdobj.wd_town_id
                update_data_instance.branch_id = branch.region
                update_data_instance.previous_quantity=str(sale_data.outstation_sales_hawker  if sale_data else 0)
                update_data_instance.new_quantity=row['outstation_sales_hawker']
                update_data_instance.year=str(row['year'])
                update_data_instance.month=row['month']
                update_data_instance.week=row['week_num']
                update_data_instance.transaction_type=tracationtype
                update_data_instance.brand_category=row['brand_category']
                update_data_instance.sku_name=str(skuname.sku_name)
                update_data_instance.sku_code=skucode
                update_data_instance.sales_type = str('outstation sales hawker')
                if float(row['outstation_sales_hawker']) != 0:
                    update_data_instance.save()
                data_changes.append({'key':'outstation_sales_hawker','old_value':sale_data.outstation_sales_hawker  if sale_data else 0,'new_value':row['outstation_sales_hawker']})
            record_data['outstation_sales_hawker']= row['outstation_sales_hawker']
            
            if ((sale_data.other_sales_retail if sale_data else 0) !=float(row['other_sales_retail'])) or (not sale_data):
                update_data_instance = Weeklysales_update_log()
                update_data_instance.sku_id=row['sku_id']
                update_data_instance.wd_id=row['wd_username']
                update_data_instance.wd_town_id=wdobj.wd_town_id
                update_data_instance.branch_id = branch.region
                # if update_data_instance.previous_quantity !=None:
                update_data_instance.previous_quantity=str(sale_data.other_sales_retail if sale_data else 0)
                update_data_instance.new_quantity=row['other_sales_retail']
                update_data_instance.year=str(row['year'])
                update_data_instance.month=row['month']
                update_data_instance.week=row['week_num']
                update_data_instance.transaction_type=tracationtype
                update_data_instance.brand_category=row['brand_category']
                update_data_instance.sku_name=str(skuname.sku_name)
                update_data_instance.sku_code=skucode
                update_data_instance.sales_type = str('other sales retail')
                if float(row['other_sales_retail']) != 0:
                    update_data_instance.save()
                data_changes.append({'key':'other_sales_retail','old_value':sale_data.other_sales_retail if sale_data else 0,'new_value':row['other_sales_retail']})
            record_data['other_sales_retail']= row['other_sales_retail']
            
            if  ((sale_data.other_sales_dealer if  sale_data else 0) !=float(row['other_sales_dealer'])) or (not sale_data):
                update_data_instance = Weeklysales_update_log()
                update_data_instance.sku_id=row['sku_id']
                update_data_instance.wd_id=row['wd_username']
                update_data_instance.wd_town_id=wdobj.wd_town_id
                update_data_instance.branch_id = branch.region
                update_data_instance.previous_quantity=str(sale_data.other_sales_dealer if  sale_data else 0)
                update_data_instance.new_quantity=row['other_sales_dealer']
                update_data_instance.year=str(row['year'])
                update_data_instance.month=row['month']
                update_data_instance.week=row['week_num']
                update_data_instance.transaction_type=tracationtype
                update_data_instance.brand_category=row['brand_category']
                update_data_instance.sku_name=str(skuname.sku_name)
                update_data_instance.sku_code=skucode
                update_data_instance.sales_type = str('other sales dealer')
                if float(row['other_sales_dealer']) != 0:
                    update_data_instance.save()
                data_changes.append({'key':'other_sales_dealer','old_value':sale_data.other_sales_dealer if  sale_data else 0,'new_value':row['other_sales_dealer']})  
            record_data['other_sales_dealer']= row['other_sales_dealer']
            
            if  ((sale_data.other_sales_modern_trade if sale_data else 0) !=float(row['other_sales_modern_trade'])) or (not sale_data):
                update_data_instance = Weeklysales_update_log()
                update_data_instance.sku_id=row['sku_id']
                update_data_instance.wd_id=row['wd_username']
                update_data_instance.wd_town_id=wdobj.wd_town_id
                update_data_instance.branch_id = branch.region
                update_data_instance.previous_quantity=str(sale_data.other_sales_modern_trade if sale_data else 0)
                update_data_instance.new_quantity=row['other_sales_modern_trade']
                update_data_instance.year=str(row['year'])
                update_data_instance.month=row['month']
                update_data_instance.week=row['week_num']
                update_data_instance.transaction_type=tracationtype
                update_data_instance.brand_category=row['brand_category']
                update_data_instance.sku_name=str(skuname.sku_name)
                update_data_instance.sku_code=skucode
                update_data_instance.sales_type = str('other sales modern trade')
                if float(row['other_sales_modern_trade']) != 0:
                    update_data_instance.save()
                data_changes.append({'key':'other_sales_modern_trade','old_value':sale_data.other_sales_modern_trade if sale_data else 0,'new_value':row['other_sales_modern_trade']})
            record_data['other_sales_modern_trade']= row['other_sales_modern_trade']
            
            if ((sale_data.other_issues_other if sale_data else 0) !=float(row['other_issues_other'])) or (not sale_data):
                update_data_instance = Weeklysales_update_log()
                update_data_instance.sku_id=row['sku_id']
                update_data_instance.wd_id=row['wd_username']
                update_data_instance.wd_town_id=wdobj.wd_town_id
                update_data_instance.branch_id = branch.region
                update_data_instance.previous_quantity=str(sale_data.other_issues_other if sale_data else 0)
                update_data_instance.new_quantity=row['other_issues_other']
                update_data_instance.year=str(row['year'])
                update_data_instance.month=row['month']
                update_data_instance.week=row['week_num']
                update_data_instance.transaction_type=tracationtype
                update_data_instance.brand_category=row['brand_category']
                update_data_instance.sku_name=str(skuname.sku_name)
                update_data_instance.sku_code=skucode
                update_data_instance.sales_type = str('other issues other')
                if float(row['other_issues_other']) != 0:
                    update_data_instance.save()
                data_changes.append({'key':'other_issues_other','old_value':sale_data.other_issues_other if sale_data else 0,'new_value':row['other_issues_other']})
            record_data['other_issues_other']= row['other_issues_other']
            
            if  ((sale_data.other_issues_damage if sale_data else 0) !=float(row['other_issues_damage']))  or (not sale_data):
                update_data_instance = Weeklysales_update_log()
                update_data_instance.sku_id=row['sku_id']
                update_data_instance.wd_id=row['wd_username']
                update_data_instance.wd_town_id=wdobj.wd_town_id
                update_data_instance.branch_id = branch.region
                update_data_instance.previous_quantity=str(sale_data.other_issues_damage if sale_data else 0)
                update_data_instance.new_quantity=row['other_issues_damage']
                update_data_instance.year=str(row['year'])
                update_data_instance.month=row['month']
                update_data_instance.week=row['week_num']
                update_data_instance.transaction_type=tracationtype
                update_data_instance.brand_category=row['brand_category']
                update_data_instance.sku_name=str(skuname.sku_name)
                update_data_instance.sku_code=skucode
                update_data_instance.sales_type = str('other issues damage')
                if float(row['other_issues_damage']) != 0:
                    update_data_instance.save()
                data_changes.append({'key':'other_issues_damage','old_value':sale_data.other_issues_damage if sale_data else 0,'new_value':row['other_issues_damage']})
            record_data['other_issues_damage']= row['other_issues_damage']
            
            if  ((sale_data.other_issues_return if sale_data else 0) !=float(row['other_issues_return'])) or (not sale_data):
                update_data_instance = Weeklysales_update_log()
                update_data_instance.sku_id=row['sku_id']
                update_data_instance.wd_id=row['wd_username']
                update_data_instance.wd_town_id=wdobj.wd_town_id
                update_data_instance.branch_id = branch.region
                    
                update_data_instance.previous_quantity=str(sale_data.other_issues_return if sale_data else 0)
                update_data_instance.new_quantity=row['other_issues_return']
                update_data_instance.year=str(row['year'])
                update_data_instance.month=row['month']
                update_data_instance.week=row['week_num']
                update_data_instance.transaction_type=tracationtype
                update_data_instance.brand_category=row['brand_category']
                update_data_instance.sku_name=str(skuname.sku_name)
                update_data_instance.sku_code=skucode
                update_data_instance.sales_type = str('other issues return')
                if float(row['other_issues_return']) != 0:
                    update_data_instance.save()
                data_changes.append({'key':'other_issues_return','old_value':sale_data.other_issues_return if sale_data else 0,'new_value':row['other_issues_return']})
            record_data['other_issues_return']= row['other_issues_return']
            
            # if  ((sale_data.transaction_source if sale_data else 0) !=row['transaction_source']) or (not sale_data):
            #     update_data_instance = Weeklysales_update_log()
            #     update_data_instance.sku_id=row['sku_id']
            #     update_data_instance.wd_id=row['wd_username']
            #     update_data_instance.wd_town_id=wdobj.wd_town_id
            #     update_data_instance.branch_id = branch.region
            #     update_data_instance.previous_quantity=str(sale_data.transaction_source if sale_data else 0)
            #     update_data_instance.new_quantity=row['transaction_source']
            #     update_data_instance.year=str(row['year'])
            #     update_data_instance.month=row['month']
            #     update_data_instance.week=row['week_num']
            #     update_data_instance.transaction_type=tracationtype
            #     update_data_instance.brand_category=row['brand_category']
            #     update_data_instance.sku_name=str(skuname.sku_name)
            #     update_data_instance.sku_code=skucode
            #     update_data_instance.sales_type = str('transaction source')
            #     update_data_instance.save()
            #     data_changes.append({'key':'transaction_source','old_value':sale_data.transaction_source if sale_data else 0,'new_value':row['transaction_source']})
            record_data['transaction_source']= row['transaction_source']
        print(tracationtype,"===================tracationtype=")
        if tracationtype == 'DAILY':
            record_data['local_sales_retail']=row.get('local_sales_retail',0)
            record_data['local_sales_dealer']= row.get('local_sales_dealer',0)
            record_data['local_sales_modern_trade']= row.get('local_sales_modern_trade',0)
            record_data['local_sales_hawker']= row.get('local_sales_hawker',0)
            record_data['outstation_sales_reatil']= row.get('outstation_sales_reatil',0)
            record_data['outstation_sales_dealer']= row.get('outstation_sales_dealer',0)
            record_data['outstation_sales_modern_trade']=row.get('outstation_sales_modern_trade',0)
            record_data['outstation_sales_hawker']= row.get('outstation_sales_hawker',0)
            record_data['other_sales_retail']= row.get('other_sales_retail',0)
            record_data['other_sales_dealer']= row.get('other_sales_dealer',0)
            record_data['other_sales_modern_trade']= row.get('other_sales_modern_trade',0)
            record_data['other_issues_other']= row.get('other_issues_other',0)
            record_data['other_issues_damage']= row.get('other_issues_damage',0)
            record_data['other_issues_return']= row.get('other_issues_return',0)
        #record_data['status']=
        record_data['total_outstation_sales']= row.get('total_outstation_sales', 0)
        record_data['grand_total']= row.get('grand_total', 0)
        record_data['total_issue']= row.get('total_issue', 0)
        record_data['total_local_sales']= row.get('total_local_sales', 0)
        record_data['total_other_sales']= row.get('total_other_sales', 0)
        record_data['brand_category']= row['brand_category']
        record_data['freeze_status']= row['freeze_status']
        record_data['transaction_type']= tracationtype 
        record_data['cnf_id']=wdobj.cnf_id
        record_data['company']=unit_value.company
        record_data['region']= region.region
        record_data['unit_price']=float(wdobj.last_price)
        record_data['value']= float(row['grand_total']) * record_data['unit_price']
        record_data['sku_code']=  unit_value.sku_code
        record_data['sku_short_name']= unit_value.sku_short_name
        record_data['town_code']= row['town_code']
        record_data['wd_name']= wd_master.wd_name
        record_data['wd_type']= wd_master.wd_type
        record_data['town_name']= wd_master.wd_postal_code
        record_data['distrcode']= f"{row['wd_username']}-{row['town_code']}"
        record_data['status'] = True
        # print('???????????????????', sale_data)
        # print(data_changes,'zzzzzz666666666666zz')
       
        if sale_data is None:
            # print(data_changes,'zzzzzz666666666666zz')
            
            record_data['created_date']= datetime.datetime.now()   
            
            record_data['created_by']=userid
            
            serializer = SalesDataCreateWeekSerializer(data=record_data)
            if serializer.is_valid():
                # print(data_changes,'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                serializer.save()
            else:
                print(serializer.errors)
            
        # Sales Data Update
        else:
            #print('jkl1111111111111111111111update')
            # record_data.pop('transaction_source')
            record_data['last_updated']= userid
            record_data['last_updated_date']=datetime.datetime.now() 
            serilaizer = SalesDataCreateWeekSerializer(instance =sale_data, data=record_data,partial=True)
            if serilaizer.is_valid():
                # print(data_changes,'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                
                serilaizer.save()
            else:
                print(serilaizer.errors)
                
       
        
        if tracationtype == 'DAILY' and help_week[2] and str(help_week[2][1]) >= record[0]['sale_date_time'] >= str(help_week[2][0]) and record_length==count:
            print(record_length==count,"=======record_length==count========")
            
            aa = SalesData.objects.filter(transaction_type='DAILY', sales_date_time__gte = help_week[2][0],sales_date_time__lte = help_week[2][1] ,town_code = row['town_code'] ,wd_id = row['wd_username'],brand_category = row['brand_category']).values_list('sku_id', flat=True)
            print(len(list(set(aa))),"================>>")
            
            week_data_sums = SalesData.objects.filter(transaction_type='DAILY', sales_date_time__gte = help_week[2][0],sales_date_time__lte = help_week[2][1] ,town_code = row['town_code'] ,wd_id = row['wd_username'],brand_category = row['brand_category']).values('wd_id','sku_id','town_id','brand_category').annotate(Sum('local_sales_retail'),
                            Sum('local_sales_dealer'),Sum('local_sales_modern_trade'),Sum('local_sales_hawker'),Sum('total_local_sales'),Sum('outstation_sales_reatil'),
                            Sum('outstation_sales_dealer'),Sum('outstation_sales_modern_trade'),Sum('outstation_sales_hawker'),Sum('total_outstation_sales'),Sum('other_sales_retail'),Sum('other_sales_dealer'),
                            Sum('other_sales_modern_trade'),Sum('total_other_sales'),Sum('other_issues_damage'),Sum('other_issues_return'),Sum('other_issues_other'),Sum('total_issue'),Sum('grand_total'))
            print(len(week_data_sums),"===============>>")
            # breakpoint()
            sum_weekly_data(week_data_sums, row, help_week, wd_master,row['town_code'],userid)
    return data_changes
        

def Weekly_roll_over_log_func(exist_weekly_sales_obj, new_record_df, record, request_user, month, year, week_num):
    ''' 
        this will be execuated only for branch user
        sales log should be roolover weekly sales
        if "check_current_week[1]" this value will None then this condition run forword.
    '''
    
    old_weekly_sales_obj_df = pd.DataFrame(exist_weekly_sales_obj) #old=====
    # new_record_df = new_record_df #new=====
    
    # print(old_weekly_sales_obj_df['created_date'],"========//--------")
    # old_weekly_sales_obj_df = old_weekly_sales_obj_df[new_record_df_column_list]
    
  
    old_data_df = old_weekly_sales_obj_df
    new_data_df = new_record_df.drop([
            'wd_id','created_date','grand_total','town_code','brand_category','freeze_status','transaction_source',
            'sales_date_time','transaction_type','region','town_name','created_by','wd_type','wd_name',
            'gpi_state','statename','company','cnf_id','unit_price','value',
            'total_local_sales','total_outstation_sales','total_other_sales','total_issue','town_id','status'
        ], axis =1)
    new_record_df_col_list = list(new_record_df.columns)
    new_record_df_column_list = list(new_data_df.columns)
    combined_data_df = pd.concat([old_data_df, new_data_df]).drop_duplicates(keep='last')
    # print(combined_data_df,"=======")
    new_filter_data = combined_data_df.drop_duplicates(subset=['sku_id','sku_code'],  keep='last', inplace=False, ignore_index=False)
    column_list = combined_data_df.columns
    
    old_data_df = pd.DataFrame(columns=new_record_df_column_list) if not exist_weekly_sales_obj else old_data_df
    
    
    for index, new_row in new_filter_data.iterrows():
        # print(index,"====//==",new_row)
        new_row = new_row.to_dict()
        old_row=old_data_df.loc[(old_data_df['sku_id'] == new_row["sku_id"]) & (old_data_df['sku_code'] == new_row["sku_code"])].to_dict('records')
        
        for column in new_record_df_column_list:
            if not old_row :
                # do not insert common column
                if column == 'sku_id' or column == 'sku_code' or column == 'sku_short_name' or column == 'town_id':
                    continue
                
                print("==========kkkk")
                update_data_instance = Weeklysales_update_log()
                update_data_instance.wd_id = record[0]['wd_username']
                update_data_instance.sku_id = new_row['sku_id']
                # update_data_instance.wd_town_id = new_row['town_id']
                update_data_instance.branch_id = request_user.user_id
                update_data_instance.previous_quantity = 0
                update_data_instance.new_quantity = new_row[column]
                update_data_instance.sales_type = column
                update_data_instance.month = month
                update_data_instance.week = week_num
                update_data_instance.year = year
                update_data_instance.transaction_type = week_num
                update_data_instance.brand_category = record[0]['brand_category']
                update_data_instance.sku_name = new_row['sku_short_name']
                update_data_instance.sku_code = new_row['sku_code']
                update_data_instance.updated_date = datetime.datetime.now()
                if float(update_data_instance.new_quantity) > 0:
                    update_data_instance.save()
            elif new_row[column] == old_row[0][column]:
                continue
            else:
                                
                update_data_instance_exist = Weeklysales_update_log()
                update_data_instance_exist.wd_id = record[0]['wd_username']
                update_data_instance_exist.sku_id = new_row['sku_id']
                # update_data_instance_exist.wd_town_id = new_row['town_id']
                update_data_instance_exist.branch_id = request_user.user_id
                update_data_instance_exist.previous_quantity = str(round(float(old_row[0][column]),3))
                update_data_instance_exist.new_quantity = new_row[column]
                update_data_instance_exist.sales_type = column
                update_data_instance_exist.month = month
                update_data_instance_exist.week = week_num
                update_data_instance_exist.year = year
                update_data_instance_exist.transaction_type = week_num
                update_data_instance_exist.brand_category = record[0]['brand_category']
                update_data_instance_exist.sku_name = new_row['sku_short_name']
                update_data_instance_exist.sku_code = new_row['sku_code']
                update_data_instance_exist.updated_date = datetime.datetime.now()
                update_data_instance_exist.save()
        
def sum_weekly_data_new(week_data_sums,wd_id,town_code,help_week,my_eng,brand_category,request_user):
    # sales_hierarchy_master = Sales_Hierarchy_Master.objects.all(wd_id = wd_id,town_code__icontains = town_code).values()
    sales_hierarchy_master = Sales_Hierarchy_Master.objects.filter(wd_id = wd_id,town_code__icontains = town_code)
    mapping_master = WdSkuCatagory.objects.filter(wd_town_id__in = sales_hierarchy_master.values_list('wd_town_id', flat= True)).values()
    sales_hierarchy_master = sales_hierarchy_master.values()
    wd_master = WDmaster.objects.all().values()
    # mapping_master = WdSkuCatagory.objects.all().values()
    product_master = SKU_Master_Product.objects.all().values()
    
    sales_hierarchy_master_df = pd.DataFrame(sales_hierarchy_master)
    sales_hierarchy_master_df = sales_hierarchy_master_df.rename({'town':'town_name','wd_town_id':'town_id'}, axis=1)
    sales_hierarchy_master_unique_town_id_df = sales_hierarchy_master_df.drop_duplicates(subset=['town_name','town_id'], keep='last')
    # sales_hierarchy_master_unique_town_id_df = sales_hierarchy_master_df.groupby(['town_name','wd_id']).tail(1)
    # sales_hierarchy_master_unique_town_wd_df = sales_hierarchy_master_df.groupby(['town_name','wd_id','town_id']).tail(1)
    
    # sales_hierarchy_master_unique_town_id_df.to_csv('heirarchy.xls', header=True, index=False)
    # df.drop(columns=['column_nameA', 'column_nameB'])

    wd_master_df = pd.DataFrame(wd_master)
    wd_master_df = wd_master_df.rename({'wd_ids':'wd_id','wd_state':'gpi_state',}, axis=1)
    product_master_df = pd.DataFrame(product_master)        
    product_master_df = product_master_df.rename({'category_code':'brand_category'}, axis=1)
    mapping_master_df = pd.DataFrame(mapping_master)
    mapping_master_df = mapping_master_df.rename({'wd_town_id':'town_id','last_price':'unit_price'}, axis=1)
    # print("=================",mapping_master_df,"=========================ngf")
    # mapping_master_df = mapping_master_df.groupby(['town_id','sku_code']).tail(1)
    
    # take town_code as per town_id from heirarchy master =================
    heirarchy_n_mapping_merge = pd.merge(mapping_master_df,sales_hierarchy_master_unique_town_id_df[['town_id','town_code','town_name']], on = ['town_id'], how='left')
    # heirarchy_n_mapping_merge = heirarchy_n_mapping_merge.drop_duplicates()
    heirarchy_n_mapping_merge = heirarchy_n_mapping_merge.drop_duplicates(['town_id','sku_code','sku_id','town_code'],keep='last')
    
    # print("==========================######===")
    # heirarchy_n_mapping_merge = heirarchy_n_mapping_merge.groupby(['town_id','sku_code']).tail(1)
    # print(heirarchy_n_mapping_merge,'-------pp----------')
    # week_data_sum = SalesData.objects.filter(transaction_type='DAILY', sales_date_time__gte=help_week[2][0], sales_date_time__lte=help_week[2][1]).values('wd_id', 'sku_id', 'town_code', 'sku_code').annotate(Sum('local_sales_retail'),
    #                                                 Sum('local_sales_dealer'), Sum('local_sales_modern_trade'), Sum('local_sales_hawker'), Sum('total_local_sales'), Sum('outstation_sales_reatil'),
    #                                                 Sum('outstation_sales_dealer'), Sum('outstation_sales_modern_trade'), Sum('outstation_sales_hawker'), Sum('total_outstation_sales'), Sum('other_sales_retail'), Sum('other_sales_dealer'),
    #                                                 Sum('other_sales_modern_trade'), Sum('total_other_sales'), Sum('other_issues_damage'), Sum('other_issues_return'), Sum('other_issues_other'), Sum('total_issue'), Sum('grand_total'), Sum('value'))
    # print(len(week_data_sum),"--------------------------------------kk")
    # breakpoint()
    weekly_sales_df = pd.DataFrame(week_data_sums)
    weekly_sales_df = pd.merge(weekly_sales_df,wd_master_df[['wd_id','wd_type','wd_name','gpi_state']], on=['wd_id'],how='outer',suffixes = ('_left', '_right'))
    # weekly_sales_df = pd.merge(weekly_sales_df, sales_hierarchy_master_df[['wd_id','town_code','town_name','region']], on=['wd_id','town_code'], how='outer', suffixes = ('_left', '_right'))
    weekly_sales_df = pd.merge(weekly_sales_df, sales_hierarchy_master_unique_town_id_df[['wd_id','town_code','town_name','region']], on=['wd_id','town_code'], how='outer', suffixes = ('_left', '_right'))
    weekly_sales_df = pd.merge(weekly_sales_df, product_master_df[['sku_code','sku_id','sku_short_name','brand_category','company']], on=['sku_code','sku_id'], how='outer', suffixes = ('_left', '_right'))
    weekly_sales_df = pd.merge(weekly_sales_df, heirarchy_n_mapping_merge[['sku_id','sku_code','cnf_id','unit_price','town_id']], on=['sku_id','sku_code'], how='outer', suffixes = ('_left', '_right'))
    weekly_sales_df['transaction_type'] = help_week[1]
    weekly_sales_df['sales_date_time'] = help_week[2][1]
    weekly_sales_df['created_date'] = datetime.datetime.now()
    weekly_sales_df['created_by'] = request_user.user_id
    weekly_sales_df['statename'] = weekly_sales_df['gpi_state']

    weekly_sales_df_ren = weekly_sales_df.rename({'local_sales_retail__sum':'local_sales_retail',
                                                    'local_sales_dealer__sum':'local_sales_dealer',
                                                    'local_sales_modern_trade__sum':'local_sales_modern_trade',
                                                    'local_sales_hawker__sum':'local_sales_hawker',
                                                    'total_local_sales__sum':'total_local_sales',
                                                    'outstation_sales_reatil__sum':'outstation_sales_reatil',
                                                    'outstation_sales_dealer__sum':'outstation_sales_dealer',
                                                    'outstation_sales_modern_trade__sum':'outstation_sales_modern_trade',
                                                    'outstation_sales_hawker__sum':'outstation_sales_hawker',
                                                    'total_outstation_sales__sum':'total_outstation_sales',
                                                    'other_sales_retail__sum':'other_sales_retail',
                                                    'other_sales_dealer__sum':'other_sales_dealer',
                                                    'other_sales_modern_trade__sum':'other_sales_modern_trade',
                                                    'total_other_sales__sum':'total_other_sales',
                                                    'other_issues_damage__sum':'other_issues_damage',
                                                    'other_issues_return__sum':'other_issues_return',
                                                    'other_issues_other__sum':'other_issues_other',
                                                    'total_issue__sum':'total_issue',
                                                    'grand_total__sum':'grand_total',
                                                    'value__sum':'value'}, axis=1)
    # print("-------------------",weekly_sales_df_ren.columns.values.tolist(),"----------------------")
    weekly_sales_df_ren['local_sales_retail'] = weekly_sales_df_ren['local_sales_retail'].round(3)
    weekly_sales_df_ren['local_sales_dealer'] = weekly_sales_df_ren['local_sales_dealer'].round(3)
    weekly_sales_df_ren['local_sales_modern_trade'] = weekly_sales_df_ren['local_sales_modern_trade'].round(3)
    weekly_sales_df_ren['local_sales_hawker'] = weekly_sales_df_ren['local_sales_hawker'].round(3)
    weekly_sales_df_ren['total_local_sales'] = weekly_sales_df_ren['total_local_sales'].round(3)
    weekly_sales_df_ren['outstation_sales_reatil'] = weekly_sales_df_ren['outstation_sales_reatil'].round(3)
    weekly_sales_df_ren['outstation_sales_dealer'] = weekly_sales_df_ren['outstation_sales_dealer'].round(3)
    weekly_sales_df_ren['outstation_sales_modern_trade'] = weekly_sales_df_ren['outstation_sales_modern_trade'].round(3)
    weekly_sales_df_ren['outstation_sales_hawker'] = weekly_sales_df_ren['outstation_sales_hawker'].round(3)
    weekly_sales_df_ren['total_outstation_sales'] = weekly_sales_df_ren['total_outstation_sales'].round(3)
    weekly_sales_df_ren['other_sales_retail'] = weekly_sales_df_ren['other_sales_retail'].round(3)
    weekly_sales_df_ren['other_sales_dealer'] = weekly_sales_df_ren['other_sales_dealer'].round(3)
    weekly_sales_df_ren['other_sales_modern_trade'] = weekly_sales_df_ren['other_sales_modern_trade'].round(3)
    weekly_sales_df_ren['total_other_sales'] = weekly_sales_df_ren['total_other_sales'].round(3)
    
    weekly_sales_df_ren['other_issues_damage'] = weekly_sales_df_ren['other_issues_damage'].round(3)
    weekly_sales_df_ren['other_issues_return'] = weekly_sales_df_ren['other_issues_return'].round(3)
    weekly_sales_df_ren['other_issues_other'] = weekly_sales_df_ren['other_issues_other'].round(3)
    weekly_sales_df_ren['total_issue'] = weekly_sales_df_ren['total_issue'].round(3)
    
    
    week_data_sum = SalesData.objects.filter(town_code = town_code , wd_id = wd_id,brand_category = brand_category, transaction_type = help_week[1], sales_date_time__gte=help_week[2][0], sales_date_time__lte=help_week[2][1]).delete()
    # my_eng = my_eng
    weekly_sales_df_ren = weekly_sales_df_ren[weekly_sales_df_ren['wd_id'].notna()]
    weekly_sales_df_ren = weekly_sales_df_ren[weekly_sales_df_ren['sku_id'].notna()]
    weekly_sales_df_ren = weekly_sales_df_ren[weekly_sales_df_ren['town_name'].notna()]
    # weekly_sales_df_ren = weekly_sales_df_ren.drop_duplicates()
    weekly_sales_df_ren = weekly_sales_df_ren.drop_duplicates(['sku_code'], keep='last')
    
    # print(weekly_sales_df_ren,"-----------------weekly_sales_df_ren-----------------")
    # pd.merge(weekly_sales_df)
    # weekly_sales_df_ren.to_csv('file2.xls', header=True, index=False)
    # print("-------------",weekly_sales_df,"=========================")
    weekly_sales_df_ren.to_sql('transaction_salesdata', my_eng, if_exists='append', index=False)
    return None

        
def daily_weekly_sale_create_update(record, userid, location, help_week,user_type,db_engine):
    # check_current_week or not===============start
    check_current_week = help_week[2][0] if help_week[1] else datetime.datetime.now().date()
    # check_current_week or not===============end
    data_changes=[]
    weeks = ('Week1','Week2','Week3','Week4')
    request_user = userid
    record_length = len(record)
    wd_id = record[0]['wd_username']
    town_code = record[0]['town_code']
    brand_category = record[0]['brand_category']
    count = 0
    data_changes=[]
    tracationtype = 'DAILY' if record[0]['week_num'].strip()=="" else record[0]['week_num'].strip()
    record_dataframe = pd.DataFrame(record)
    wd_town_check =Sales_Hierarchy_Master.objects.filter(wd_id=wd_id,town_code__in = [town_code,re.sub('\W+','',town_code),str(town_code),str(town_code)[1:],'0'+str(town_code)])
    wd_town_list = wd_town_check.values_list('wd_town_id',flat=True)
    wd_master = WDmaster.objects.filter(wd_ids = wd_id).last()
    master_mapping = WdSkuCatagory.objects.filter(wd_town_id__in = wd_town_list)
    master_mapping_df = pd.DataFrame(master_mapping.values())
    master_mapping_df = master_mapping_df.rename({'last_price':'unit_price','wd_town_id':'town_id'}, axis=1)
    # master_mapping_df = master_mapping_df.groupby(['town_id','sku_code']).head(0)
    master_product = SKU_Master_Product.objects.all().values()
    master_product_df = pd.DataFrame(master_product)
    # wdobj = WdSkuCatagory.objects.filter(wd_town_id__in=wd_town_list,sku_id=json_data['sku_id']).last()
    # print(record,"=====================record_dataframe","------------------------------000")
    record_dataframe = record_dataframe.rename({'wd_username':'wd_id','sale_date_time':'sales_date_time'}, axis=1)
    if request_user.user_type != "WD":
        record_dataframe = record_dataframe.drop(['other_sales_hawker','week_num','year','month'], axis=1)
    elif request_user.user_type == "WD":
        record_dataframe = record_dataframe.drop(['other_sales_hawker','week_num'], axis=1)
    
    record_dataframe = record_dataframe.assign(created_date = [datetime.datetime.now() for i in range(len(record))])
    # record_dataframe = record_dataframe.assign(town_id = [wd_town_check.last().wd_town_id for i in range(len(record))])
    record_dataframe = record_dataframe.assign(transaction_type = [tracationtype for i in range(len(record))])
    record_dataframe = record_dataframe.assign(region = [wd_town_check.first().region for i in range(len(record))])
    record_dataframe = record_dataframe.assign(town_name = [wd_town_check.first().town for i in range(len(record))])
    record_dataframe = record_dataframe.assign(created_by = [request_user.user_id for i in range(len(record))])
    record_dataframe = record_dataframe.assign(wd_type = [wd_master.wd_type for i in range(len(record))])
    record_dataframe = record_dataframe.assign(wd_name = [wd_master.wd_name for i in range(len(record))])
    record_dataframe = record_dataframe.assign(gpi_state = [wd_master.wd_state for i in range(len(record))])
    record_dataframe = record_dataframe.assign(statename = [wd_master.wd_state for i in range(len(record))])
    record_dataframe['status'] = True
    record_dataframe['freeze_status'] = False
    
    record_dataframe['total_local_sales'] = record_dataframe['local_sales_retail'].astype(float) + record_dataframe['local_sales_dealer'].astype(float) + record_dataframe['local_sales_modern_trade'].astype(float) + record_dataframe['local_sales_hawker'].astype(float)
    record_dataframe['total_local_sales'] = record_dataframe['total_local_sales'].round(3)
    record_dataframe['total_outstation_sales'] = record_dataframe['outstation_sales_reatil'].astype(float) + record_dataframe['outstation_sales_dealer'].astype(float) + record_dataframe['outstation_sales_modern_trade'].astype(float) + record_dataframe['outstation_sales_hawker'].astype(float)
    record_dataframe['total_outstation_sales'] = record_dataframe['total_outstation_sales'].round(3)
    record_dataframe['total_other_sales'] = record_dataframe['other_sales_retail'].astype(float) + record_dataframe['other_sales_dealer'].astype(float) + record_dataframe['other_sales_modern_trade'].astype(float)
    record_dataframe['total_other_sales'] = record_dataframe['total_other_sales'].round(3)
    record_dataframe['grand_total'] = record_dataframe['total_local_sales'].astype(float) + record_dataframe['total_outstation_sales'].astype(float) + record_dataframe['total_other_sales'].astype(float)
    record_dataframe['grand_total'] = record_dataframe['grand_total'].round(3)
    # print(record_dataframe['sku_id'],"=====================record_dataframe")
    sku_id_list = list(record_dataframe['sku_id'])
    # my_eng = db_engine
    # my_eng = create_engine('mysql+mysqlconnector://secsales:s_ecGpi1_23@10.250.1.191:3306/gpi_ss') # UAT ----------------------
    
    # for town id validation===========start===========
    wd_town_check = pd.DataFrame(wd_town_check.values('wd_id','wd_town_id','town'))
    wd_town_check_uniques_df = wd_town_check.drop_duplicates(subset=['wd_id','wd_town_id','town'], keep='last')
    wd_town_check_uniques_rename_df = wd_town_check_uniques_df.rename(columns = {'wd_town_id':'town_id','town':'town_name'})
    town_id_code_sku_df = pd.merge(wd_town_check_uniques_rename_df,master_mapping_df[['town_id','sku_id']], on = 'town_id', how='left')
    town_id_code_sku_unique_df = town_id_code_sku_df.drop_duplicates(subset=['wd_id','town_id','town_name','sku_id'])
    # for town id validation=============end=========
    
    
    if tracationtype == 'DAILY':
        print(record_dataframe['local_sales_modern_trade'].astype(float),"--------------------------record_dataframe['local_sales_modern_trade'].astype(float)")
        sale_date_time = record[0]['sale_date_time']
        pas_sale_data = SalesData.objects.filter(wd_id__icontains = wd_id, sku_id__in = sku_id_list, sales_date_time = sale_date_time, transaction_type__icontains = tracationtype, town_code__icontains = town_code, brand_category__icontains = brand_category).delete()

        record_dataframe = pd.merge(record_dataframe,master_product_df[['sku_short_name','sku_id','company']], on=['sku_id'],  how='outer', suffixes = ('_left', '_right') )
        
        df2 = master_mapping_df[master_mapping_df['sku_id'].isin(sku_id_list)]
        mast = df2[['cnf_id', 'unit_price','sku_id']]
        
        mergedRes = pd.merge(record_dataframe, mast, on ='sku_id')
        # mergedRes.to_csv('file2.csv', header=True, index=False)
        mergedRes['value'] = mergedRes['unit_price'] * mergedRes['grand_total']
        
        mergedRes = pd.merge(mergedRes, town_id_code_sku_unique_df[['town_id','sku_id']], on='sku_id' ,how='left')
        
        print(mergedRes,'.................>>>>>>>>>>>>>>>>>>>>>>============mergedRes')
        mergedRes = mergedRes.drop_duplicates(['sku_code'], keep='last')

        # record_dataframe = pd.merge(record_dataframe,master_mapping_df[['sku_id','town_id','unit_price','cnf_id']], on=['sku_id','town_id'],  how='outer', suffixes = ('_left', '_right') )
        # # print("ppppppppppppppppp",record_dataframe['sku_id','town_id','unit_price','cnf_id'],"----------------------------record_dataframe")
        # record_dataframe = pd.merge(record_dataframe,master_product_df[['sku_short_name','sku_id','company']], on=['sku_id'],  how='outer', suffixes = ('_left', '_right') )

        
        # record_dataframe = pd.merge(record_dataframe,master_mapping_df[['sku_id','town_id','unit_price','cnf_id']], on=['sku_id','town_id'],  how='outer', suffixes = ('_left', '_right') )
        # print("ppppppppppppppppp",record_dataframe['sku_id','town_id','unit_price','cnf_id'],"----------------------------record_dataframe")
        mergedRes.to_sql('transaction_salesdata', my_eng, if_exists='append', index=False)
        
        
    else :
        # print("-----------------------------------kkkk---------------------------------",tracationtype)
        week_num = record[0]['week_num']
        if request_user.user_type == "BRANCH USER":
            print("----------bu-----------------------")
            year = record[0]['year']
            month = record[0]['month']
            week_date_and_freeze_status = freeze_status_val_weekly_and_date(year,month,week_num)
            print('weekly',week_date_and_freeze_status)
            # weeklastdate = help_week[2][1]
            # weekstartdate = help_week[2][0]
            weeklastdate = week_date_and_freeze_status[1][1]
            weekstartdate = week_date_and_freeze_status[1][0]
        else:
            help_week = week_sele_before_date(request_user.user_type)
            weeklastdate = help_week[2][1]
            print("-----------------wd---------------------",weeklastdate)
            # weekstartdate = week_date_and_freeze_status[1][0]
        # past_date = (datetime.datetime.now() - datetime.timededaily_weekly_sale_create_updatelta(days=70)).date()
        sale_date_time = record[0]['sale_date_time']
        weekly_sales_obj = SalesData.objects.filter(wd_id__icontains = wd_id, sku_id__in = sku_id_list, sales_date_time = weeklastdate, transaction_type__icontains = tracationtype, town_code__icontains = town_code, brand_category__icontains = brand_category)
        exist_weekly_sales_obj = weekly_sales_obj.values()
        record_dataframe = pd.merge(record_dataframe,master_product_df[['sku_short_name','sku_id','company']], on=['sku_id'],  how='outer', suffixes = ('_left', '_right') )
        
        df2 = master_mapping_df[master_mapping_df['sku_id'].isin(sku_id_list)]
        mast = df2[['cnf_id', 'unit_price','sku_id']]
        record_dataframe['sales_date_time'] = weeklastdate
        record_dataframe['transaction_type'] = week_num
        mergedRes = pd.merge(record_dataframe, mast, on ='sku_id')
        # mergedRes.to_csv('file2.csv', header=True, index=False)
        mergedRes['value'] = mergedRes['unit_price'] * mergedRes['grand_total']
        
        mergedRes = pd.merge(mergedRes, town_id_code_sku_unique_df[['town_id','sku_id']], on='sku_id' ,how='left')
        
        new_record_df = mergedRes
        print('file_generate',"==============/////===========","file_generate")
        mergedRes = mergedRes.drop_duplicates(['sku_code'], keep='last')
        # weekly rool over sale email insert in weekly log ====================
        if tracationtype != 'DAILY' and user_type != 'WD' and parse(str(weeklastdate)).date() < check_current_week:
            roolover_weekly_log = Weekly_roll_over_log_func(exist_weekly_sales_obj, new_record_df, record, request_user, month, year, week_num)
        
        weekly_sales_obj.delete()
        mergedRes.to_sql('transaction_salesdata', my_eng, if_exists='append', index=False)
        
        
        # roolover weekly sales modified by only "BRANCH USER"======= end
            
    
    if tracationtype == 'DAILY' and help_week[2] and str(help_week[2][1]) >= record[0]['sale_date_time'] >= str(help_week[2][0]):
        # print("----------------",help_week,"-------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>-")
        
        # aa = SalesData.objects.filter(transaction_type='DAILY', sales_date_time__gte = help_week[2][0],sales_date_time__lte = help_week[2][1] ,town_code = row['town_code'] ,wd_id = row['wd_username'],brand_category = row['brand_category']).values_list('sku_id', flat=True)
        # print(len(list(set(aa))),"================>>")
        
        week_data_sums = SalesData.objects.filter(transaction_type='DAILY', sales_date_time__gte = help_week[2][0],sales_date_time__lte = help_week[2][1] ,town_code = town_code , wd_id = wd_id,brand_category = brand_category).values('wd_id','sku_id','town_code','sku_code').annotate(Sum('local_sales_retail'),
                        Sum('local_sales_dealer'),Sum('local_sales_modern_trade'),Sum('local_sales_hawker'),Sum('total_local_sales'),Sum('outstation_sales_reatil'),
                        Sum('outstation_sales_dealer'),Sum('outstation_sales_modern_trade'),Sum('outstation_sales_hawker'),Sum('total_outstation_sales'),Sum('other_sales_retail'),Sum('other_sales_dealer'),
                        Sum('other_sales_modern_trade'),Sum('total_other_sales'),Sum('other_issues_damage'),Sum('other_issues_return'),Sum('other_issues_other'),Sum('total_issue'),Sum('grand_total'),Sum('value'))
        
        sum_weekly_data_new(week_data_sums,wd_id,town_code,help_week,my_eng,brand_category,request_user)
    
    return None