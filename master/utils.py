import datetime
from base.models import BranchMaster, User, WDmaster
from master.models import Integration_log_summary, SKU_Master_Product, Sales_Hierarchy_Master, SalesData, WdSkuCatagory
from django.db.models import Sum
from wd import utils
from wd.helper import week_sele_before_date
import logging
from rest_framework.response import Response
from rest_framework import status

from wd.serializers import SalesDataCreateWeekSerializer
logger = logging.getLogger(__name__)
from django.db.models import Q
date_list_2d = [8,15,22,1]
# today = utils.now_date
today = datetime.datetime.now()
now_day=str(today.date())
splited_today = now_day.split('-')

user_type = 'BRANCH USER'
week_help = week_sele_before_date(user_type)


def weekly_generate_on_weekend(wd_id_li):
    try:
        if int(splited_today[2]) in date_list_2d and week_help[2]:
            print(week_help,"====================================================//==============")
            week_data_sum = SalesData.objects.filter(transaction_type='DAILY',wd_id__in = wd_id_li,sales_date_time__gte=week_help[2][0],sales_date_time__lte=week_help[2][1]).values('wd_id','sku_id','town_code','brand_category').annotate(Sum('local_sales_retail'),
                                    Sum('local_sales_dealer'),Sum('local_sales_modern_trade'),Sum('local_sales_hawker'),Sum('total_local_sales'),Sum('outstation_sales_reatil'),
                                    Sum('outstation_sales_dealer'),Sum('outstation_sales_modern_trade'),Sum('outstation_sales_hawker'),Sum('total_outstation_sales'),Sum('other_sales_retail'),Sum('other_sales_dealer'),
                                    Sum('other_sales_modern_trade'),Sum('total_other_sales'),Sum('other_issues_damage'),Sum('other_issues_return'),Sum('other_issues_other'),Sum('total_issue'),Sum('grand_total'),Sum('value'))
            if week_data_sum:
                for week_sale in week_data_sum:
                    source_data = WDmaster.objects.filter(wd_ids = week_sale['wd_id']).last()
                    
                    wd_town_code = Sales_Hierarchy_Master.objects.filter(wd_id=week_sale['wd_id'],town_code = week_sale['town_code']).values_list('wd_town_id',flat=True)
                    wdobj = WdSkuCatagory.objects.filter(wd_town_id__in=wd_town_code,sku_id=week_sale['sku_id']).last()
                    town_name = WDmaster.objects.filter(wd_ids = week_sale['wd_id'],wd_postal_code__icontains = week_sale['town_code']).values('wd_postal_code').last()
                    if wdobj:
                        town_id = wdobj.wd_town_id
                    else:
                        town_id = None
                    
                    week_sale_data = SalesData.objects.filter(sales_date_time = week_help[2][1],wd_id=week_sale['wd_id'],sku_id=week_sale['sku_id'],town_id = town_id,transaction_type=week_help[1], town_code = week_sale['town_code'])
                    if source_data:
                        wd_type = source_data.wd_type
                    else:
                        wd_type = source_data.wd_type
                    if town_name:
                        wd_name = source_data.wd_name
                    else:
                        wd_name = None
                    # print(week_sale['wd_id'],"=======week_val_rng=======",week_sale['sku_id'])
                    if not week_sale_data and town_id is not None:
                        print("create==============")
                        sele_week_obj['statename'] = town_name.wd_state
                        sele_week_obj= SalesData()
                        sele_week_obj.wd_name = wd_name
                        sele_week_obj.town_name = source_data.wd_postal_code
                        sele_week_obj.wd_type = wd_type
                        sele_week_obj.town_code = week_sale['town_code']
                        sele_week_obj.town_id = town_id
                        sele_week_obj.sku_id = week_sale['sku_id']
                        sele_week_obj.wd_id = week_sale['wd_id']
                        sele_week_obj.sales_date_time = week_help[2][1]
                        sele_week_obj.transaction_source = "SURYA_API"
                        sele_week_obj.created_by = 'auto_scheduler'
                        sele_week_obj.transaction_type = week_help[1]
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

                        unit_value = SKU_Master_Product.objects.filter(sku_id = week_sale['sku_id']).last()
                        if unit_value:
                            sku_code = unit_value.sku_code
                            sku_short_name = unit_value.sku_short_name
                            sele_week_obj.company = unit_value.company
                        else:
                            sku_code = None
                            sku_short_name = unit_val.sku_short_name
                            sele_week_obj.company = "unit_value.company"
                        category_data = WdSkuCatagory.objects.filter(wd_town_id =town_id,sku_id = week_sale['sku_id']).last()
                        
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
                        sele_week_obj.distrcode = str(week_sale['wd_id'])+"-"+str(week_sale['town_code'])
                        
                        sele_week_obj.save()
    except Exception as e:
        error = getattr(e, 'message', repr(e))
        logger.error(error)
        context = {'status': False,'message':'Something Went Wrong','error':error}
        return Response(context, status=status.HTTP_200_OK)
    

