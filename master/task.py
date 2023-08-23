import datetime
from celery import shared_task
# from secondary_sales import settings
from django.core.mail import send_mail
from django.conf import settings
import re
# =====================
import json
import logging
import requests
from itertools import chain
from django.db.models import Q
import pandas as pd
from dateutil.parser import parse
from master.thread import SaleData_create, SaleData_update
from master.utils import count_invalid_sale_date_wise, count_success_sale_date_wise, create_update_weekly
from master.views import emailsend_zoro_or_running

from wd.helper import week_sele_before_date
logger = logging.getLogger(__name__)
from django.http import HttpResponse
from django.core.mail import EmailMessage
from base.models import BranchMaster, User, WDmaster
from secondary_sales.settings import *
from django.core import mail
from master.models import Apistatus, Integration_log_details, Integration_log_summary, Invalid_log_data, Repeat_count, SKU_Master_Product, Sales_Hierarchy_Master, SalesData, Temp_Total_sku_sales, WdSkuCatagory
from master.serializers import Integration_log_detailsSerializers, Integration_log_summarySerializers, Invalid_log_dataSerializers, Repeat_countSerializers, SalesDataSerializer, Temp_Total_sku_salesSerializer
from django.db.models import Sum
from django.db.models import Q
from .email_sub import surya_success_sub,surya_failed_sub,sfa_success_sub,sfa_failed_sub,success_email_list,failed_list,cc_list,test_sch
from .test_json import distributer_sale as ds

