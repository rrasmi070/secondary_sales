import datetime
from os import PRIO_PGRP
from rest_framework.response import Response
from base.models import Access_log, Attendence, BranchMaster, User, WDmaster
from master.models import SKU_Master_Product, Sales_Hierarchy_Master, SalesData
from rest_framework.views import APIView
import csv
from django.http import HttpResponse
from rest_framework.permissions import (AllowAny,IsAuthenticated)
import logging
logger = logging.getLogger(__name__)
from rest_framework import status
from django.db.models import Q
from django.db.models import Sum
from branch_user.reports_serializers import *
import pandas as pd
from django.db import connection
class Report_get(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        # try:
            cursor = connection.cursor()
            data_list=[]
            json_list=[]
            to_date = request.GET.get('to_date', datetime.datetime.now().date())
            from_date = request.GET.get('from_date', None)
            category = request.GET.get('category', None)
           
                
            cat_split_li = category.split(",")
          
            category_list = []
            for csl  in cat_split_li:
                category_list.append(csl.split("_")[0])
            split_cat = cat_split_li[0].split("_")
            if len(split_cat) > 1:
                if split_cat[0] is not None and split_cat[1] is not None and split_cat[2] is not None:
                    request.user=User.objects.filter(user_id=split_cat[1]).last()
                    request.user.id=split_cat[1]
                    category = split_cat[0]
                    request.user.user_type =split_cat[2]        
            transaction_type = request.GET.get('transaction_type', None)
            towns = request.GET.get('towns', None)
            wd_id = request.GET.get('wd_id', None)
            if towns:
                town_list = towns.split(",")
            else:
                town_list = None
            response = HttpResponse(content_type='text/csv')
            #>>>>>>>>>>>>>ADMIN and HO
            if request.user.user_type in ["ADMIN",'HO']:
                locationcode = request.GET.get('locationcode')
                print("ADMIN___________________________--------------------",locationcode)
                # user_id_list = User.objects.filter(locationcode = locationcode).exclude(user_type = 'BRANCH USER').values_list('user_id', flat=True)
                locationcode = locationcode.split(',') if locationcode else None
                user_id_list = User.objects.filter(locationcode__in = locationcode).exclude(user_type = 'BRANCH USER').values_list('user_id', flat=True)
                
                # print(user_id_list,'//////////??????????')
                if transaction_type.upper() == "MTD_REPORT":
                    if category_list:
                        category_list = category_list
                    else:
                        category_list = None
                    wd_idesq=str(tuple(user_id_list))
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="MTD_REPORT_BRANCH USER.csv"'
                    if len(category_list)==1:
                        # print("===========================")
                        query="""SELECT wd_name,wd_id,brand_category,sku_id,sku_code, sku_short_name,SUM(local_sales_retail),SUM( local_sales_dealer),
                        SUM(local_sales_modern_trade),SUM(local_sales_hawker),SUM(total_local_sales),SUM( outstation_sales_reatil),
                        SUM(outstation_sales_dealer),SUM( outstation_sales_modern_trade) ,SUM(outstation_sales_hawker),
                        SUM( total_outstation_sales) ,SUM(other_sales_retail),SUM( other_sales_dealer) ,SUM(other_sales_modern_trade),
                        SUM( total_other_sales),SUM(other_issues_damage),SUM( other_issues_return),SUM(other_issues_other),
                        SUM( total_issue),SUM(grand_total),statename FROM transaction_salesdata WHERE 
                        sales_date_time >= '"""+from_date+"""' AND sales_date_time <= '"""+to_date+"""' AND 
                        transaction_type = 'DAILY' AND brand_category = '"""+category_list[0]+"""' AND wd_id IN """+wd_idesq+""" GROUP BY wd_id,sku_id;"""
                    else:
                        # print("===========>>")
                        query="""SELECT wd_name,wd_id,brand_category,sku_id,sku_code,sku_short_name,SUM(local_sales_retail),SUM( local_sales_dealer),
                        SUM(local_sales_modern_trade),SUM(local_sales_hawker),SUM(total_local_sales),SUM( outstation_sales_reatil),
                        SUM(outstation_sales_dealer),SUM( outstation_sales_modern_trade) ,SUM(outstation_sales_hawker),
                        SUM( total_outstation_sales) ,SUM(other_sales_retail),SUM( other_sales_dealer) ,SUM(other_sales_modern_trade),
                        SUM( total_other_sales),SUM(other_issues_damage),SUM( other_issues_return),SUM(other_issues_other),
                        SUM( total_issue),SUM(grand_total),statename FROM transaction_salesdata WHERE 
                        sales_date_time >= '"""+from_date+"""' AND sales_date_time <= '"""+to_date+"""' AND 
                        transaction_type = 'DAILY' AND brand_category IN """+str(tuple(category_list))+""" AND wd_id IN """+wd_idesq+""" GROUP BY wd_id,sku_id;"""
                    cursor.execute(query)
                    row = cursor.fetchall()
                    for i in row:
                        wd_dict={}
                        wd_dict['Wd Name'] = i[0]
                        wd_dict['Wd ID'] = i[1]
                        wd_dict['Category'] = i[2]
                        wd_dict['Sku Id'] = i[3]
                        wd_dict['Brand Code'] = i[4]
                        wd_dict['Brand Short Name'] = i[5]
                        
                        wd_dict['Local Sales Retail'] = i[6]
                        wd_dict['Local Sales Dealer'] = i[7]
                        wd_dict['Local Sales Modern Trade'] = i[8]
                        wd_dict['Local Sales Hawker'] = i[9]
                        
                        wd_dict['Outstation Sales Retail'] = i[11]
                        wd_dict['Outstation Sales Dealer'] = i[12]
                        wd_dict['Outstation Sales Modern Trade'] = i[13]
                        wd_dict['Outstation Sales Hawker'] = i[14]
                        
                        wd_dict['Other Sales Retail'] = i[16]
                        wd_dict['Other Sales Dealer'] = i[17]
                        wd_dict['OtherSales Modern Trade'] = i[18]
                        
                        wd_dict['Total Retail'] = float(wd_dict['Local Sales Retail']) + float(wd_dict['Outstation Sales Retail']) + float(wd_dict['Other Sales Retail'])
                        wd_dict['Total Dealer'] = float(wd_dict['Local Sales Dealer'] ) + float(wd_dict['Outstation Sales Dealer'] ) + float(wd_dict['Other Sales Dealer'])
                        wd_dict['Total Modern Trade'] = float(wd_dict['Local Sales Modern Trade']) + float(wd_dict['Outstation Sales Modern Trade']) + float(+ wd_dict['OtherSales Modern Trade'])
                        wd_dict['Total Hawker'] = float(wd_dict['Local Sales Hawker']) + float(wd_dict['Outstation Sales Hawker']) 
                        
                        wd_dict['Total Local'] = i[10]
                        wd_dict['Total Outstation'] = i[15]
                        wd_dict['Grand Total'] = i[24]
                                               
                        wd_dict['Other Issues Damage'] = i[20]
                        wd_dict['Other Issues Return'] = i[21]
                        wd_dict['Other Issues Other'] = i[22]
                        wd_dict['Total Issue'] = i[23]
                        wd_dict['State'] = i[25]
                        
                        
                        # wd_dict['Total Other'] = i[19]
                        
                        
                        
                        wd_dict['Total Modern Trade'] = float(wd_dict['Local Sales Modern Trade']) + float(wd_dict['Outstation Sales Modern Trade']) + float(wd_dict['OtherSales Modern Trade'])
                        json_list.append(wd_dict)

                    df = pd.DataFrame.from_dict(list(json_list))
                    df.to_csv (response, index = False)
                    return response
                    # return Response({"message":"Invalid Transaction Type","data":json_list})
                elif user_id_list or town_list:
                    if town_list:
                        wd_town_id_list = Sales_Hierarchy_Master.objects.filter(town_code__in = town_list, wd_id__in = user_id_list).values_list('wd_town_id',flat=True)
                        Salesobj = SalesData.objects.filter(wd_id__in = list(set(user_id_list)) ,town_id__in = wd_town_id_list ,sales_date_time__gte=from_date,sales_date_time__lte=to_date,brand_category__in=category_list,transaction_type = "DAILY").values()
                    else:
                        Salesobj = SalesData.objects.filter(wd_id__in = list(set(user_id_list)),sales_date_time__gte=from_date,sales_date_time__lte=to_date,brand_category__in=category_list,transaction_type = "DAILY").values()
                    if Salesobj :
                        if transaction_type.upper() == "SALES_DATA_WD":
                            response = HttpResponse(content_type='text/csv')
                            response['Content-Disposition'] = 'attachment; filename="sec_sales_data_wd.csv"'
                            sales_data_wd_serializer = SalesDataSerialize_WD(Salesobj,many=True).data
                            # print(sales_data_wd_serializer,"=========bu========")
                            df = pd.DataFrame.from_dict(list(sales_data_wd_serializer))
                            rename_dict = {'region':'Region Name','State':'statename','town_name' :'Town Name','wd_name':'WD Name',
                                    'wd_id':'Wd Id','brand_category':'Category','sku_code':'Brand Code','sku_short_name':'Brandshort Name','sales_date_time':'Secsale Date',
                            'local_sales_retail':'Local Sales Retail','local_sales_dealer':'Local Sales Dealer','local_sales_modern_trade':'Local Sales Modern Trade','local_sales_hawker':'Local Sales Hawker',
                            'outstation_sales_reatil':'Outstation Sales Retail','outstation_sales_dealer':'Outstation Sales Dealer','outstation_sales_modern_trade':'Outstation Sales Modern Trade','outstation_sales_hawker':'Outstation Sales Hawker',
                            'other_sales_retail':'Other Sales Retail','other_sales_dealer':'Other Sales Dealer','other_sales_modern_trade':'Other Sales Modern Trade',
                            'total_retail':'Total Retail','toatal_Dealer':'Total Dealer','total_Modern_Trade_Sales':'Total Modern Trade Sales','total_Howker':'Total Hawker',
                            'total_local_sales':'Total Local','total_outstation_sales':'Total Outstation Sales',
                            # 'total_other_sales':'Total Other Sales',
                            'grand_total':'Grand Total',
                            'other_issues_damage':'Other Issues Damage','other_issues_return':'Other Issues Return','other_issues_other':'Other Issues Other','total_issue':'Total Issue','wd_type':'Transaction Source'
                            }
                            df.rename(columns=rename_dict,inplace=True)
                            df.to_csv (response, index = False)
                            return response
                        elif transaction_type.upper() == "SALES_DATA":
                            sales_data_serializer = SalesDataSerialize(Salesobj,many=True).data
                            response = HttpResponse(content_type='text/csv')
                            response['Content-Disposition'] = 'attachment; filename="sec_sales_data.csv"'
                            # print(sales_data_serializer,"=================")
                            df = pd.DataFrame.from_dict(list(sales_data_serializer))
                            rename_dict = {'region':'Region Name','State':'statename','town_name' :'Town Name','wd_name':'WD Name',
                                        
                                           'wd_id':'Wd Id','brand_category':'Category','sku_code':'Brand Code','sku_short_name':'Brandshort Name','sales_date_time':'Secsale Date',
                            'local_sales_retail':'Local Sales Retail','local_sales_dealer':'Local Sales Dealer','local_sales_modern_trade':'Local Sales Modern Trade','local_sales_hawker':'Local Sales Hawker',
                            'outstation_sales_reatil':'Outstation Sales Retail','outstation_sales_dealer':'Outstation Sales Dealer','outstation_sales_modern_trade':'Outstation Sales Modern Trade','outstation_sales_hawker':'Outstation Sales Hawker',
                            'other_sales_retail':'Other Sales Retail','other_sales_dealer':'Other Sales Dealer','other_sales_modern_trade':'Other Sales Modern Trade',
                            'total_retail':'Total Retail','toatal_Dealer':'Total Dealer','total_Modern_Trade_Sales':'Total Modern Trade Sales','total_Howker':'Total Hawker',
                            'total_local_sales':'Total Local','total_outstation_sales':'Total Outstation Sales',
                            # 'total_other_sales':'Total Other Sales',
                            'grand_total':'Grand Total',
                            'other_issues_damage':'Other Issues Damage','other_issues_return':'Other Issues Return','other_issues_other':'Other Issues Other','total_issue':'Total Issue','wd_type':'Transaction Source'
                            }
                            df.rename(columns=rename_dict,inplace=True)
                            df.to_csv (response, index = False)
                            return response
                        else:
                            return Response({"message":"Invalid Transaction Type",'status': False})
                    else:
                        return Response({"message":"There is no sales record.",'status': False})
                else:
                        return Response({"message":"You have no WD User.",'status': True})
            
            
            
            
            
            if request.user.user_type == 'BRANCH USER':
                
                print(request.user.locationcode,"@@@@@@@@@@@@@@")
                
                user_id_list = User.objects.filter(locationcode = request.user.locationcode).exclude(user_type = 'BRANCH USER').values_list('user_id', flat=True)
                # user_id_list = User.objects.filter(locationcode = request.user.locationcode).exclude(user_type = 'BRANCH USER').values_list('user_id', flat=True)
                
                
                if transaction_type.upper() == "MTD_REPORT":
                    if category_list:
                        category_list = category_list
                    else:
                        category_list = None
                    wd_idesq=str(tuple(user_id_list))
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="MTD_REPORT_BRANCH USER.csv"'
                    if len(category_list)==1:
                        query="""SELECT wd_name,wd_id,brand_category,sku_id,sku_code,sku_short_name,SUM(local_sales_retail),SUM( local_sales_dealer),
                        SUM(local_sales_modern_trade),SUM(local_sales_hawker),SUM(total_local_sales),SUM( outstation_sales_reatil),
                        SUM(outstation_sales_dealer),SUM( outstation_sales_modern_trade) ,SUM(outstation_sales_hawker),
                        SUM( total_outstation_sales) ,SUM(other_sales_retail),SUM( other_sales_dealer) ,SUM(other_sales_modern_trade),
                        SUM( total_other_sales),SUM(other_issues_damage),SUM( other_issues_return),SUM(other_issues_other),
                        SUM( total_issue),SUM(grand_total) ,statename FROM transaction_salesdata WHERE 
                        sales_date_time >= '"""+from_date+"""' AND sales_date_time <= '"""+to_date+"""' AND 
                        transaction_type = 'DAILY' AND brand_category = '"""+category_list[0]+"""' AND wd_id IN """+wd_idesq+""" GROUP BY wd_id,sku_id;"""
                    else:
                        query="""SELECT wd_name,wd_id,brand_category,sku_id,sku_code,sku_short_name,SUM(local_sales_retail),SUM( local_sales_dealer),
                        SUM(local_sales_modern_trade),SUM(local_sales_hawker),SUM(total_local_sales),SUM( outstation_sales_reatil),
                        SUM(outstation_sales_dealer),SUM( outstation_sales_modern_trade) ,SUM(outstation_sales_hawker),
                        SUM( total_outstation_sales) ,SUM(other_sales_retail),SUM( other_sales_dealer) ,SUM(other_sales_modern_trade),
                        SUM( total_other_sales),SUM(other_issues_damage),SUM( other_issues_return),SUM(other_issues_other),
                        SUM( total_issue),SUM(grand_total) ,statename FROM transaction_salesdata WHERE 
                        sales_date_time >= '"""+from_date+"""' AND sales_date_time <= '"""+to_date+"""' AND 
                        transaction_type = 'DAILY' AND brand_category IN """+str(tuple(category_list))+""" AND wd_id IN """+wd_idesq+""" GROUP BY wd_id,sku_id;"""
                    cursor.execute(query)
                    row = cursor.fetchall()
                    for i in row:
                        wd_dict={}
                        
                        wd_dict['Wd Name'] = i[0]
                        wd_dict['Wd ID'] = i[1]
                        wd_dict['Category'] = i[2]
                        wd_dict['Sku Id'] = i[3]
                        wd_dict['Brand Code'] = i[4]
                        wd_dict['Brand Short Name'] = i[5]
                        
                        wd_dict['Local Sales Retail'] = i[6]
                        wd_dict['Local Sales Dealer'] = i[7]
                        wd_dict['Local Sales Modern Trade'] = i[8]
                        wd_dict['Local Sales Hawker'] = i[9]
                        
                        wd_dict['Outstation Sales Retail'] = i[11]
                        wd_dict['Outstation Sales Dealer'] = i[12]
                        wd_dict['Outstation Sales Modern Trade'] = i[13]
                        wd_dict['Outstation Sales Hawker'] = i[14]
                        
                        wd_dict['Other Sales Retail'] = i[16]
                        wd_dict['Other Sales Dealer'] = i[17]
                        wd_dict['OtherSales Modern Trade'] = i[18]
                        
                        wd_dict['Total Retail'] = float(wd_dict['Local Sales Retail']) + float(wd_dict['Outstation Sales Retail']) + float(wd_dict['Other Sales Retail'])
                        wd_dict['Total Dealer'] = float(wd_dict['Local Sales Dealer'] ) + float(wd_dict['Outstation Sales Dealer'] ) + float(wd_dict['Other Sales Dealer'])
                        wd_dict['Total Modern Trade'] = float(wd_dict['Local Sales Modern Trade']) + float(wd_dict['Outstation Sales Modern Trade']) + float(+ wd_dict['OtherSales Modern Trade'])
                        wd_dict['Total Hawker'] = float(wd_dict['Local Sales Hawker']) + float(wd_dict['Outstation Sales Hawker']) 
                        
                        wd_dict['Total Local'] = i[10]
                        wd_dict['Total Outstation'] = i[15]
                        wd_dict['Grand Total'] = i[24]
                                               
                        wd_dict['Other Issues Damage'] = i[20]
                        wd_dict['Other Issues Return'] = i[21]
                        wd_dict['Other Issues Other'] = i[22]
                        wd_dict['Total Issue'] = i[23]
                        wd_dict['state']=i[25]
                        
                        
                        # wd_dict['Total Other'] = i[19]
                        
                        
                        
                        wd_dict['Total Modern Trade'] = float(wd_dict['Local Sales Modern Trade']) + float(wd_dict['Outstation Sales Modern Trade']) + float(wd_dict['OtherSales Modern Trade'])
                        json_list.append(wd_dict)

                    df = pd.DataFrame.from_dict(list(json_list))
                    df.to_csv (response, index = False)
                    return response
                    # return Response({"message":"Invalid Transaction Type","data":json_list})
                elif user_id_list or town_list:
                    if town_list:
                        wd_town_id_list = Sales_Hierarchy_Master.objects.filter(town_code__in = town_list, wd_id__in = user_id_list).values_list('wd_town_id',flat=True)
                        Salesobj = SalesData.objects.filter(wd_id__in = list(set(user_id_list)) ,town_id__in = wd_town_id_list ,sales_date_time__gte=from_date,sales_date_time__lte=to_date,brand_category__in=category_list,transaction_type = "DAILY").values()
                    else:
                        Salesobj = SalesData.objects.filter(wd_id__in = list(set(user_id_list)),sales_date_time__gte=from_date,sales_date_time__lte=to_date,brand_category__in=category_list,transaction_type = "DAILY").values()
                    if Salesobj :
                        if transaction_type.upper() == "SALES_DATA_WD":
                            response = HttpResponse(content_type='text/csv')
                            response['Content-Disposition'] = 'attachment; filename="sec_sales_data_wd.csv"'
                            sales_data_wd_serializer = SalesDataSerialize_WD(Salesobj,many=True).data
                            # print(sales_data_wd_serializer,"=========bu========")
                            df = pd.DataFrame.from_dict(list(sales_data_wd_serializer))
                            rename_dict = {'region':'Region Name','State':'statename','town_name' :'Town Name','wd_name':'WD Name',
                                    'wd_id':'Wd Id','brand_category':'Category','sku_code':'Brand Code','sku_short_name':'Brandshort Name','sales_date_time':'Secsale Date',
                            'local_sales_retail':'Local Sales Retail','local_sales_dealer':'Local Sales Dealer','local_sales_modern_trade':'Local Sales Modern Trade','local_sales_hawker':'Local Sales Hawker',
                            'outstation_sales_reatil':'Outstation Sales Retail','outstation_sales_dealer':'Outstation Sales Dealer','outstation_sales_modern_trade':'Outstation Sales Modern Trade','outstation_sales_hawker':'Outstation Sales Hawker',
                            'other_sales_retail':'Other Sales Retail','other_sales_dealer':'Other Sales Dealer','other_sales_modern_trade':'Other Sales Modern Trade',
                            'total_retail':'Total Retail','toatal_Dealer':'Total Dealer','total_Modern_Trade_Sales':'Total Modern Trade Sales','total_Howker':'Total Hawker',
                            'total_local_sales':'Total Local','total_outstation_sales':'Total Outstation Sales',
                            # 'total_other_sales':'Total Other Sales',
                            'grand_total':'Grand Total',
                            'other_issues_damage':'Other Issues Damage','other_issues_return':'Other Issues Return','other_issues_other':'Other Issues Other','total_issue':'Total Issue','wd_type':'Transaction Source'
                            }
                            df.rename(columns=rename_dict,inplace=True)
                            df.to_csv (response, index = False)
                            return response
                        elif transaction_type.upper() == "SALES_DATA":
                            sales_data_serializer = SalesDataSerialize(Salesobj,many=True).data
                            response = HttpResponse(content_type='text/csv')
                            response['Content-Disposition'] = 'attachment; filename="sec_sales_data.csv"'
                            # print(sales_data_serializer,"=================")
                            df = pd.DataFrame.from_dict(list(sales_data_serializer))
                            rename_dict = {'region':'Region Name','State':'statename','town_name' :'Town Name','wd_name':'WD Name',
                                        
                                           'wd_id':'Wd Id','brand_category':'Category','sku_code':'Brand Code','sku_short_name':'Brandshort Name','sales_date_time':'Secsale Date',
                            'local_sales_retail':'Local Sales Retail','local_sales_dealer':'Local Sales Dealer','local_sales_modern_trade':'Local Sales Modern Trade','local_sales_hawker':'Local Sales Hawker',
                            'outstation_sales_reatil':'Outstation Sales Retail','outstation_sales_dealer':'Outstation Sales Dealer','outstation_sales_modern_trade':'Outstation Sales Modern Trade','outstation_sales_hawker':'Outstation Sales Hawker',
                            'other_sales_retail':'Other Sales Retail','other_sales_dealer':'Other Sales Dealer','other_sales_modern_trade':'Other Sales Modern Trade',
                            'total_retail':'Total Retail','toatal_Dealer':'Total Dealer','total_Modern_Trade_Sales':'Total Modern Trade Sales','total_Howker':'Total Hawker',
                            'total_local_sales':'Total Local','total_outstation_sales':'Total Outstation Sales',
                            # 'total_other_sales':'Total Other Sales',
                            'grand_total':'Grand Total',
                            'other_issues_damage':'Other Issues Damage','other_issues_return':'Other Issues Return','other_issues_other':'Other Issues Other','total_issue':'Total Issue','wd_type':'Transaction Source'
                            }
                            df.rename(columns=rename_dict,inplace=True)
                            df.to_csv (response, index = False)
                            return response
                        else:
                            return Response({"message":"Invalid Transaction Type",'status': False})
                    else:
                        return Response({"message":"There is no sales record.",'status': False})
                else:
                        return Response({"message":"You have no WD User.",'status': True})
            #>>>>>>>>>>>>>>>>>>>>>>> ADMIN >>>>>>>>>>>>>>>>>>>>>>>
            
            
            
            
            elif request.user.user_type == "WD":
                Salesobj = SalesData.objects.filter(wd_id = request.user.user_id ,sales_date_time__gte=from_date,sales_date_time__lte=to_date,brand_category__in=category_list,transaction_type = "DAILY").values()
                if Salesobj:
                    if transaction_type.upper() == "MTD_REPORT":
                        if category_list:
                            category_list = category_list
                        else:
                            category_list = None
                        wd_idesq = request.user.user_id
                        response = HttpResponse(content_type='text/csv')
                        response['Content-Disposition'] = 'attachment; filename="MTD_REPORT_BRANCH USER.csv"'
                        if len(category_list)==1:
                            query="""SELECT wd_name,wd_id,brand_category,sku_id,sku_code,sku_short_name,SUM(local_sales_retail),SUM( local_sales_dealer),
                            SUM(local_sales_modern_trade),SUM(local_sales_hawker),SUM(total_local_sales),SUM( outstation_sales_reatil),
                            SUM(outstation_sales_dealer),SUM( outstation_sales_modern_trade) ,SUM(outstation_sales_hawker),
                            SUM( total_outstation_sales) ,SUM(other_sales_retail),SUM( other_sales_dealer) ,SUM(other_sales_modern_trade),
                            SUM( total_other_sales),SUM(other_issues_damage),SUM( other_issues_return),SUM(other_issues_other),
                            SUM( total_issue),SUM(grand_total)  FROM transaction_salesdata WHERE 
                            sales_date_time >= '"""+from_date+"""' AND sales_date_time <= '"""+to_date+"""' AND 
                            transaction_type = 'DAILY' AND brand_category = '"""+category_list[0]+"""' AND wd_id = '"""+wd_idesq+"""' GROUP BY wd_id,sku_id;"""
                        else:
                            query="""SELECT wd_name,wd_id,brand_category,sku_id,sku_code,sku_short_name,SUM(local_sales_retail),SUM( local_sales_dealer),
                            SUM(local_sales_modern_trade),SUM(local_sales_hawker),SUM(total_local_sales),SUM( outstation_sales_reatil),
                            SUM(outstation_sales_dealer),SUM( outstation_sales_modern_trade) ,SUM(outstation_sales_hawker),
                            SUM( total_outstation_sales) ,SUM(other_sales_retail),SUM( other_sales_dealer) ,SUM(other_sales_modern_trade),
                            SUM( total_other_sales),SUM(other_issues_damage),SUM( other_issues_return),SUM(other_issues_other),
                            SUM( total_issue),SUM(grand_total) FROM transaction_salesdata WHERE 
                            sales_date_time >= '"""+from_date+"""' AND sales_date_time <= '"""+to_date+"""' AND 
                            transaction_type = 'DAILY' AND brand_category IN """+str(tuple(category_list))+""" AND wd_id = '"""+wd_idesq+"""' GROUP BY wd_id,sku_id;"""
                        cursor.execute(query)
                        row = cursor.fetchall()
                        for i in row:
                            wd_dict={}
                            wd_dict['Wd Name'] = i[0]
                            wd_dict['Wd ID'] = i[1]
                            wd_dict['Category'] = i[2]
                            wd_dict['Sku Id'] = i[3]
                            wd_dict['Brand Code'] = i[4]
                            wd_dict['Brand Short Name'] = i[5]
                            
                            wd_dict['Local Sales Retail'] = i[6]
                            wd_dict['Local Sales Dealer'] = i[7]
                            wd_dict['Local Sales Modern Trade'] = i[8]
                            wd_dict['Local Sales Hawker'] = i[9]
                            
                            wd_dict['Outstation Sales Retail'] = i[11]
                            wd_dict['Outstation Sales Dealer'] = i[12]
                            wd_dict['Outstation Sales Modern Trade'] = i[13]
                            wd_dict['Outstation Sales Hawker'] = i[14]
                            
                            wd_dict['Other Sales Retail'] = i[16]
                            wd_dict['Other Sales Dealer'] = i[17]
                            wd_dict['OtherSales Modern Trade'] = i[18]
                            
                            wd_dict['Total Retail'] = float(wd_dict['Local Sales Retail']) + float(wd_dict['Outstation Sales Retail']) + float(wd_dict['Other Sales Retail'])
                            wd_dict['Total Dealer'] = float(wd_dict['Local Sales Dealer'] ) + float(wd_dict['Outstation Sales Dealer'] ) + float(wd_dict['Other Sales Dealer'])
                            wd_dict['Total Modern Trade'] = float(wd_dict['Local Sales Modern Trade']) + float(wd_dict['Outstation Sales Modern Trade']) + float(+ wd_dict['OtherSales Modern Trade'])
                            wd_dict['Total Hawker'] = float(wd_dict['Local Sales Hawker']) + float(wd_dict['Outstation Sales Hawker']) 
                            
                            wd_dict['Total Local'] = i[10]
                            wd_dict['Total Outstation'] = i[15]
                            wd_dict['Grand Total'] = i[24]
                                                
                            wd_dict['Other Issues Damage'] = i[20]
                            wd_dict['Other Issues Return'] = i[21]
                            wd_dict['Other Issues Other'] = i[22]
                            wd_dict['Total Issue'] = i[23]
                            # wd_dict['Wd Name'] = i[0]
                            # wd_dict['Wd ID'] = i[1]
                            # wd_dict['Category'] = i[2]
                            # wd_dict['Sku Id'] = i[3]
                            # wd_dict['Sku Code'] = i[4]
                            # wd_dict['Brand Short Name'] = i[5]
                            # wd_dict['Local Sales Retail'] = i[6]
                            # wd_dict['Local Sales Dealer'] = i[7]
                            # wd_dict['Local Sales Modern Trade'] = i[8]
                            # wd_dict['Local Sales Hawker'] = i[9]
                            # wd_dict['Total Local'] = i[10]
                            # wd_dict['Outstation Sales Retail'] = i[11]
                            # wd_dict['Outstation Sales Dealer'] = i[12]
                            # wd_dict['Outstation Sales Modern Trade'] = i[13]
                            # wd_dict['Outstation Sales Hawker'] = i[14]
                            # wd_dict['Total Outstation'] = i[15]
                            # wd_dict['Other Sales Retail'] = i[16]
                            # wd_dict['Other Sales Dealer'] = i[17]
                            # wd_dict['OtherSales Modern Trade'] = i[18]
                            # wd_dict['Total Other'] = i[19]
                            # wd_dict['Other Issues Damage'] = i[20]
                            # wd_dict['Other Issues Return'] = i[21]
                            # wd_dict['Other Issues Other'] = i[22]
                            # wd_dict['Total Issue'] = i[23]
                            # wd_dict['Grand Total'] = i[24]
                            # wd_dict['Total Retail'] = float(wd_dict['Local Sales Retail']) + float(wd_dict['Outstation Sales Retail']) + float(wd_dict['Other Sales Retail'])
                            # wd_dict['Total Dealer'] = float(wd_dict['Local Sales Dealer'] ) + float(wd_dict['Outstation Sales Dealer'] ) + float(wd_dict['Other Sales Dealer'])
                            # wd_dict['Total Hawker'] = float(wd_dict['Local Sales Hawker']) + float(wd_dict['Outstation Sales Hawker'])
                            # wd_dict['Total Modern Trade'] = float(wd_dict['Local Sales Modern Trade']) + float(wd_dict['Outstation Sales Modern Trade']) + float(wd_dict['OtherSales Modern Trade'])
                            json_list.append(wd_dict)

                        df = pd.DataFrame.from_dict(list(json_list))
                        df.to_csv (response, index = False)
                        return response
        
                        # return Response({"message":"Invalid Transaction Type","data":dataframe_list})
                    # else:
                    #     return Response({"message":"You have no sales record.",'status': True})
                    elif Salesobj:
                        if transaction_type:
                            wd_sales_data_serializer = WD_SalesDataSerialize(Salesobj, many = True).data
                            response = HttpResponse(content_type='text/csv')
                            response['Content-Disposition'] = 'attachment; filename="wd_sec_sales_data.csv"'
                            df = pd.DataFrame.from_dict(list(wd_sales_data_serializer))
                            rename_dict = {
                                # 'wd_name':'WD Name','wd_id':'Wd Id',
                                'town_name' :'Town Name','wd_name':'WD Name','wd_id':'Wd Id','brand_category':'Category','sku_code':'Brand Code','sku_short_name':'Brand Short Name','sales_date_time':'Secsale Date',
                                'local_sales_retail':'Local Sales Retail','local_sales_dealer':'Local Sales Dealer','local_sales_modern_trade':'Local Sales Modern Trade','local_sales_hawker':'Local Sales Hawker',
                                'outstation_sales_reatil':'Outstation Sales Retail','outstation_sales_dealer':'Outstation Sales Dealer','outstation_sales_modern_trade':'Outstation Sales Modern Trade','outstation_sales_hawker':'Outstation Sales Hawker',
                                'other_sales_retail':'Other Sales Retail','other_sales_dealer':'Other Sales Dealer','other_sales_modern_trade':'Other Sales Modern Trade',
                                'total_retail':'Total Retail','toatal_Dealer':'Total Dealer','total_Modern_Trade_Sales':'Total Modern Trade Sales','total_Howker':'Total Hawker',
                                'total_local_sales':'Total Local','total_outstation_sales':'Total Outstation Sales',
                                # 'total_other_sales':'Total Other Sales',
                                'grand_total':'Grand Total',
                                'other_issues_damage':'Other Issues Damage','other_issues_return':'Other Issues Return','other_issues_other':'Other Issues Other','total_issue':'Total Issue',
                                'wd_type':'Transaction Source'
                            }
                            df.rename(columns=rename_dict,inplace=True)
                            df.to_csv (response, index = False)
                            return response
                else:
                    return Response({"message":"You have no sales record.", "data":Salesobj,'status': True})
            else:
                return Response({"message":"Invalid User Type.",'status': False})
        # except Exception as e:
        #     error = getattr(e, 'message', repr(e))
        #     logger.error(error)
        #     context = {'status': False,'message':'Something Went Wrong','error':error}
        #     return Response(context, status=status.HTTP_200_OK)

class WeeklyReport_get(APIView):
    
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        try:
            # sales_type=request.GET.get('transaction_type',None)
            sales_year=request.GET.get('sales_year',None)
            sales_month=request.GET.get('sales_month',None)      
            weekno=request.GET.get('week',None)
            town_code = request.GET.get('town_code', None)
            
            week_li=weekno.split(",")
            print(week_li)



            
            
            # print(weekno)
            
            
        

            if request.user.user_type in ["BRANCH USER","ADMIN" , "HO"] :
                town_split_li = town_code.split(",")
                json_list = []
                print(town_split_li)
                data=SalesData.objects.filter(sales_date_time__month=sales_month , sales_date_time__year=sales_year,town_code__in=town_split_li,transaction_type__in=week_li).values()
                serializer_class=WeeklyDataSerialize(data,many=True)
                for i in serializer_class.data:
                    # print(dict(i))
                    i=dict(i)
                    # print(i['wd_name'])
                    wd_dict={}
                    wd_dict['Region Name'] = i['region']
                    wd_dict['Town Name'] = i['town_name']
                    # wd_dict['Town Code'] = i['town_code']
                    

                    wd_dict['Wd Name'] = i['wd_name']
                    wd_dict['Wd ID'] = i['wd_id']
                    wd_dict['Category'] = i['brand_category']
                    # wd_dict['Sku Id'] = i['sku_id']
                    wd_dict['Brand Code'] = i['sku_code']
                    wd_dict['Brandshort Name'] = i['sku_short_name']
                    wd_dict['Secsale date']=i['sales_date_time']
                    
                    wd_dict['Local Sales Retail'] = i['local_sales_retail']
                    wd_dict['Local Sales Dealer'] = i['local_sales_dealer']
                    wd_dict['Local Sales Modern Trade'] = i['local_sales_modern_trade']
                    wd_dict['Local Sales Hawker'] = i['local_sales_hawker']
                    
                    wd_dict['Outstation Sales Retail'] = i['outstation_sales_reatil']
                    wd_dict['Outstation Sales Dealer'] = i['outstation_sales_dealer']
                    wd_dict['Outstation Sales Modern Trade'] = i['outstation_sales_modern_trade']
                    wd_dict['Outstation Sales Hawker'] = i['outstation_sales_hawker']
                    
                    wd_dict['Other Sales Retail'] = i['other_sales_retail']
                    wd_dict['Other Sales Dealer'] = i['other_sales_dealer']
                    wd_dict['Other Sales Modern Trade'] = i['other_sales_modern_trade']
                    
                    wd_dict['Total Retail'] = float(wd_dict['Local Sales Retail']) + float(wd_dict['Outstation Sales Retail']) + float(wd_dict['Other Sales Retail'])
                    wd_dict['Total Dealer'] = float(wd_dict['Local Sales Dealer'] ) + float(wd_dict['Outstation Sales Dealer'] ) + float(wd_dict['Other Sales Dealer'])
                    wd_dict['Total Modern Trade Sales'] = float(wd_dict['Local Sales Modern Trade']) + float(wd_dict['Outstation Sales Modern Trade']) + float(+ wd_dict['Other Sales Modern Trade'])
                    wd_dict['Total Hawker'] = float(wd_dict['Local Sales Hawker']) + float(wd_dict['Outstation Sales Hawker']) 
                    
                    wd_dict['Total Local'] = i['total_local_sales']
                    wd_dict['Total Outstation Sales'] = i['total_outstation_sales']
                    wd_dict['Grand Total'] = i['grand_total']
                                        
                    wd_dict['Other Issues Damage'] = i['other_issues_damage']
                    wd_dict['Other Issues Return'] = i['other_issues_return']
                    wd_dict['Other Issues Other'] = i['other_issues_other']
                    wd_dict['Total Issue'] = i['total_issue']
                    wd_dict['Transaction Source'] = i['wd_type']
                    wd_dict['Sales Week'] = i['transaction_type']
                    



                    json_list.append(wd_dict)
                if data:
                    return Response({"status":True,"message":"Success","data":json_list})
                else:
                    return Response({"status":False,"message":"No Record Found"})
                # .values(
                    # "brand_category","sku_id","wd_id","town_id","sales_date_time","local_sales_retail","local_sales_dealer","local_sales_modern_trade","local_sales_hawker","total_local_sales",
                    # "outstation_sales_reatil","outstation_sales_dealer","outstation_sales_modern_trade","outstation_sales_hawker","total_outstation_sales","other_sales_retail",
                    # "other_sales_dealer","other_sales_modern_trade","total_other_sales","other_issues_damage","other_issues_return","other_issues_other","total_issue",
                    # "grand_total","created_by","last_updated","transaction_source","created_date","last_updated_date","status","freeze_status","transaction_type","company","unit_price",
                    # "region","cnf_id","value","wd_name","wd_type","sku_code","sku_short_name","town_name","town_code","distrcode")
                
                # response=data
                # return Response(response,status=status.HTTP_200_OK)
            elif  request.user.user_type=="WD":
                wd_id = request.user.user_id
                json_list = []
                data=SalesData.objects.filter(sales_date_time__month=sales_month , sales_date_time__year=sales_year,transaction_type__in=week_li,wd_id=wd_id).values()
                serializer_class=WD_WeeklyDataSerialize(data,many=True)
                for i in serializer_class.data:
                    i=dict(i)
                    print(i['wd_name'],"=================//")
                    wd_dict={}
                    wd_dict['Region Name'] = i['region']
                    wd_dict['Town Name'] = i['town_name']
                    # wd_dict['Town Code'] = i['town_code']
                    

                    wd_dict['Wd Name'] = i['wd_name']
                    wd_dict['Wd ID'] = i['wd_id']
                    wd_dict['Category'] = i['brand_category']
                    # wd_dict['Sku Id'] = i['sku_id']
                    wd_dict['Brand Code'] = i['sku_code']
                    wd_dict['Brandshort Name'] = i['sku_short_name']
                    wd_dict['Secsale date']=i['sales_date_time']
                    
                    wd_dict['Local Sales Retail'] = i['local_sales_retail']
                    wd_dict['Local Sales Dealer'] = i['local_sales_dealer']
                    wd_dict['Local Sales Modern Trade'] = i['local_sales_modern_trade']
                    wd_dict['Local Sales Hawker'] = i['local_sales_hawker']
                    
                    wd_dict['Outstation Sales Retail'] = i['outstation_sales_reatil']
                    wd_dict['Outstation Sales Dealer'] = i['outstation_sales_dealer']
                    wd_dict['Outstation Sales Modern Trade'] = i['outstation_sales_modern_trade']
                    wd_dict['Outstation Sales Hawker'] = i['outstation_sales_hawker']
                    
                    wd_dict['Other Sales Retail'] = i['other_sales_retail']
                    wd_dict['Other Sales Dealer'] = i['other_sales_dealer']
                    wd_dict['Other Sales Modern Trade'] = i['other_sales_modern_trade']
                    
                    wd_dict['Total Retail'] = float(wd_dict['Local Sales Retail']) + float(wd_dict['Outstation Sales Retail']) + float(wd_dict['Other Sales Retail'])
                    wd_dict['Total Dealer'] = float(wd_dict['Local Sales Dealer'] ) + float(wd_dict['Outstation Sales Dealer'] ) + float(wd_dict['Other Sales Dealer'])
                    wd_dict['Total Modern Trade Sales'] = float(wd_dict['Local Sales Modern Trade']) + float(wd_dict['Outstation Sales Modern Trade']) + float(+ wd_dict['Other Sales Modern Trade'])
                    wd_dict['Total Hawker'] = float(wd_dict['Local Sales Hawker']) + float(wd_dict['Outstation Sales Hawker']) 
                    
                    wd_dict['Total Local'] = i['total_local_sales']
                    wd_dict['Total Outstation Sales'] = i['total_outstation_sales']
                    wd_dict['Grand Total'] = i['grand_total']
                                        
                    wd_dict['Other Issues Damage'] = i['other_issues_damage']
                    wd_dict['Other Issues Return'] = i['other_issues_return']
                    wd_dict['Other Issues Other'] = i['other_issues_other']
                    wd_dict['Total Issue'] = i['total_issue']
                    wd_dict['Transaction Source'] = i['wd_type']
                    wd_dict['Sales Week'] = i['transaction_type']



                    json_list.append(wd_dict)
                # return Response(serializer_class.data)
                if data:
                    return Response({"status":True,"message":"Success","data":json_list})
                else:
                    return Response({"status":False,"message":"No Record Found"})

                # .values(
                #     "brand_category","sku_id","wd_id","town_id","sales_date_time","local_sales_retail","local_sales_dealer","local_sales_modern_trade","local_sales_hawker","total_local_sales",
                #     "outstation_sales_reatil","outstation_sales_dealer","outstation_sales_modern_trade","outstation_sales_hawker","total_outstation_sales","other_sales_retail",
                #     "other_sales_dealer","other_sales_modern_trade","total_other_sales","other_issues_damage","other_issues_return","other_issues_other","total_issue",
                #     "grand_total","created_by","last_updated","transaction_source","created_date","last_updated_date","status","freeze_status","transaction_type","company","unit_price",
                #     "region","cnf_id","value","wd_name","wd_type","sku_code","sku_short_name","town_name","town_code","distrcode")

                print(">>>>>>>>>>>>>>>>>>>>>>>WD",data)
                response=data
                return Response(response,status=status.HTTP_200_OK)
                

            else:            
                # return HttpResponse(" API Not working")
                return HttpResponse("Called Other User")
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong','error':error}
            return Response(context, status=status.HTTP_200_OK)
        
        

class Attendence_Report_get(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        try:
            from_date = request.GET.get('from_date',None)
            to_date = request.GET.get('to_date',None)

            # request.user.user_type=="BRANCH USER"
            

            # if request.user.user_type=="BRANCH USER":
            if request.user.user_type in ["BRANCH USER","ADMIN" , "HO"] :
                
                town_code=request.GET.get('town_code',None)
                # town_code="0112300"
                town_code_li=town_code.split(",")
                wd_id_list=Sales_Hierarchy_Master.objects.filter(town_code__in=town_code_li).values_list('wd_id',flat=True)
                print(wd_id_list)
                attendence=Attendence.objects.filter(user_id__in=wd_id_list,added_on__date__gte=from_date,added_on__date__lte=to_date)
                print(attendence)
                serializer_class=AttendenceSerializer(attendence,many=True)
                print("<<<<<<<<<<<<<<<<<<<<<<....................")
                return Response(serializer_class.data)
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong','error':error}
            return Response(context, status=status.HTTP_200_OK)
        




class Attendence_access_Report(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self,request):
        
        from_date = request.GET.get('from_date',None)
        to_date = request.GET.get('to_date',None)



        # if request.user.user_type=="BRANCH USER":
        if request.user.user_type in ["BRANCH USER","ADMIN" , "HO"] :
            

            report_type=request.GET.get('report_type',None)
            # report_type=report_type.upper()

            if report_type.upper() == "ATTENDENCE":
                print(report_type,"WWWWWWWWWWWWWWWWWW")

                town_code=request.GET.get('town_code',None)
                # town_code="0112300"
                town_code_li=town_code.split(",")
                wd_id_list=Sales_Hierarchy_Master.objects.filter(town_code__in=town_code_li).values_list('wd_id',flat=True)
                print(wd_id_list)
                attendence=Attendence.objects.filter(user_id__in=wd_id_list,added_on__date__gte=from_date,added_on__date__lte=to_date)
                print(attendence)
                serializer_class=AttendenceSerializer(attendence,many=True)
                print("<<<<<<<<<<<<<<<< ................")
                if attendence: 
                    return Response({"status":True,"message":"Success","data":serializer_class.data})
                else:
                    return Response({"status":False,"message":"No Record Found"})


                
            elif report_type.upper()=="ACCESSLOG":
                town_code=request.GET.get('town_code',None)
                # town_code="0112300"
                town_code_li=town_code.split(",")
                wd_id_list=Sales_Hierarchy_Master.objects.filter(town_code__in=town_code_li).values_list('wd_id',flat=True)
                print(wd_id_list)
                
                access_log=Access_log.objects.filter(user_id__in=wd_id_list,created_at__date__gte=from_date,created_at__date__lte=to_date)
                print(access_log)
                # breakpoint()
                serializer_class=AccessSerializer(access_log,many=True)
                print("<<<<<<<<<<<<<<<< ................")
                if access_log: 
                    return Response({"status":True,"message":"Success","data":serializer_class.data})
                else:
                    return Response({"status":False,"message":"No Record Found"})

                # return Response(serializer_class.data)

            else:
                return HttpResponse("Invalid Request")