def create_update_weekly(wd_id_li):
    try:
        today = datetime.datetime.now()
        now_day=str(today.date())
        splited_today = now_day.split('-')
        global_data = []
        if int(splited_today[2]) in date_list_2d and week_help[2]:
            print(week_help,"====================================================//==============")
            week_data_sums = SalesData.objects.filter(transaction_type='DAILY',wd_id__in = wd_id_li,sales_date_time__gte=week_help[2][0],sales_date_time__lte=week_help[2][1]).values('wd_id','sku_id','town_code','brand_category').annotate(Sum('local_sales_retail'),
                                    Sum('local_sales_dealer'),Sum('local_sales_modern_trade'),Sum('local_sales_hawker'),Sum('total_local_sales'),Sum('outstation_sales_reatil'),
                                    Sum('outstation_sales_dealer'),Sum('outstation_sales_modern_trade'),Sum('outstation_sales_hawker'),Sum('total_outstation_sales'),Sum('other_sales_retail'),Sum('other_sales_dealer'),
                                    Sum('other_sales_modern_trade'),Sum('total_other_sales'),Sum('other_issues_damage'),Sum('other_issues_return'),Sum('other_issues_other'),Sum('total_issue'),Sum('grand_total'),Sum('value'))
        if week_data_sums:
            for week_data_sum in week_data_sums:
                
                unit_value = SKU_Master_Product.objects.filter(sku_id=week_data_sum['sku_id']).last()
                wd_town_list =Sales_Hierarchy_Master.objects.filter(wd_id=week_data_sum['wd_id'],town_code=week_data_sum['town_code']).values_list('wd_town_id',flat=True)
                wdobj = WdSkuCatagory.objects.filter(wd_town_id__in=wd_town_list,sku_id=week_data_sum['sku_id']).last()
                sele_week_obj = {}
                town_name = WDmaster.objects.filter(wd_ids = week_data_sum['wd_id'],wd_postal_code__icontains = week_data_sum['town_code']).last()
                wd_town_name = town_name.wd_postal_code if town_name else ''
                if town_name:
                    wd_name = town_name.wd_name
                    wd_type = town_name.wd_type
                else:
                    wd_name = week_data_sum['town_code']
                    wd_type = "Seconadary_sales"
                    
                wdobj = WdSkuCatagory.objects.filter(wd_town_id__in=wd_town_list,sku_id=week_data_sum['sku_id']).last()
                try:
                    parse_town = int(week_data_sum['town_code'])
                except Exception as e:
                    parse_town = None
                town_name = WDmaster.objects.filter((Q(wd_postal_code__icontains = week_data_sum['town_code'])| Q(wd_postal_code__icontains = week_data_sum['town_code'])),wd_ids = week_data_sum['wd_id'],).values('wd_postal_code').last()
                if wdobj:
                    town_id = wdobj.wd_town_id
                else:
                    town_id = None
                
                source_data = WDmaster.objects.filter(wd_ids=week_data_sum['wd_id']).last()
                if source_data:
                    source_user = source_data.wd_type
                else:
                    source_user = None
                if town_id is not None:
                    sale_data = SalesData.objects.filter(wd_id__icontains = week_data_sum['wd_id'],sku_id__icontains = week_data_sum['sku_id'],sales_date_time__icontains = week_help[2][1],transaction_type__icontains=week_help[1],town_id__icontains = town_id ,town_code__icontains=week_data_sum['town_code'],brand_category__icontains=week_data_sum['brand_category']).last()
                    sele_week_obj['town_id'] = town_id
                    sele_week_obj['statename'] = source_data.wd_state
                    sele_week_obj['sku_id'] = week_data_sum['sku_id']
                    sele_week_obj['wd_id'] = week_data_sum['wd_id']
                    sele_week_obj['sales_date_time'] = week_help[2][1]
                
                    sele_week_obj['transaction_source'] = source_user
                    sele_week_obj['created_by'] = "auto_secdulre"
                    sele_week_obj['transaction_type'] = week_help[1]
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
                    sele_week_obj['town_code'] = week_data_sum['town_code']
                    sele_week_obj['sku_short_name'] = unit_value.sku_short_name
                    sele_week_obj['sku_code'] = unit_value.sku_code
                    sele_week_obj['wd_name'] = wd_name
                    sele_week_obj['town_name'] = wd_town_name
                    sele_week_obj['wd_type'] = wd_type
                    sele_week_obj['cnf_id'] = wdobj.cnf_id if wdobj and wdobj.cnf_id else None
                    sele_week_obj['distrcode'] = str(week_data_sum['wd_id'])+"-"+str(str(week_data_sum['town_code']))
                    sele_week_obj['brand_category'] = week_data_sum['brand_category']
                

                    
                    if unit_value:
                    
                        sele_week_obj['company'] = unit_value.company
                    else:
                    
                        sele_week_obj['company'] = ""
                    wdregion = User.objects.filter(user_id=week_data_sum['wd_id']).last()
                    region = BranchMaster.objects.filter(branch_code=wdregion.locationcode).last()
                    sele_week_obj['region'] = region.region
                    sele_week_obj['unit_price'] = float(wdobj.last_price)
                    sele_week_obj['value'] = sele_week_obj['grand_total'] * float(wdobj.last_price)
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
                        print(global_data)
                        print('joooooooooooooooooooooooooo')
                        serializer = SalesDataCreateWeekSerializer(data=sele_week_obj)
                        if serializer.is_valid():
                            serializer.save()
                            
                        print(serializer.errors)
    except Exception as e:
        error = getattr(e, 'message', repr(e))
        logger.error(error)
        context = {'status': False,'message':'Something Went Wrong','error':error}
        return Response(context, status=status.HTTP_200_OK)
    
    
    
    
    
    