@shared_task(bind=True)
def Sfa_api(self):
    try:
        print('success_count',"========success_count=========")
        # print(aa = 66)
        # breakpoint()
        # url = 'https://uat.lakshya.rsr.cloware.com/secondarysync/secondary_sales/0'
        # hashers = {'Authorization':'Basic  U0VDT05EQVJZX0lOVEVHUkFUSU9OX1RFQU06U0VDT05EQVJZU3luYzEyMyM=','Auth-Key':'secondaryauth','Content-Type':'application/json'}
        # production=======
        url = "https://drop52.reports.cloware.com/secondarysync/secondary_sales/0"
        hashers = {'Authorization':'Basic  U0VDT05EQVJZX0lOVEVHUkFUSU9OX1RFQU06U0VDT05EQVJZU3luYzEyMyM=','Auth-Key':'secondaryauth','Content-Type':'application/json'}

        data=requests.get(url, headers=hashers)
        success_count=data.json()['data']['success_count']
        s=0
        all_data=[]
        errors_list=[]
        flag=0
        repet_flag = 0
        histry_dict={}
        error_detail_dict = {}
        len_val = 0
        town_cd =[]
        wd_list_4_week = []
        date_tuple_weekly = [8,15,22,1]
        log_list = 0
        success_list = 0

        for i in range(0,int(success_count),500):
            if s==0:
                # url = 'https://uat.lakshya.rsr.cloware.com/secondarysync/secondary_sales/0'
                url = "https://drop52.reports.cloware.com/secondarysync/secondary_sales/0"
                data=requests.get(url, headers=hashers)
                total_data=data.json()['data']['distributer_sale']
                all_data.append(total_data)
            else:
                # url = 'https://uat.lakshya.rsr.cloware.com/secondarysync/secondary_sales/'+str(i+1)
                url = "https://drop52.reports.cloware.com/secondarysync/secondary_sales/"+str(i+1)
                data=requests.get(url, headers=hashers)
                total_data=data.json()['data']['distributer_sale']
                all_data.append(total_data)
            s=s+1
        final_data=list(chain(*all_data))
        json_object = json.dumps(all_data, indent = 4)
        # n = datetime.datetime.now().date()-datetime.timedelta(days=1)
        
        with open(settings.MEDIA_ROOT + 'sfa_api_sales/'+"sfa_sales_"+str(datetime.datetime.now().date()) + '.json','w')as outfile:
            outfile.write(json_object)
        if json_object[0]:
            response = HttpResponse(content_type='text/csv')
            df = pd.DataFrame.from_dict(list(final_data))
            df.to_csv(settings.MEDIA_ROOT + 'sfa_api_sales_csv/'+"sfa_sales_"+str(datetime.datetime.now().date()) + '.csv', index = False)
        # =========testcase===========================================
        # from master import sfa
        # success_count = sfa.aa['data']['success_count']
        # final_data = sfa.aa['data']['distributer_sale']
        # print(len(sfa.aa['data']['distributer_sale']),"==========",success_count)
        # breakpoint()
        a = 0
        # ===========================end test case====================
        today_date = datetime.datetime.now()
        if json_object[0]:
            response = HttpResponse(content_type='text/csv')
            df = pd.DataFrame.from_dict(list(final_data))
            df.to_csv(settings.MEDIA_ROOT + 'sfa_api_sales_csv/'+"sfa_sales_"+str(datetime.datetime.now().date()) + '.csv', index = False)
        
        status_data = Apistatus.objects.filter(running_date=today_date.date(),api="SFA_API").last()
        running_state =  status_data.status if status_data and status_data.status == True else False
        if int(success_count) > 0  and (running_state == False) :
            aaa=Apistatus.objects.create(running_date=today_date.date(),status=True,api="SFA_API")
            trans_obj=Integration_log_summary.objects.filter(sale_date=final_data[0].get('sale_date')).last()
            temp_sale_data_objs = Temp_Total_sku_sales.objects.all()
            
            print(temp_sale_data_objs)
            temp_sale_data_objs.delete()
            Integration_log_summary.objects.all().delete()
            Integration_log_details.objects.all().delete()
            # breakpoint()
            # final_data = ds
            less_30_day = today_date.date()-datetime.timedelta(days=20)
            for json_data in final_data:
                # sales_data = SalesData.objects.filter(sales_date_time__gte = less_30_day)
                # breakpoint()
                a = a+1
                print(a,"=====================================================================================//==")
                sku_obj=SKU_Master_Product.objects.filter(sku_code__iexact=json_data['prodcode']).last()
                wd_id = json_data['distrcode'].split("-")[0]
                
                town_trim_wd = str(json_data['distrcode']).replace(json_data['town_code'],'')
                user_id = User.objects.filter(Q(user_id = wd_id)|Q(user_id = town_trim_wd)).last()
                town_cd.append(json_data['town_code'])
                wd_town_list =Sales_Hierarchy_Master.objects.filter((Q(wd_id=wd_id)|Q(wd_id = town_trim_wd)),town_code__in=[json_data['town_code'],re.sub('\W+','',json_data['town_code']),str(json_data['town_code']),str(json_data['town_code'])[1:],'0'+str(json_data['town_code'])]).values_list('wd_town_id',flat=True)
                sku_obj=SKU_Master_Product.objects.filter(sku_code__iexact=json_data['prodcode']).last()
                wd_id = json_data['distrcode'].split("-")[0]
                
                town_trim_wd = str(json_data['distrcode']).replace(json_data['town_code'],'')
                user_id = User.objects.filter(Q(user_id = wd_id)|Q(user_id = town_trim_wd)).last()
                town_cd.append(json_data['town_code'])
                # wd_town_list =Sales_Hierarchy_Master.objects.filter((Q(wd_id=wd_id)|Q(wd_id = town_trim_wd)),(Q(town_code=json_data['town_code'])|Q(town_code__iexact=json_data['town_code'])|Q(town_code__iexact=str(json_data['town_code'])[1:])|Q(town_code__iexact='0'+str(json_data['town_code'])))).values_list('wd_town_id',flat=True)
                wd_town_list =Sales_Hierarchy_Master.objects.filter((Q(wd_id=wd_id)|Q(wd_id = town_trim_wd)),town_code__in=[json_data['town_code'],re.sub('\W+','',json_data['town_code']),str(json_data['town_code']),str(json_data['town_code'])[1:],'0'+str(json_data['town_code'])]).values_list('wd_town_id',flat=True)
                wdobj = WdSkuCatagory.objects.filter(sku_code__iexact=json_data['prodcode'],wd_town_id__in=wd_town_list).last()
                sku = []
                wd = []
                town = []
                unmap_sku = []
                if not user_id:
                    wd.append(wd_id)
                elif not wd_town_list:
                    town.append(json_data['town_code'])
                elif not wdobj:
                    unmap_sku.append(json_data['prodcode'])
                elif not sku_obj:
                    sku.append(json_data['prodcode'])
                total_sale = (float(json_data.get('local_retail', 0))+float(json_data.get('local_dealer', 0))+float(json_data.get('local_MT', 0))+float(json_data.get('local_HA', 0))
                            +float(json_data.get('out_retail', 0))+float(json_data.get('out_dealer', 0))+float(json_data.get('out_MT', 0))+float(json_data.get('out_HA', 0))
                            +float(json_data.get('other_retail', 0))+float(json_data.get('other_dealer', 0))+float(json_data.get('other_MT', 0)))
                if sku_obj and wdobj and user_id and (total_sale > 0):
                    success_list = success_list + 1
                    wd_list_4_week.append(user_id.user_id)
                    
                    wds = WDmaster.objects.filter(wd_ids = user_id.user_id).last()
                    # town_nm = Sales_Hierarchy_Master.objects.filter((Q(wd_id = user_id.user_id)|Q(wd_id = town_trim_wd)),(Q(town_code__iexact=json_data['town_code'])|Q(town_code__iexact = str(json_data['town_code'])[1:])|Q(town_code__iexact='0'+str(json_data['town_code'])))).last()
                    town_nm = wd_town_list =Sales_Hierarchy_Master.objects.filter((Q(wd_id=wd_id)|Q(wd_id = town_trim_wd)),town_code__in=[json_data['town_code'],re.sub('\W+','',json_data['town_code']),str(json_data['town_code']),str(json_data['town_code'])[1:],'0'+str(json_data['town_code'])]).last()
                    if town_nm:
                        town_name = town_nm.town
                    else:
                        town_name = " "

                    if wds:
                        wd_type_master = wds.wd_type
                        wd_id_name = wds.wd_name
                    else:
                        wd_id_name = "Name not Avail in wd_master"
                        
                    json_data['distrcode'] = str(user_id.user_id)+"-"+json_data['town_code']
                    json_data['town_code'] = json_data['town_code']
                    json_data['sku_short_name'] = sku_obj.sku_short_name
                    json_data['sku_code'] = json_data['prodcode']
                    json_data['town_name'] = town_name

                    json_data['wd_name'] = wd_id_name
                    json_data['wd_type'] = wd_type_master
                    json_data['statename'] = wds.wd_state
                    json_data['sku_id'] = sku_obj.sku_id
                    json_data['town_id'] = wdobj.wd_town_id
                    json_data['wd_id'] = user_id.user_id
                    json_data['tranisition_source'] = json_data['dist_type']
                    json_data['transaction_type'] = 'DAILY'
                    json_data['created_by'] = "SFA/SFA_LITE_API"
                    json_data['brand_category'] = json_data.get('catcode')
                    json_data['created_date'] = datetime.datetime.now()
                    json_data['sales_date_time'] = json_data.get('sale_date')
                    json_data['local_sales_retail'] = json_data.get('local_retail', 0)
                    json_data['local_sales_dealer'] = json_data.get('local_dealer', 0)
                    json_data['local_sales_modern_trade'] = json_data.get('local_MT', 0)
                    json_data['local_sales_hawker'] = json_data.get('local_HA', 0)
                    json_data['outstation_sales_reatil'] = json_data.get('out_retail', 0)
                    json_data['outstation_sales_dealer'] = json_data.get('out_dealer', 0)
                    json_data['outstation_sales_modern_trade'] = json_data.get('out_MT', 0)
                    json_data['outstation_sales_hawker'] = json_data.get('out_HA', 0)
                    json_data['other_sales_retail'] = json_data.get('other_retail', 0)
                    json_data['other_sales_dealer'] = json_data.get('other_dealer', 0)
                    json_data['other_sales_modern_trade'] = json_data.get('other_MT', 0)
                    json_data['other_issues_other'] = json_data.get('other_issues_other', 0)
                    json_data['other_issues_damage'] = json_data.get('other_issued_damage', 0)
                    json_data['other_issues_return'] = json_data.get('other_issued_returns', 0)
                    # json_data['last_updated_date'] = datetime.datetime.now()
                    json_data['total_local_sales'] = float(json_data['local_sales_retail']) + float(json_data['local_sales_dealer']) +float(json_data['local_sales_modern_trade'])+float(json_data['local_sales_hawker'])
                    json_data['total_outstation_sales'] = float(json_data['outstation_sales_reatil']) +float(json_data['outstation_sales_dealer']) +float(json_data['outstation_sales_modern_trade']) +float(json_data['outstation_sales_hawker'])
                    json_data['total_other_sales'] = float(json_data['other_sales_retail']) +float(json_data['other_sales_dealer']) +float(json_data['other_sales_modern_trade'])
                    json_data['total_issue'] = float(json_data['other_issues_other']) +float(json_data['other_issues_damage']) +float(json_data['other_issues_return'])
                    json_data['grand_total'] = json_data['total_local_sales'] +json_data['total_outstation_sales'] +json_data['total_other_sales']
                    if sku_obj:
                        json_data['company'] = sku_obj.company
                    else:
                        json_data['company'] =None
                    if wdobj:
                        json_data['unit_price'] = wdobj.last_price
                        json_data['cnf_id'] = wdobj.cnf_id
                    else:
                        json_data['unit_price'] = 0
                        json_data['cnf_id'] = None
                    branch = User.objects.filter(user_id = json_data.get('wd_id'), user_type = "WD").last()
                    if branch:
                        region = BranchMaster.objects.filter(branch_code = branch.locationcode).last()
                        json_data['region'] = region.region
                    else:
                        json_data['region'] = None

                    json_data['value'] = float(json_data['unit_price']) * float(json_data['grand_total'])
                    json_data['value'] = float(json_data['unit_price']) * float(json_data['grand_total'])
                    # sales_obj = sales_data.filter(wd_id = json_data['wd_id'],sku_id = json_data['sku_id'],transaction_type = 'DAILY',sales_date_time=json_data['sales_date_time'],town_id = json_data['town_id'],town_code = json_data['town_code']).last()
                    sales_obj = SalesData.filter(wd_id = json_data['wd_id'],sku_id = json_data['sku_id'],transaction_type = 'DAILY',sales_date_time=json_data['sales_date_time'],town_id = json_data['town_id'],town_code = json_data['town_code']).last()
                    if not sales_obj:
                        SaleData_create(json_data).sale_create()
                    else:
                        SaleData_update(sales_obj,json_data).sale_update()
                    
                    # this section connented due to duplicate sale will not comming on SFA API===================== 
                    temp_sale_data = Temp_Total_sku_sales.objects.filter(wd_id = json_data['wd_id'],sku_id = json_data['sku_id'],transaction_type = 'DAILY',sales_date_time=json_data['sales_date_time'],town_id = json_data['town_id'],town_code = json_data['town_code']).last()
                    if not temp_sale_data:
                        serializer_temp_sale_data = Temp_Total_sku_salesSerializer(data = json_data, many = False)
                        if serializer_temp_sale_data.is_valid():
                            serializer_temp_sale_data.save()
                        else:
                            print(serializer_temp_sale_data.errors)
                            pass
                        # print(total_sale,"===================>>createing===================sfa======",temp_sale_data)
                        # breakpoint()
                    else:
                        # json_data['local_sales_retail'] = float(json_data['local_sales_retail']) + temp_sale_data.local_sales_retail
                        json_data['local_sales_dealer'] = float(json_data['local_sales_dealer']) + temp_sale_data.local_sales_dealer 
                        json_data['local_sales_modern_trade'] = float(json_data['local_sales_modern_trade']) + temp_sale_data.local_sales_modern_trade
                        json_data['local_sales_hawker'] = float(json_data['local_sales_hawker']) + temp_sale_data.local_sales_hawker
                        json_data['total_local_sales'] = float(json_data['local_sales_retail']) + json_data['local_sales_dealer'] +json_data['local_sales_modern_trade']+json_data['local_sales_hawker']

                        json_data['outstation_sales_reatil'] = float(json_data['outstation_sales_reatil']) + temp_sale_data.outstation_sales_reatil
                        json_data['outstation_sales_dealer'] = float(json_data['outstation_sales_dealer']) + temp_sale_data.outstation_sales_dealer
                        json_data['outstation_sales_modern_trade'] = float(json_data['outstation_sales_modern_trade']) + temp_sale_data.outstation_sales_modern_trade
                        json_data['outstation_sales_hawker'] = float(json_data['outstation_sales_hawker']) + temp_sale_data.outstation_sales_hawker
                        json_data['total_outstation_sales'] = float(json_data['outstation_sales_reatil']) + json_data['outstation_sales_dealer'] + json_data['outstation_sales_modern_trade'] + json_data['outstation_sales_hawker']

                        json_data['other_sales_retail'] = float(json_data['other_sales_retail']) + temp_sale_data.other_sales_retail
                        json_data['other_sales_dealer'] = float(json_data['other_sales_dealer']) + temp_sale_data.other_sales_dealer
                        json_data['other_sales_modern_trade'] = float(json_data['other_sales_modern_trade']) + temp_sale_data.other_sales_modern_trade
                        json_data['total_other_sales'] = float(json_data['other_sales_retail']) + json_data['other_sales_dealer'] + json_data['other_sales_modern_trade']

                        json_data['other_issues_damage'] = float(json_data['other_issues_damage']) + temp_sale_data.other_issues_damage
                        json_data['other_issues_return'] = float(json_data['other_issues_return']) + temp_sale_data.other_issues_return
                        json_data['other_issues_other'] = float(json_data['other_issues_other']) + temp_sale_data.other_issues_other
                        json_data['total_issue'] = json_data['other_issues_damage'] + json_data['other_issues_return']+json_data['other_issues_other']

                        json_data['grand_total'] = json_data['total_local_sales'] +json_data['total_outstation_sales'] +json_data['total_other_sales']
                        json_data['value'] = float(json_data['unit_price']) * float(json_data['grand_total'])

                        if wdobj:
                            json_data['unit_price'] = wdobj.last_price
                            json_data['cnf_id'] = wdobj.cnf_id
                        else:
                            json_data['unit_price'] = 0
                            json_data['cnf_id'] = None
                        json_data.pop('created_by')
                        json_data.pop('sales_date_time')
                        json_data.pop('created_date')
                        json_data['last_updated'] = "SFA/SFA_LITE_API"
                        json_data['last_updated_date'] = datetime.datetime.now()
                        serializer_temp_sale_data = Temp_Total_sku_salesSerializer(temp_sale_data,data = json_data, partial = True)
                        if serializer_temp_sale_data.is_valid():
                            serializer_temp_sale_data.save()
                    
                    count_success_sale_date_wise(today_date, json_data.get('sale_date'))
                    
                else:
                    count_invalid_sale_date_wise(today_date, json_data.get('sale_date'))
                    
                    log_list = log_list+1
                    # print("=======00=======")
                    # json_data['transaction_source'] = "SFA/SFA_LITE_API"
                    # log_data_serializer = Invalid_log_dataSerializers(data = json_data)
                    # if log_data_serializer.is_valid():
                    #     log_data_serializer.save()
                        
                        
                    # breakpoint()
                    len_val=len_val+1
                    errors_list.append(json_data)
                    # const_time = datetime.datetime(2009, 10, 5, 00, 00, 00)
                    # wdid_town = json_data['distrcode'].split("-")
                    error_detail_dict['sku_id'] = json_data['prodcode']
                    error_detail_dict['wd_id'] = json_data['dist_id']
                    error_detail_dict['town_id'] = json_data['town_code']

                    if total_sale == 0:
                        error_detail_dict['reason'] = str(wd_id) +" "+" Received '0' sales for SKU "+ str(json_data['prodcode'])
                    elif len(wd)>0:
                        error_detail_dict['reason'] = str(wd_id) +" "+" wd_id is not present in user_master database."
                        print("===========ss",str(wd_id) +" "+" wd_id is not present in user_master database.")
                        # error_detail_dict['repeat_count'] = len_val
                    elif len(town)>0:
                        error_detail_dict['reason'] = str(wd_id)+ " WD_id is not mapped with " + str(json_data['town_code'])+" town code."
                        print("----------------------rrrr",str(wd_id)+ " WD_id is not mapped with " + str(json_data['town_code'])+" town code.")
                        
                    elif len(unmap_sku) > 0:
                        error_detail_dict['reason'] = str(json_data['prodcode']) +" sku_code is not mapped with "+ str(wd_id) +" wd_id in SS_database:Sales_Hierarchy_Master"
                        print("===========ss",str(json_data['prodcode']) +" sku_code is not mapped with "+ str(wd_id) +" wd_id in SS_database:Sales_Hierarchy_Master")
                        
                    elif len(sku)>0:
                        error_detail_dict['reason'] = str(json_data['prodcode']) +" "+ " sku_code is not present in sku_master database: sku_master"
                        print("===============88",str(json_data['prodcode']) +" "+ " sku_code is not present in sku_master database: sku_master")
                        # error_detail_dict['repeat_count'] = len_val
                    else:
                        # error_detail_dict['repeat_count'] = len_val
                        error_detail_dict['reason'] = str(json_data['town_code']) +"This towm_code is not mapped with any WD"

                    error_detail_dict['tranisition_source'] = "SFA/SFA_LITE_API"
                    # comb_d_t = datetime.datetime.combine(parse(final_data[0].get('sale_date')), const_time.time())
                    comb_d_t = parse(json_data['sale_date'])
                    # print(comb_d_t)
                    error_detail_dict['sales_date_time'] = comb_d_t
                    log_detail = Integration_log_details.objects.filter(tranisition_source = "SFA/SFA_LITE_API",sales_date_time = comb_d_t, sku_id = json_data['prodcode'],town_id = json_data['town_code']).last()
                    if log_detail:
                        # error_detail_dict['repeat_count'] = int(log_detail.repeat_count) +1
                        log_serializer = Integration_log_detailsSerializers(log_detail, data = error_detail_dict, partial=True)
                        
                        if log_serializer.is_valid():
                            
                            log_serializer.save()
                    else:
                        # print(error_detail_dict,"======error_detail_dict======")
                        error_detail_dict['repeat_count'] = 1
                        error_detail_dict['created_date'] = today_date
                        log_serializer = Integration_log_detailsSerializers(data = error_detail_dict)
                        
                        if log_serializer.is_valid():
                            
                            log_serializer.save()
                        else:
                            pass
                            # return Response(log_serializer.errors)
                
            from_temp_sale = Temp_Total_sku_sales.objects.all().values('brand_category','sku_id','wd_id','town_id','sales_date_time',
                                                            'local_sales_retail','local_sales_dealer','local_sales_modern_trade','local_sales_hawker','total_local_sales',
                                                            'outstation_sales_reatil','outstation_sales_dealer','outstation_sales_modern_trade','outstation_sales_hawker','total_outstation_sales',
                                                            'other_sales_retail','other_sales_dealer','other_sales_modern_trade','total_other_sales',
                                                            'other_issues_damage','other_issues_return','other_issues_other','total_issue',
                                                            'grand_total','created_by','last_updated','transaction_source','created_date','last_updated_date',
                                                            'status','freeze_status','transaction_type','company','unit_price','region','cnf_id','value',
                                                            'wd_name','wd_type','sku_code','sku_short_name','town_name','town_code','distrcode',
                                                        )

            if from_temp_sale:
                # less_30_day = today_date.date()-datetime.timedelta(days=30)
                # sales_data = SalesData.objects.filter(sales_date_time__gte = less_30_day)
                for fts in from_temp_sale:
                    retive_cre_update = SalesData.objects.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
                    # retive_cre_update = sales_data.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
                    if not retive_cre_update:
                        # SaleData_create(fts).sale_create()
                        
                        
                        
                        # commented for create sale thread=============
                        
                        sales_data_serializer = SalesDataSerializer(data = fts, many = False)
                        if sales_data_serializer.is_valid():
                            sales_data_serializer.save()
                            print(sales_data_serializer.data,"=========ccrr")
                        else:
                            print(sales_data_serializer.errors)
                    else:
                        # SaleData_update(retive_cre_update,fts).sale_update()
                        
                        # commented for update sale thread=============
                        sales_data_serializer = SalesDataSerializer(retive_cre_update,data = fts, partial = True)
                        if sales_data_serializer.is_valid():
                            sales_data_serializer.save()
                            print(sales_data_serializer.data,"=========upup")
                            
                        else:
                            print(sales_data_serializer.errors)


                
            SalesData.objects.filter(wd_id__in = wd_list_4_week).update(status=True)
            trans_obj = Integration_log_summary.objects.filter(created_date__date=today_date.date(),tranisition_source = "SFA/SFA_LITE_API" ).values("total_distributer_sale","total_insart_sale","sale_date")
            log_detail = Integration_log_details.objects.filter(created_date__date = today_date.date(), tranisition_source = "SFA/SFA_LITE_API").values("sku_id","wd_id","town_id","sales_date_time","reason")
            # print(trans_obj,"======trans_obj==========mail=====")
            success_count = success_count if success_count else 0
            row_no = 0
            detail_row_no = 0
            # today = utils.now_date
            today = datetime.datetime.now()
            now_day=str(today.date())
            splited_today = now_day.split('-')[2]
            # week_details = week_sele_before_date('BRANCH USER')
            # if int(splited_today) in date_tuple_weekly and week_details[2]:
            #     print(wd_list_4_week,"==============wd_list_4_week==============")
            #     create_update_weekly(wd_list_4_week)
            count_dist_sale = 0
            insert_sale = 0
            if trans_obj:
                print(trans_obj,"======================================================mail============")
                subject = sfa_success_sub
                html_message = '<table style="width:100% ; border: 1px solid black;">'
                        
                html_message +=            '<tr style="border: 1px solid black;">'
                html_message +=                '<th "border: 1px solid black;">SNo.</th>'
                html_message +=                '<th "border: 1px solid black;">Sale Date</th>'
                html_message +=                '<th style="border: 1px solid black;">Total distributer sale</th>'
                html_message +=                '<th style="border: 1px solid black;">Total insert sale</th>'
                # html_message +=                '<th>town_id</th>'
                # html_message +=                '<th>reason</th>'
                html_message +=            '</tr>'
                for ils in trans_obj:
                    # print(ils,"=================")
                    row_no+=1
                    html_message +=            '<tr style="border: 1px solid red;">'
                    html_message +=                '<td style="border: 1px solid black;">'+str(row_no)+'</td>'
                    html_message +=                '<td style="border: 1px solid black;">'+str(ils['sale_date'])+'</td>'
                    html_message +=                '<td style="border: 1px solid black;">'+str(ils['total_distributer_sale'])+'</td>'
                    count_dist_sale = count_dist_sale + ils['total_distributer_sale']
                    html_message +=                '<td style="border: 1px solid black;">'+str(ils['total_insart_sale'])+'</td>'
                    insert_sale = insert_sale + ils['total_insart_sale']
                    
                    html_message +=            '</tr>'
                html_message +=            '<tr>'
                html_message +=                '<td style="border: 1px solid black;">'+str(str(success_count))+'</td>'
                html_message +=                '<td style="border: 1px solid black;">'+str("Total")+'</td>'
                html_message +=                '<td style="border: 1px solid black;">'+str(count_dist_sale)+'</td>'
                html_message +=                '<td style="border: 1px solid black;">'+str(insert_sale)+'</td>'
                html_message +=            '</tr>'

                
                html_message += '</table> </br></br>'



                # log details==============
                # html_message += '<table style="width:100% ; border: 1px solid black;">'
                        
                # html_message +=            '<tr style="border: 1px solid black;">'
                # html_message +=                '<th style="border: 1px solid black;">SNo.</th>'
                # html_message +=                '<th style="border: 1px solid black;">Sale Date</th>'
                # html_message +=                '<th style="border: 1px solid black;">Sku id</th>'
                # html_message +=                '<th style="border: 1px solid black;">Wd id</th>'
                # html_message +=                '<th style="border: 1px solid black;">Town id</th>'
                # html_message +=                '<th style="border: 1px solid black;">Reason</th>'
                # # html_message +=                '<th style="border: 1px solid black;">Repeat Count</th>'
                # html_message +=            '</tr>'
                # for ld in log_detail:
                    
                #     detail_row_no+=1
                #     # print(ld['sales_date_time'].date(),"==========date=======")
                #     html_message +=            '<tr style="border: 1px solid red;">'
                #     html_message +=                '<td style="border: 1px solid black;">'+str(detail_row_no)+'</td>'
                #     html_message +=                '<td style="border: 1px solid black;">'+str(ld['sales_date_time'].date())+'</td>'
                #     html_message +=                '<td style="border: 1px solid black;">'+str(ld['sku_id'])+'</td>'
                #     html_message +=                '<td style="border: 1px solid black;">'+str(ld['wd_id'])+'</td>'
                #     html_message +=                '<td style="border: 1px solid black;">'+str(ld['town_id'])+'</td>'
                #     html_message +=                '<td style="border: 1px solid black;">'+str(ld['reason'])+'</td>'
                #     # html_message +=                '<td style="border: 1px solid black;">'+str(ld['repeat_count'])+'</td>'
                #     html_message +=            '</tr>'
                # html_message += '</table> </br></br>'

                
                email_from = settings.EMAIL_HOST_USER
                cc_email = cc_list
                # ,'saurabha@triazinesoft.com','mayankg@triazinesoft.com'
                recipient_list = success_email_list
                # recipient_list = ["VIPULSHARMA-gpi@modi-ent.com","ankit.rakwal@esobene.com"]

                reset_email = EmailMessage(
                            subject = subject,
                            body = html_message,
                            from_email = email_from,
                            to = recipient_list,
                            cc = cc_email,
                            reply_to = cc_email,
                            )
                trans_obj=Integration_log_summary.objects.filter(sale_date=final_data[0].get('sale_date'),email_status = False).update(email_status = True)
                Apistatus.objects.filter(running_date=today_date,api="SFA_API").update(status=False)
                reset_email.content_subtype = "html"
                reset_email.send(fail_silently=True)
            week_details = week_sele_before_date('BRANCH USER')
            if int(splited_today) in date_tuple_weekly and week_details[2]:
                print(wd_list_4_week,"==============wd_list_4_week==============")
                create_update_weekly(wd_list_4_week)
            else:
                if int(success_count)<=0:
                    
                    emailsend_zoro_or_running("There is no sale in SFA/SFA lite API.")
                elif running_state==True:
                    
                    emailsend_zoro_or_running("SFA API is still running.")

            return None

    except Exception as e:
        error = getattr(e, 'message', repr(e))
        logger.error(error)
        context = {'status': False,'message':'Something Went Wrong','error':error}
        # subject = "UAT | SFA/SFA_lite Issue"
        subject = sfa_failed_sub
        recipient_list = failed_list
        cc_email = cc_list
        # recipient_list = ["VIPULSHARMA-gpi@modi-ent.com","ankit.rakwal@esobene.com"]
        html_message = str(context)
        reset_email = EmailMessage(
                            subject = subject,
                            body = html_message,
                            from_email = settings.EMAIL_HOST_USER,
                            to = recipient_list,
                            cc = cc_email,
                            reply_to = cc_email,
                            )
        reset_email.content_subtype = "html"
        reset_email.send(fail_silently=True)
        # return Response(context, status=status.HTTP_200_OK)

@shared_task(bind=True)
def Surya_api(self):
    try:
        print(datetime.datetime.now(),"========================")
        # print(www = 890)
        n= datetime.datetime.now().date()
        # from_date = request.GET.get("from_date",None)
        # to_date = request.GET.get("to_date",None)
        # aaa = WDmaster.objects.filter(wd_ids = "2247",wd_postal_code__icontains = '0212802').values('wd_postal_code')
        # print(week_sele_before_date('BRANCH USER'),"=======================>>>")
        # breakpoint()
        # print(str(to_date),"=====from_date=====")
        # url = "http://gpisfatest.winitsoftware.com/api/api/GPIInterface/GET?StartDate="+str(start_date)+"&EndDate="+str(start_date)+"9&Passcode=GP!W!N"
        # url = "http://gpisfatest.winitsoftware.com/api/api/GPIInterface/GET?StartDate=2022-03-23&EndDate=2022-03-23&Passcode=GP!W!N"
        # url="http://gpisfatest.winitsoftware.com/api/api/GPIInterface/GET?StartDate="+str(from_date)+"&EndDate="+str(to_date)+"&Passcode=GP!W!N"
        # print(from_date,"====",from_date)
        # if from_date and to_date:
        #     print("=======dt======")
        #     # url="https://ss.godfreyphillips.co/api_ss/api/GPIInterface/GET?StartDate="+str(from_date)+"&EndDate="+str(to_date)+"&Passcode=GP!W!N"
        #     url="https://ss.godfreyphillips.co/GPIInterFaceAPI_new/api/GPIInterface?Passcode=GP!W!N&StartDate="+str(from_date)+"&EndDate="+str(to_date)+"&Passcode=GP!W!N"

        # else:
            # print("===nn====dt======")
            # url = "https://ss.godfreyphillips.co/api_ss/api/GPIInterface?Passcode=GP!W!N"
            # url = "https://ss.godfreyphillips.co/GPIInterFaceAPI_new/api/GPIInterface?Passcode=GP!W!N"
            
        # url = "https://ss.godfreyphillips.co/api_ss/api/GPIInterface?Passcode=GP!W!N"
        url = "https://ss.godfreyphillips.co/GPIInterFaceAPI_new/api/GPIInterface?Passcode=GP!W!N"
        surya_data = requests.get(url).json()
        print("surya_data",url,"======surya_data ======")
        errors_list = []
        error_obj_list = []
        valid_in_ss = []
        transaction_history = {}
        error_detail_dict = {}
        flag=0
        wd_list_4_week = []
        date_tuple_weekly = [8,15,22,1]
        
        wd_count = 0
        sku_count = 0
        town_count = 0
        n = datetime.datetime.now().date()-datetime.timedelta(days=1)
        # today = utils.now_date
        today = datetime.datetime.now()
        now_day=str(today.date())
        splited_today = now_day.split('-')[2]
        week_details = week_sele_before_date('BRANCH USER')
    
    
        surya_api_sale_date=parse(surya_data.get('StartDate'))
        
        surya_datas=surya_data.get('Data')
        json_object = json.dumps(surya_datas, indent = 4)
        with open(settings.MEDIA_ROOT + 'surya_api_sales/'+"surya_sales_"+str(datetime.datetime.now().date()) + '.json','w')as outfile:
            outfile.write(json_object)
        if surya_datas:
            response = HttpResponse(content_type='text/csv')
            # response['Content-Disposition'] = 'attachment; filename="sec_sales_data.csv"'
            df = pd.DataFrame.from_dict(list(surya_datas))
            df.to_csv(settings.MEDIA_ROOT + 'surya_api_sales_csv/'+"surya_sales_"+str(datetime.datetime.now().date()) + '.csv', index = False)

        if surya_datas:
            
            for json_data in surya_datas:
                wd = []
                sku = []
                town = []
                if json_data['sku_code'] and json_data['wd_code'] and json_data['town_id']:
                    sku_obj=SKU_Master_Product.objects.filter(sku_code=json_data['sku_code']).last()
                    json_data['wd_id'] = json_data['wd_code']
                    
                    user = User.objects.filter(user_id = json_data['wd_code'])
                    town_cde = str("0")+str(json_data['town_id'])# 0 concatenate for town issue================
                    town_cde2 = str(json_data['town_id']).strip('-')
                    wd_town_list =Sales_Hierarchy_Master.objects.filter((Q(town_code=json_data['town_id'])|Q(town_code=town_cde)|Q(town_code=town_cde2)|Q(town_code__iexact = str(json_data['town_id'])[1:])),wd_id=json_data.get('wd_id')).values_list('wd_town_id',flat=True)
                    wdobj = WdSkuCatagory.objects.filter(sku_code=json_data['sku_code'],wd_town_id__in=wd_town_list).last()
                    
                    if not sku_obj:
                        sku.append(json_data['sku_code'])
                    if not user:
                        wd.append(json_data['wd_code'])
                    if not wdobj:
                        town.append(json_data['town_id'])
                    total_sale = (
                            float(json_data.get('local_sales_reatil') if json_data.get('local_sales_reatil', 0) else 0) 
                            + float(json_data.get('local_sales_dealer') if json_data.get('local_sales_dealer', 0) else 0)
                            + float(json_data.get('local_sales_modern_trade') if json_data.get('local_sales_modern_trade', 0) else 0)
                            + float(json_data.get('local_sales_hawker') if json_data.get('local_sales_hawker', 0) else 0)
                            
                            + float(json_data.get('outstation_sales_reatil') if json_data.get('outstation_sales_reatil', 0) else 0) 
                            + float(json_data.get('outstation_sales_dealer') if json_data.get('outstation_sales_dealer', 0) else 0)
                            + float(json_data.get('outstation_sales_modern_trade') if json_data.get('outstation_sales_modern_trade', 0) else 0)
                            + float(json_data.get('outstation_sales_hawker') if json_data.get('outstation_sales_hawker', 0) else 0)
                            
                            + float(json_data.get('other_sales_reatil') if json_data.get('other_sales_reatil', 0) else 0) 
                            + float(json_data.get('other_sales_dealer') if json_data.get('other_sales_dealer', 0) else 0)
                            + float(json_data.get('other_sales_hawker') if json_data.get('other_sales_hawker', 0) else 0)
                            + float(json_data.get('other_sales_modern_trade') if json_data.get('other_sales_modern_trade', 0) else 0)
                        )

                    if sku_obj and wdobj and user and (total_sale > 0):
                        valid_in_ss.append(json_data)
                    else:
                        json_data['dist_id']=json_data['wd_code']
                        json_data['prodcode']=json_data['sku_code']
                        json_data['town_code']=json_data['town_id']
                        json_data['sale_date']=json_data['sale_date_time']
                        json_data['region']=json_data['region']
                        json_data['local_retail']=json_data['local_sales_reatil']
                        json_data['local_dealer']=json_data['local_sales_dealer']
                        json_data['local_MT']=json_data['local_sales_modern_trade']
                        json_data['local_HA']=json_data['local_sales_hawker']
                        json_data['out_retail']=json_data['outstation_sales_reatil']
                        json_data['out_dealer']=json_data['outstation_sales_dealer']
                        json_data['out_MT']=json_data['outstation_sales_modern_trade']
                        json_data['out_HA']=json_data['outstation_sales_hawker']
                        json_data['other_retail']=json_data['other_sales_reatil']
                        json_data['other_dealer']=json_data['other_sales_dealer']
                        json_data['other_MT']=json_data['other_sales_modern_trade']
                        json_data['other_issued_damage']=json_data['other_issues_damage']
                        json_data['other_issues_return']=json_data['other_issues_return']
                        json_data['transaction_source'] = "SURYA_API"
                        json_data['plan_type'] = "DAILY"
                        json_data['distrcode'] = str(json_data['wd_code'])+"-"+str(json_data['town_code'])
                        log_data_serializer = Invalid_log_dataSerializers(data = json_data)
                        if log_data_serializer.is_valid():
                            log_data_serializer.save()
                        if total_sale == 0:
                            error_detail_dict['reason'] = str(json_data['wd_code']) +" "+" Received '0' sales for this SKU"+ str(json_data['sku_code'])
                        elif len(wd)>0:
                            wd_count = wd_count+1
                            error_detail_dict['repeat_count'] = wd_count
                            error_detail_dict['reason'] = str(json_data['wd_code']) +" "+" wd_id is not present in user_master database."
                        elif len(sku)>0:
                            sku_count = sku_count+1
                            error_detail_dict['repeat_count'] = sku_count
                            error_detail_dict['reason'] = str(json_data['sku_code']) +" "+ " sku_code is not present in sku_master database: sku_master"
                        elif len(town)>0:
                            town_count = town_count+1
                            error_detail_dict['repeat_count'] = town_count
                            error_detail_dict['reason'] = str(json_data['sku_code']) +" sku_code is not mapped with "+ str(json_data['wd_code']) +" wd_id in SS_database: Sales_Hierarchy_Master"
                        
                        const_time = datetime.datetime(2009, 10, 5, 00, 00, 00)
                        error_detail_dict['sku_id'] = str(json_data['sku_code'])
                        error_detail_dict['wd_id'] = str(json_data['wd_code'])
                        error_detail_dict['town_id'] = str(json_data['town_id'])
                
                        error_detail_dict['tranisition_source'] = "SURYA_API"
                        comb_d_t = datetime.datetime.combine(parse(json_data['sale_date_time']), const_time.time())
                        error_detail_dict['sales_date_time'] = comb_d_t
                        log_detail = Integration_log_details.objects.filter(tranisition_source = "SURYA_API",sales_date_time = comb_d_t, sku_id = json_data['sku_code'],town_id = json_data['town_id']).last()
                        
                        if log_detail:
                            log_serializer = Integration_log_detailsSerializers(log_detail, data = error_detail_dict , partial = True)
                            
                            if log_serializer.is_valid():
                                
                                log_serializer.save()
                        else:
                            log_serializer = Integration_log_detailsSerializers(data = error_detail_dict)
                            
                            if log_serializer.is_valid():
                                
                                log_serializer.save()
                            else:
                                pass
                                # return Response(log_serializer.errors)
            a = 0
            if valid_in_ss:
                # print(a,"====")
                for ss_store in valid_in_ss:
                    a=a+1
                    wd_list_4_week.append(ss_store.get('wd_id'))
                    sku_obj=SKU_Master_Product.objects.filter(sku_code=ss_store['sku_code']).last()
                    
                    local_sales_retailcalulated = ss_store.get('local_sales_reatil') if ss_store.get('local_sales_reatil', 0) else 0
                    local_sales_dealercalulated = ss_store.get('local_sales_dealer') if ss_store.get('local_sales_dealer', 0) else 0
                    # calculate suryaAPI sale value======================
                    if sku_obj and sku_obj.category_name == "CIGARETTE":
                        umo_code = sku_obj.weight_uom_code if sku_obj.weight_uom_code else 10
                        calculated_val = sku_obj.calculated_by if sku_obj.calculated_by else 100
                        local_sales_retailcalulated = float(ss_store.get('local_sales_reatil') if ss_store.get('local_sales_reatil', 0) else 0)/float(calculated_val)
                        local_sales_dealercalulated = float(ss_store.get('local_sales_dealer') if ss_store.get('local_sales_dealer', 0) else 0)/float(calculated_val)
                        

                    ss_store['wd_id'] = ss_store['wd_code']
                    wd_town_list =Sales_Hierarchy_Master.objects.filter(Q(wd_id=ss_store.get('wd_id'))|Q(town_code=ss_store['town_id'])|Q(town_code__iexact = str(ss_store['town_id'])[1:])).values_list('wd_town_id',flat=True)
                    wdobj = WdSkuCatagory.objects.filter(sku_code=ss_store['sku_code'],wd_town_id__in=wd_town_list).last()
                    wdid = WDmaster.objects.filter(wd_ids = ss_store.get('wd_id')).last()
                    town_code1 = "0"+str(ss_store['town_id'])# 0 concatenate for town issue================
                    town_cde2 = str(ss_store['town_id']).strip('-')
                    wd_town_name =Sales_Hierarchy_Master.objects.filter(wd_id=ss_store.get('wd_id')).last()
                    wd_town_code =Sales_Hierarchy_Master.objects.filter((Q(town_code=ss_store['town_id'])| Q(town_code__iexact = str(ss_store['town_id'])[1:]) |Q(town_code=town_code1)|Q(town_code=town_cde2)),wd_id=ss_store.get('wd_id')).last()
                    town_name = WDmaster.objects.filter(wd_ids = ss_store.get('wd_id'),wd_postal_code__icontains = wd_town_code.town_code).values('wd_postal_code').last()
                    ss_store['town_code'] = wd_town_code.town_code
                    ss_store['sku_short_name'] = sku_obj.sku_short_name
                    ss_store['sku_code'] = ss_store['sku_code']
                    ss_store['region'] = ss_store['region']
                    ss_store['wd_name'] = wdid.wd_name
                    ss_store['wd_type'] = wdid.wd_type
                    # print(town_name['wd_postal_code'])
                    if town_name:
                        ss_store['town_name'] = town_name['wd_postal_code']
                    else:
                        ss_store['town_name'] = None

                    ss_store['sku_id'] = sku_obj.sku_id
                    ss_store['transaction_source'] = "SURYA_API"
                    
                    ss_store['brand_category'] = sku_obj.category_code
                    ss_store['transaction_type'] = 'DAILY'
                    ss_store['created_by'] = "SURYA_API"
                    ss_store['created_date'] = datetime.datetime.now()
                    ss_store['sales_date_time'] = ss_store.get('sale_date_time')
                    ss_store['local_sales_retail'] = round(float(local_sales_retailcalulated),3)
                    ss_store['local_sales_dealer'] = round(float(local_sales_dealercalulated),3)
                    ss_store['local_sales_modern_trade'] = 0
                    ss_store['local_sales_hawker'] = 0
                    ss_store['outstation_sales_reatil'] = 0
                    ss_store['outstation_sales_dealer'] = 0
                    ss_store['outstation_sales_modern_trade'] = 0
                    ss_store['outstation_sales_hawker'] = 0
                    ss_store['other_sales_reatil'] = 0
                    ss_store['other_sales_dealer'] = 0
                    ss_store['other_sales_modern_trade'] = 0
                    ss_store['other_issues_other'] = 0
                    ss_store['other_issues_damage'] = 0
                    ss_store['other_issues_return'] = 0

                    ss_store['total_local_sales'] = round((float(ss_store['local_sales_retail'],) + float(ss_store['local_sales_dealer'],) + float(ss_store['local_sales_modern_trade'],) + float(ss_store['local_sales_hawker'],)),3)
                    ss_store['total_outstation_sales'] = round((float(ss_store['outstation_sales_reatil']) + float(ss_store['outstation_sales_dealer']) + float(ss_store['outstation_sales_hawker']) + float(ss_store['outstation_sales_modern_trade'])),3)
                    ss_store['total_other_sales'] = round((float(ss_store['other_sales_reatil']) + float(ss_store['other_sales_dealer']) + float(ss_store['other_sales_modern_trade'])),3)
                    ss_store['grand_total'] = round((ss_store['total_local_sales'] + ss_store['total_outstation_sales'] + ss_store['total_other_sales']),3)

                    ss_store['total_issue'] = round((float(ss_store['other_issues_other']) + float(ss_store['other_issues_damage']) + float(ss_store['other_issues_return'])),3)
                    
                    ss_store['company'] = sku_obj.company
                    branch = User.objects.filter(user_id = ss_store['wd_code']).last()
                    region = BranchMaster.objects.filter(branch_code = branch.locationcode).last()
                    ss_store['region'] = region.region
                    sale_data=""
                    if wdobj:
                        ss_store['unit_price'] = wdobj.last_price
                        ss_store['cnf_id'] = wdobj.cnf_id
                        ss_store['town_id'] =  wdobj.wd_town_id
                        ss_store['value'] = float(wdobj.last_price) * float(ss_store['grand_total'])
                        
                        sale_data = SalesData.objects.filter(wd_id = ss_store['wd_id'], sku_id = sku_obj.sku_id, sales_date_time=ss_store['sales_date_time'],town_id = wdobj.wd_town_id,town_code = wd_town_code.town_code).last()
                    
                    if sale_data :
                        ss_store.pop('created_by')
                        ss_store.pop('sales_date_time')
                        ss_store.pop('created_date')
                        ss_store['last_updated'] = "Surya_API"
                        ss_store['last_updated_date'] = datetime.datetime.now()
                        serializer = SalesDataSerializer(sale_data, data = ss_store,partial=True)
                        if serializer.is_valid():
                            serializer.save()
                            flag=flag+1
                        else:
                            errors_list.append(serializer.errors,ss_store['wd_code'],ss_store['sku_code'])
                            
                    else:
                        serializer = SalesDataSerializer(data = ss_store)
                        if serializer.is_valid():
                            serializer.save()
                            flag=flag+1
                        else:
                            errors_list.append(serializer.errors,)

            transaction_history['tranisition_source'] = "SURYA_API"
            transaction_history['sale_date'] = surya_api_sale_date.date()
            transaction_history['total_distributer_sale'] = len(surya_datas)
            transaction_history['total_insart_sale'] = len(valid_in_ss) if len(valid_in_ss) else 0
            transaction_history['created_by'] = "SURYA_API"
            transaction_history['created_date'] = datetime.datetime.now()
            transact_his = Integration_log_summary.objects.filter(sale_date = transaction_history['sale_date'],tranisition_source = "SURYA_API").last()
            print(transact_his,"=====",transaction_history['sale_date'])
            # print(transaction_history,"======transaction_history==== ",transaction_history)
            if transact_his is not None:
                print("======update")
                transaction_history.pop('created_date')
                transaction_history['last_updated_date'] = datetime.datetime.now()
                serializer_class = Integration_log_summarySerializers(transact_his,data = transaction_history,partial=True)
                if serializer_class.is_valid():
                    serializer_class.save()
                else:
                    # return Response(serializer_class.errors)
                    pass
            else:
                print("======create")
                
                serializer_class = Integration_log_summarySerializers(data = transaction_history)
                if serializer_class.is_valid():
                    # print("hiii__create")
                    serializer_class.save()
                else:
                    # return Response(serializer_class.errors)
                    pass

            trans_obj=Integration_log_summary.objects.filter(sale_date=transaction_history['sale_date'],email_status = False,tranisition_source = "SURYA_API").values("total_distributer_sale","total_insart_sale","sale_date")
            log_detail = Integration_log_details.objects.filter(sales_date_time__date = surya_datas[0]['sale_date_time'],tranisition_source = "SURYA_API").values("sku_id","wd_id","town_id","sales_date_time","reason","repeat_count")
            row_no = 0
            if trans_obj or log_detail:
                # subject = '"UAT | SURYA_API Integration Status Report."'
                subject = surya_success_sub
                html_message = '<table style="width:100% ; border: 1px solid black;">'
                        
                html_message +=            '<tr style="border: 1px solid black;">'
                html_message +=                '<th "border: 1px solid black;">SNo.</th>'
                html_message +=                '<th "border: 1px solid black;">Sale Date</th>'
                html_message +=                '<th style="border: 1px solid black;">Total distributer sale</th>'
                html_message +=                '<th style="border: 1px solid black;">Total insert sale</th>'
                # html_message +=                '<th>town_id</th>'
                # html_message +=                '<th>reason</th>'
                html_message +=            '</tr>'
                for ils in trans_obj:
                    # print(ils,"=================")
                    html_message +=            '<tr style="border: 1px solid red;">'
                    html_message +=                '<td style="border: 1px solid black;">'+str(row_no+1)+'</td>'
                    html_message +=                '<td style="border: 1px solid black;">'+str(ils['sale_date'])+'</td>'
                    html_message +=                '<td style="border: 1px solid black;">'+str(ils['total_distributer_sale'])+'</td>'
                    html_message +=                '<td style="border: 1px solid black;">'+str(ils['total_insart_sale'])+'</td>'
                    
                    html_message +=            '</tr>'
                html_message += '</table> </br></br>'



                # log details==============
                html_message += '<table style="width:100% ; border: 1px solid black;">'
                        
                html_message +=            '<tr style="border: 1px solid black;">'
                html_message +=                '<th style="border: 1px solid black;">SNo.</th>'
                html_message +=                '<th style="border: 1px solid black;">Sale Date</th>'
                html_message +=                '<th style="border: 1px solid black;">Sku id</th>'
                html_message +=                '<th style="border: 1px solid black;">Wd id</th>'
                html_message +=                '<th style="border: 1px solid black;">Town id</th>'
                html_message +=                '<th style="border: 1px solid black;">Reason</th>'
                # html_message +=                '<th style="border: 1px solid black;">Repeat Count</th>'
                html_message +=            '</tr>'
                for ld in log_detail:
                    
                    row_no+=1
                    # print(ld['sales_date_time'].date(),"==========date=======")
                    html_message +=            '<tr style="border: 1px solid red;">'
                    html_message +=                '<td style="border: 1px solid black;">'+str(row_no)+'</td>'
                    html_message +=                '<td style="border: 1px solid black;">'+str(ld['sales_date_time'].date())+'</td>'
                    html_message +=                '<td style="border: 1px solid black;">'+str(ld['sku_id'])+'</td>'
                    html_message +=                '<td style="border: 1px solid black;">'+str(ld['wd_id'])+'</td>'
                    html_message +=                '<td style="border: 1px solid black;">'+str(ld['town_id'])+'</td>'
                    html_message +=                '<td style="border: 1px solid black;">'+str(ld['reason'])+'</td>'
                    # html_message +=                '<td style="border: 1px solid black;">'+str(ld['repeat_count'])+'</td>'

                    html_message +=            '</tr>'
                html_message += '</table> </br></br>'

                
                email_from = settings.EMAIL_HOST_USER
                cc_email = cc_list
                # # ,'saurabha@triazinesoft.com','mayankg@triazinesoft.com'
                # recipient_list = ["rasmis@triazinesoft.com"]
                recipient_list = success_email_list

                reset_email = EmailMessage(
                            subject = subject,
                            body = html_message,
                            from_email = email_from,
                            to = recipient_list,
                            cc = cc_email,
                            reply_to = cc_email,
                            )
                # trans_obj=Integration_log_summary.objects.filter(sale_date = surya_datas[0]['sale_date_time'],email_status = False,tranisition_source = "SURYA_API").update(email_status = True)
                reset_email.content_subtype = "html"
                reset_email.send(fail_silently=True)      
                
                
            
            # today = utils.now_date
            today = datetime.datetime.now()
            now_day=str(today.date())
            splited_today = now_day.split('-')[2]
            week_details = week_sele_before_date('BRANCH USER')
            
            if int(splited_today) in date_tuple_weekly and week_details[2]:
                create_update_weekly(wd_list_4_week)
                
            # return Response({"errors_list":errors_list,"error":error_obj_list})
        else:
            # subject = '"SURYA_API_No Sale"'
            subject = surya_success_sub
            html_message = "SURYA API Having No sales.</p>"
            email_from = settings.EMAIL_HOST_USER
            cc_email = cc_list
            # # ,'saurabha@triazinesoft.com','mayankg@triazinesoft.com'
            recipient_list = failed_list
            # recipient_list = ["VIPULSHARMA-gpi@modi-ent.com","ankit.rakwal@esobene.com"]

            no_sale_mail = EmailMessage(
                        subject = subject,
                        body = html_message,
                        from_email = email_from,
                        to = recipient_list,
                        cc = cc_email,
                        reply_to = cc_email,
                        )
            no_sale_mail.content_subtype = "html"
            no_sale_mail.send(fail_silently=True)
    except Exception as e:
        error = getattr(e, 'message', repr(e))
        logger.error(error)
        context = {'status': False,'message':'Something Went Wrong','error':error}
        subject = "UAT | SURYA_API Issues"
        subject = surya_failed_sub
        # recipient_list = ["VIPULSHARMA-gpi@modi-ent.com","ankit.rakwal@esobene.com"]
        cc_email = cc_list
        recipient_list = failed_list
        html_message = str(context)
        reset_email = EmailMessage(
                            subject = subject,
                            body = html_message,
                            from_email = settings.EMAIL_HOST_USER,
                            to = recipient_list,
                            cc = cc_email,
                            reply_to = cc_email,
                            )
        reset_email.content_subtype = "html"
        reset_email.send(fail_silently=True)
        # return Response(context, status=status.HTTP_200_OK)