def count_success_sale_date_wise(today_date,sale_date):
    today_date = datetime.datetime.now().date()
    log_sumry = Integration_log_summary.objects.filter(created_date__date=today_date, sale_date = sale_date)
    # print()
    if not log_sumry:
        Integration_log_summary.objects.create(sale_date = sale_date, total_distributer_sale = 0, total_insart_sale = 1,invalid = 0,tranisition_source = "SFA/SFA_LITE_API")
        print(log_sumry,"======call succ",today_date,sale_date)
        # breakpoint()
    else:
        log_sumry = log_sumry.last()
        log_sumry.total_insart_sale = log_sumry.total_insart_sale + 1
        log_sumry.save()
        log_sumry.total_distributer_sale = log_sumry.invalid + log_sumry.total_insart_sale
        log_sumry.save()
        
def count_invalid_sale_date_wise(today_date,sale_date):
    print("======call fail")
    
    today_date = datetime.datetime.now().date()
    log_sumry = Integration_log_summary.objects.filter(created_date__date=today_date, sale_date = sale_date)
    
    # print()
    if not log_sumry:
        # breakpoint()
        Integration_log_summary.objects.create(sale_date = sale_date,total_distributer_sale = 0,total_insart_sale = 0,invalid = 1,tranisition_source = "SFA/SFA_LITE_API")
        print(log_sumry,"======call succ",today_date,sale_date)
    else:
        log_sumry = log_sumry.last()
        log_sumry.invalid = log_sumry.invalid + 1
        log_sumry.save()
        log_sumry.total_distributer_sale = log_sumry.invalid + log_sumry.total_insart_sale
        log_sumry.save()