# create Weekly by wd_wise==============

@shared_task(bind=True)
def create_weekly_wd_wise(self,wd_id,cat_li,week,date_range):
    try:
        week_data_sum = SalesData.objects.filter(transaction_type='DAILY',wd_id = wd_id,brand_category__in=cat_li,sales_date_time__gte=parse(date_range[0]).date(),sales_date_time__lte=parse(date_range[1]).date()).values('wd_id','sku_id','town_id','town_code','brand_category').annotate(Sum('local_sales_retail'),
                                        Sum('local_sales_dealer'),Sum('local_sales_modern_trade'),Sum('local_sales_hawker'),Sum('total_local_sales'),Sum('outstation_sales_reatil'),
                                        Sum('outstation_sales_dealer'),Sum('outstation_sales_modern_trade'),Sum('outstation_sales_hawker'),Sum('total_outstation_sales'),Sum('other_sales_retail'),Sum('other_sales_dealer'),
                                        Sum('other_sales_modern_trade'),Sum('total_other_sales'),Sum('other_issues_damage'),Sum('other_issues_return'),Sum('other_issues_other'),Sum('total_issue'),Sum('grand_total'),Sum('value'))
        print(wd_id,cat_li,week,date_range,"===========",week_data_sum)
        # print(parse(date_range[0]).date(),cat_li)
        # breakpoint()
        if week_data_sum and date_range:
            for week_sale in week_data_sum:
                print("=======v=====")
                # print(week_sale['sku_id'],"=====",week_sale['wd_id'],"======",week_sale['town_id'])
                week_sale_data = SalesData.objects.filter(sales_date_time = parse(date_range[1]).date(),wd_id=week_sale['wd_id'],sku_id=week_sale['sku_id'],town_id = week_sale['town_id'],transaction_type=week, town_code = week_sale['town_code'])
                source_data = WDmaster.objects.filter(wd_ids = week_sale['wd_id']).last()
                wd_town_code = Sales_Hierarchy_Master.objects.filter(wd_id=week_sale['wd_id']).last()
                if wd_town_code:
                    town_code = wd_town_code.town_code
                else:
                    town_code = None
                if source_data:
                    source_user = source_data.wd_type
                    wd_name = source_data.wd_name
                    wd_type = source_data.wd_type
                else:
                    source_user = None
                    wd_name = source_data.wd_name
                    wd_type = source_data.wd_type
                if not week_sale_data:
                    sele_week_obj= SalesData()
                    sele_week_obj.wd_name = wd_name
                    sele_week_obj.town_name = source_data.wd_postal_code
                    sele_week_obj.wd_type = wd_type
                    sele_week_obj.town_code = town_code
                    sele_week_obj.town_id = week_sale['town_id']
                    sele_week_obj.sku_id = week_sale['sku_id']
                    sele_week_obj.wd_id = week_sale['wd_id']
                    sele_week_obj.sales_date_time = parse(date_range[1]).date()
                    # -datetime.timedelta(days=1)
                    sele_week_obj.transaction_source = source_user
                    sele_week_obj.created_by = 'auto_scheduler'
                    sele_week_obj.transaction_type = week
                    sele_week_obj.created_date = datetime.datetime.now()
                    sele_week_obj.local_sales_retail = round(week_sale['local_sales_retail__sum'],2)
                    sele_week_obj.local_sales_dealer = round(week_sale['local_sales_dealer__sum'],2)
                    sele_week_obj.local_sales_modern_trade = round(week_sale['local_sales_modern_trade__sum'],2)
                    sele_week_obj.local_sales_hawker = round(week_sale['local_sales_hawker__sum'],2)
                    sele_week_obj.outstation_sales_reatil = round(week_sale['outstation_sales_reatil__sum'],2)
                    sele_week_obj.outstation_sales_dealer = round(week_sale['outstation_sales_dealer__sum'],2)
                    sele_week_obj.outstation_sales_modern_trade = round(week_sale['outstation_sales_modern_trade__sum'],2)
                    sele_week_obj.outstation_sales_hawker = round(week_sale['outstation_sales_hawker__sum'],2)
                    sele_week_obj.other_sales_retail = round(week_sale['other_sales_retail__sum'],2)
                    sele_week_obj.other_sales_dealer = round(week_sale['other_sales_dealer__sum'],2)
                    sele_week_obj.other_sales_modern_trade = round(week_sale['other_sales_modern_trade__sum'],2)
                    sele_week_obj.other_issues_other = round(week_sale['other_issues_other__sum'],2)
                    sele_week_obj.other_issues_damage = round(week_sale['other_issues_damage__sum'],2)
                    sele_week_obj.other_issues_return = round(week_sale['other_issues_return__sum'],2)
                    sele_week_obj.total_local_sales = round(week_sale['total_local_sales__sum'],2)
                    sele_week_obj.total_outstation_sales = round(week_sale['total_outstation_sales__sum'],2)
                    sele_week_obj.total_other_sales = round(week_sale['total_other_sales__sum'],2)
                    sele_week_obj.total_issue = round(week_sale['total_issue__sum'],2)
                    sele_week_obj.grand_total = round(week_sale['grand_total__sum'],2)
                    
                    sele_week_obj.brand_category = week_sale['brand_category']
                    # sele_week_obj.last_updated_date = datetime.datetime.now()

                    unit_value = SKU_Master_Product.objects.filter(sku_id = week_sale['sku_id']).last()
                    if unit_value:
                        sku_code = unit_value.sku_code
                        sku_short_name = unit_value.sku_short_name
                        sele_week_obj.company = unit_value.company
                    else:
                        sku_code = None
                        sku_short_name = unit_val.sku_short_name
                        sele_week_obj.company = "unit_value.company"
                    category_data = WdSkuCatagory.objects.filter(wd_town_id = week_sale['town_id'],sku_id = week_sale['sku_id']).last()
                    
                    if category_data:
                        sele_week_obj.cnf_id = category_data.cnf_id
                        unit_val = category_data.last_price
                    else:
                        sele_week_obj.cnf_id = None
                        unit_val =  0
                    wdregion = User.objects.filter(user_id = week_sale['wd_id']).last()
                    region = BranchMaster.objects.filter(branch_code = wdregion.locationcode).last()
                    sele_week_obj.sku_code = sku_code
                    sele_week_obj.sku_short_name = sku_short_name
                    sele_week_obj.region = region.region
                    sele_week_obj.unit_price = unit_val
                    sele_week_obj.value = sele_week_obj.grand_total * sele_week_obj.unit_price
                    sele_week_obj.distrcode = str(week_sale['wd_id'])+"-"+str(town_code)
                    
                    sele_week_obj.save()
    except Exception as e:
        error = getattr(e, 'message', repr(e))
        logger.error(error)
        context = {'status': False,'message':'Something Went Wrong','error':error}
        # return Response(context, status=status.HTTP_200_OK)