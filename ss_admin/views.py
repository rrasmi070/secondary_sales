import json
from branch_user.views import current_week
from django.db import transaction
from datetime import date
from dateutil.relativedelta import relativedelta
from wd.serializers import *
from ss_admin.serializers import *
from master.serializers import *
from master.models import SalesData, SKU_Master_Product, Sales_Hierarchy_Master
from branch_user.serializers import UserSerialize_getWD, WDmaster_wd_town
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from pymysql import NULL
from django.db.models.expressions import Exists
from http.client import ImproperConnectionState
from functools import partial
from datetime import timedelta
from django.db import connection
# from django.utils import simplejson
import pandas as pd
from branch_user.reports_serializers import *
from django.db.models import Sum
from django.db.models import Q
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from dateutil import parser
from base.models import User
from rest_framework import status
import datetime
from rest_framework.response import Response
from base.models import Access_log, Attendence, BranchMaster, User, WDmaster
# from ss_admin.serializers import BranchListSerializer
from master.models import SKU_Master_Product, Sales_Hierarchy_Master, SalesData
from rest_framework.views import APIView
import csv
from django.http import HttpResponse
from rest_framework.permissions import (AllowAny, IsAuthenticated)
import logging
logger = logging.getLogger(__name__)

# import imp
logger = logging.getLogger(__name__)

# Create your views here.


class Test(APIView):
    def get(self, request):
        return Response("HIiii===========")\



class BranchList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:

            if request.user.user_type == "ADMIN":

                # user_type="BRANCH USER"

                branch_list = BranchMaster.objects.all().values( 'branch_name', 'region', 'branch_code')
                # branch_list=User.objects.filter('branch_name', 'region', 'branch_code'
                    # ).all().values()
                    
                    # 'branch_name', 'region', 'branch_code','user_id','user_type')
                # # print(branch_list)
                # serializer=BranchListSerializer(branch_list,many=True)
                # datalist=serializer.data
                if branch_list:

                    response = {'status': True,
                        "data": branch_list, 'message': 'Success'}
                else:
                    response = {'status': True,
                        'message': 'No branch you have'}
                return Response(response)
            return Response({'status': False, 'message': 'Invalid req'})

        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False, 'message': 'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)


class WDTownlist(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        try:

            branch_code = request.GET.get("branch_code", None)
            # branch_code= "01,04"
            branch_code_li = branch_code.split(',') if branch_code else None
            # branch_code_li = branch_code.split(',')

            user_id_li = User.objects.filter(locationcode__in=branch_code_li).exclude(
                user_type="BRANCH USER").values_list("user_id", flat=True)
            wlist = WDmaster.objects.filter(
                wd_ids__in=user_id_li).values('wd_postal_code').distinct()

            
            if wlist:
                    serializer = Wmaster_wd_towns(wlist, many=True)
                    wlist = serializer.data
            # wlist = Sales_Hierarchy_Master.objects.filter(
            #     region_code__in=branch_code_li).values('town', 'town_code').distinct()
            if wlist:

                response = {'status': True,
                    "data": wlist, 'message': 'Success'}
            else:
                response = {'status': True, 'message': 'No Towns you have'}

            # serializer=WDListSerializer(wlist,many=True)

            return Response(response)

        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False, 'message': 'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)
# from django.core import serializers
from django.core import serializers as ABC
# from rest_framework import serializers
class WDlist(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:

            town_code = request.GET.get("town_code", None)
            # town_code="0174700,0112300,0166800"
            town_code_li = town_code.split(",")
            wdlist = Sales_Hierarchy_Master.objects.filter(
                town_code__in=town_code_li).values('wd_id')

            wname = User.objects.filter(
                user_id__in=wdlist).values('user_id', 'first_name')
            # serializer=WDListSerializer(wname,many=True)
            if wname:

                response = {'status': True,
                    "data": wname, 'message': 'Success'}

            else:
                response = {'status': True, 'message': 'No data '}

            return Response(response)
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False, 'message': 'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)

from rest_framework import generics
from rest_framework.mixins import ListModelMixin
# >>>>>>>>>>>>>>>>>>> Report Section

# class Admin_HO_Report_get(APIView):
class Admin_HO_Report_get(generics.GenericAPIView,ListModelMixin):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # try:
            cursor = connection.cursor()
            data_list = []
            json_list = []
            to_date = request.GET.get(
                'to_date', datetime.datetime.now().date())
            from_date = request.GET.get('from_date', None)
            category = request.GET.get('category', None)
            cat_split_li = category.split(",")
            category_list = []
            for csl in cat_split_li:
                category_list.append(csl.split("_")[0])
            split_cat = cat_split_li[0].split("_")
            # if len(split_cat) > 1:
            #     if split_cat[0] is not None and split_cat[1] is not None and split_cat[2] is not None:
            #         request.user = User.objects.filter(
            #             user_id=split_cat[1]).last()
            #         request.user.id = split_cat[1]
            #         category = split_cat[0]
            #         request.user.user_type = split_cat[2]
            transaction_type = request.GET.get('transaction_type', None)
            towns = request.GET.get('towns', None)
            # wd_id = request.GET.get('wd_id', None)
            branch = request.GET.get('branch_id', None)
            if towns:
                town_list = towns.split(',')
            else:
                town_list = None
            print(category)
            print(towns)
            print(transaction_type, branch)
            # breakpoint()
            response = HttpResponse(content_type='text/csv')
            if request.user.user_type == 'ADMIN' or "HO":
                # user=User.objects.filter(user_id=branch).last()
                # print(user.locationcode,">>>>>>>>>>>>>>>>>>>>>bbbbbbb")
                # user_id_list = User.objects.filter(locationcode = user.locationcode).values_list('user_id', flat=True)
                # print(user_id_list,"LLLLLLLLLLLLLLLLL")
                if town_list:
                    wd_town_id_list = Sales_Hierarchy_Master.objects.filter(town_code__in=town_list).values_list('wd_id', flat=True)
                
                else:
                    wd_town_id_list = Sales_Hierarchy_Master.objects.all().values_list('wd_id', flat=True)
                    
                    
                if transaction_type.upper() == "MTD_REPORT":
                    if category_list:
                        category_list = category_list
                    else:
                        category_list = None
                    wd_idesq = str(tuple(wd_town_id_list))
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="MTD_REPORT_BRANCH USER.csv"'
                    if len(category_list) == 1:
                        query = """SELECT wd_name,wd_id,brand_category,sku_id,sku_code,sku_short_name,SUM(local_sales_retail),SUM( local_sales_dealer),
                        SUM(local_sales_modern_trade),SUM(local_sales_hawker),SUM(
                            total_local_sales),SUM( outstation_sales_reatil),
                        SUM(outstation_sales_dealer),SUM(
                            outstation_sales_modern_trade) ,SUM(outstation_sales_hawker),
                        SUM( total_outstation_sales) ,SUM(other_sales_retail),SUM(
                            other_sales_dealer) ,SUM(other_sales_modern_trade),
                        SUM( total_other_sales),SUM(other_issues_damage),SUM(
                            other_issues_return),SUM(other_issues_other),
                        SUM( total_issue),SUM(grand_total)  FROM transaction_salesdata WHERE
                        sales_date_time >= '"""+from_date+"""' AND sales_date_time <= '"""+to_date+"""' AND
                        transaction_type = 'DAILY' AND brand_category = '"""+category_list[0]+"""' AND wd_id IN """+wd_idesq+""" GROUP BY wd_id,sku_id;"""
                    else:
                        query = """SELECT wd_name,wd_id,brand_category,sku_id,sku_code,sku_short_name,SUM(local_sales_retail),SUM( local_sales_dealer),
                        SUM(local_sales_modern_trade),SUM(local_sales_hawker),SUM(
                            total_local_sales),SUM( outstation_sales_reatil),
                        SUM(outstation_sales_dealer),SUM(
                            outstation_sales_modern_trade) ,SUM(outstation_sales_hawker),
                        SUM( total_outstation_sales) ,SUM(other_sales_retail),SUM(
                            other_sales_dealer) ,SUM(other_sales_modern_trade),
                        SUM( total_other_sales),SUM(other_issues_damage),SUM(
                            other_issues_return),SUM(other_issues_other),
                        SUM( total_issue),SUM(grand_total) FROM transaction_salesdata WHERE
                        sales_date_time >= '"""+from_date+"""' AND sales_date_time <= '"""+to_date+"""' AND
                        transaction_type = 'DAILY' AND brand_category IN """+str(tuple(category_list))+""" AND wd_id IN """+wd_idesq+""" GROUP BY wd_id,sku_id;"""
                    cursor.execute(query)
                    row = cursor.fetchall()
                    for i in row:
                        wd_dict = {}
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

                        wd_dict['Total Retail'] = float(wd_dict['Local Sales Retail']) + float(
                            wd_dict['Outstation Sales Retail']) + float(wd_dict['Other Sales Retail'])
                        wd_dict['Total Dealer'] = float(wd_dict['Local Sales Dealer']) + float(
                            wd_dict['Outstation Sales Dealer']) + float(wd_dict['Other Sales Dealer'])
                        wd_dict['Total Modern Trade'] = float(wd_dict['Local Sales Modern Trade']) + float(
                            wd_dict['Outstation Sales Modern Trade']) + float(+ wd_dict['OtherSales Modern Trade'])
                        wd_dict['Total Hawker'] = float(
                            wd_dict['Local Sales Hawker']) + float(wd_dict['Outstation Sales Hawker'])

                        wd_dict['Total Local'] = i[10]
                        wd_dict['Total Outstation'] = i[15]
                        wd_dict['Grand Total'] = i[24]

                        wd_dict['Other Issues Damage'] = i[20]
                        wd_dict['Other Issues Return'] = i[21]
                        wd_dict['Other Issues Other'] = i[22]
                        wd_dict['Total Issue'] = i[23]

                        # wd_dict['Total Other'] = i[19]

                        wd_dict['Total Modern Trade'] = float(wd_dict['Local Sales Modern Trade']) + float(
                            wd_dict['Outstation Sales Modern Trade']) + float(wd_dict['OtherSales Modern Trade'])
                        json_list.append(wd_dict)

                    df = pd.DataFrame.from_dict(list(json_list))
                    df.to_csv(response, index=False)
                    return response
                    # return Response({"message":"Invalid Transaction Type","data":json_list})
                elif town_list or wd_town_id_list:
                    
                    if town_list:
                        wd_town_id_list = Sales_Hierarchy_Master.objects.filter(
                            town_code__in=town_list).values_list('wd_town_id', flat=True)
                        Salesobj = SalesData.objects.filter( town_id__in=wd_town_id_list, sales_date_time__gte=from_date,
                                                            sales_date_time__lte=to_date, brand_category__in=category_list, transaction_type="DAILY").values()
                    else:
                        Salesobj = SalesData.objects.filter( sales_date_time__gte=from_date, sales_date_time__lte=to_date, brand_category__in=category_list, transaction_type="DAILY").values()
                    if Salesobj:
                        if transaction_type.upper() == "SALES_DATA_WD":
                            response=HttpResponse(content_type='text/csv')
                            response['Content-Disposition']='attachment; filename="sec_sales_data_wd.csv"'
                            sales_data_wd_serializer=SalesDataSerialize_WD(
                                Salesobj, many=True).data
                            print(sales_data_wd_serializer,
                                  "=========bu========")
                            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
                            df=pd.DataFrame.from_dict(
                                list(sales_data_wd_serializer))
                            rename_dict={'region': 'Region Name', 'town_name': 'Town Name', 'wd_name': 'WD Name',
                                    'wd_id': 'Wd Id', 'brand_category': 'Category', 'sku_code': 'Brand Code', 'sku_short_name': 'Brandshort Name', 'sales_date_time': 'Secsale Date',
                            'local_sales_retail': 'Local Sales Retail', 'local_sales_dealer': 'Local Sales Dealer', 'local_sales_modern_trade': 'Local Sales Modern Trade', 'local_sales_hawker': 'Local Sales Hawker',
                            'outstation_sales_reatil': 'Outstation Sales Retail', 'outstation_sales_dealer': 'Outstation Sales Dealer', 'outstation_sales_modern_trade': 'Outstation Sales Modern Trade', 'outstation_sales_hawker': 'Outstation Sales Hawker',
                            'other_sales_retail': 'Other Sales Retail', 'other_sales_dealer': 'Other Sales Dealer', 'other_sales_modern_trade': 'Other Sales Modern Trade',
                            'total_retail': 'Total Retail', 'toatal_Dealer': 'Total Dealer', 'total_Modern_Trade_Sales': 'Total Modern Trade Sales', 'total_Howker': 'Total Hawker',
                            'total_local_sales': 'Total Local', 'total_outstation_sales': 'Total Outstation Sales',
                            # 'total_other_sales':'Total Other Sales',
                            'grand_total': 'Grand Total',
                            'other_issues_damage': 'Other Issues Damage', 'other_issues_return': 'Other Issues Return', 'other_issues_other': 'Other Issues Other', 'total_issue': 'Total Issue', 'wd_type': 'Tranisition Source'
                            }
                            df.rename(columns=rename_dict, inplace=True)
                            df.to_csv(response, index=False)
                            return response
                        elif transaction_type.upper() == "SALES_DATA":
                            sales_data_serializer=SalesDataSerialize(
                                Salesobj, many=True).data
                            response=HttpResponse(content_type='text/csv')
                            response['Content-Disposition']='attachment; filename="sec_sales_data.csv"'
                            print(sales_data_serializer, "=================")
                            df=pd.DataFrame.from_dict(
                                list(sales_data_serializer))
                            rename_dict={'region': 'Region Name', 'town_name': 'Town Name', 'wd_name': 'WD Name',

                                           'wd_id': 'Wd Id', 'brand_category': 'Category', 'sku_code': 'Brand Code', 'sku_short_name': 'Brandshort Name', 'sales_date_time': 'Secsale Date',
                            'local_sales_retail': 'Local Sales Retail', 'local_sales_dealer': 'Local Sales Dealer', 'local_sales_modern_trade': 'Local Sales Modern Trade', 'local_sales_hawker': 'Local Sales Hawker',
                            'outstation_sales_reatil': 'Outstation Sales Retail', 'outstation_sales_dealer': 'Outstation Sales Dealer', 'outstation_sales_modern_trade': 'Outstation Sales Modern Trade', 'outstation_sales_hawker': 'Outstation Sales Hawker',
                            'other_sales_retail': 'Other Sales Retail', 'other_sales_dealer': 'Other Sales Dealer', 'other_sales_modern_trade': 'Other Sales Modern Trade',
                            'total_retail': 'Total Retail', 'toatal_Dealer': 'Total Dealer', 'total_Modern_Trade_Sales': 'Total Modern Trade Sales', 'total_Howker': 'Total Hawker',
                            'total_local_sales': 'Total Local', 'total_outstation_sales': 'Total Outstation Sales',
                            # 'total_other_sales':'Total Other Sales',
                            'grand_total': 'Grand Total',
                            'other_issues_damage': 'Other Issues Damage', 'other_issues_return': 'Other Issues Return', 'other_issues_other': 'Other Issues Other', 'total_issue': 'Total Issue', 'wd_type': 'Tranisition Source'
                            }
                            df.rename(columns=rename_dict, inplace=True)
                            df.to_csv(response, index=False)
                            # print(type(response),"qqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
                            # print(json.dumps(response),"ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
                            data1=list(response)
                            print(data1[0],"]]]]]]]]]]]]]]]]]]]]]]]]mmmmmmmmmmmm")
                            json_object = {'key':response}
                            # print(json_object,"????????????????????????//")
                            # return JsonResponse(json_object)
                        
                    
                            return JsonResponse(json.dumps(json_object),safe=False)
                            # data = ABC.serialize('json', [response],many=True)
                            # print(type(data),">>>>>>>>>>>>>>>>>>>>>> TYPE")
                            # print(data,"GGGGGGGGGGGGGGGGGG")
                            
                            return HttpResponse(data, content_type="application/json")
                       
                            return response
                        else:
                            return Response({"message": "Invalid Transaction Type", 'status': False})
                    else:
                        return Response({"message": "There is no sales record.", 'status': False})
                else:
                        return Response({"message": "You have no WD User.", 'status': True})

            # # elif request.user.user_type == "WD":
            # #     Salesobj = SalesData.objects.filter(wd_id = request.user.user_id ,sales_date_time__gte=from_date,sales_date_time__lte=to_date,brand_category__in=category_list,transaction_type = "DAILY").values()
            # #     if Salesobj:
            # #         if transaction_type.upper() == "MTD_REPORT":
            # #             if category_list:
            # #                 category_list = category_list
            # #             else:
            # #                 category_list = None
            # #             wd_idesq = request.user.user_id
            # #             response = HttpResponse(content_type='text/csv')
            # #             response['Content-Disposition'] = 'attachment; filename="MTD_REPORT_BRANCH USER.csv"'
            # #             if len(category_list)==1:
            # #                 query="""SELECT wd_name,wd_id,brand_category,sku_id,sku_code,sku_short_name,SUM(local_sales_retail),SUM( local_sales_dealer),
            # #                 SUM(local_sales_modern_trade),SUM(local_sales_hawker),SUM(total_local_sales),SUM( outstation_sales_reatil),
            # #                 SUM(outstation_sales_dealer),SUM( outstation_sales_modern_trade) ,SUM(outstation_sales_hawker),
            # #                 SUM( total_outstation_sales) ,SUM(other_sales_retail),SUM( other_sales_dealer) ,SUM(other_sales_modern_trade),
            # #                 SUM( total_other_sales),SUM(other_issues_damage),SUM( other_issues_return),SUM(other_issues_other),
            # #                 SUM( total_issue),SUM(grand_total)  FROM transaction_salesdata WHERE
            # #                 sales_date_time >= '"""+from_date+"""' AND sales_date_time <= '"""+to_date+"""' AND
            # #                 transaction_type = 'DAILY' AND brand_category = '"""+category_list[0]+"""' AND wd_id = '"""+wd_idesq+"""' GROUP BY wd_id,sku_id;"""
            # #             else:
            # #                 query="""SELECT wd_name,wd_id,brand_category,sku_id,sku_code,sku_short_name,SUM(local_sales_retail),SUM( local_sales_dealer),
            # #                 SUM(local_sales_modern_trade),SUM(local_sales_hawker),SUM(total_local_sales),SUM( outstation_sales_reatil),
            # #                 SUM(outstation_sales_dealer),SUM( outstation_sales_modern_trade) ,SUM(outstation_sales_hawker),
            # #                 SUM( total_outstation_sales) ,SUM(other_sales_retail),SUM( other_sales_dealer) ,SUM(other_sales_modern_trade),
            # #                 SUM( total_other_sales),SUM(other_issues_damage),SUM( other_issues_return),SUM(other_issues_other),
            # #                 SUM( total_issue),SUM(grand_total) FROM transaction_salesdata WHERE
            # #                 sales_date_time >= '"""+from_date+"""' AND sales_date_time <= '"""+to_date+"""' AND
            # #                 transaction_type = 'DAILY' AND brand_category IN """+str(tuple(category_list))+""" AND wd_id = '"""+wd_idesq+"""' GROUP BY wd_id,sku_id;"""
            # #             cursor.execute(query)
            # #             row = cursor.fetchall()
            # #             for i in row:
            # #                 wd_dict={}
            # #                 wd_dict['Wd Name'] = i[0]
            # #                 wd_dict['Wd ID'] = i[1]
            # #                 wd_dict['Category'] = i[2]
            # #                 wd_dict['Sku Id'] = i[3]
            # #                 wd_dict['Brand Code'] = i[4]
            # #                 wd_dict['Brand Short Name'] = i[5]

            # #                 wd_dict['Local Sales Retail'] = i[6]
            # #                 wd_dict['Local Sales Dealer'] = i[7]
            # #                 wd_dict['Local Sales Modern Trade'] = i[8]
            # #                 wd_dict['Local Sales Hawker'] = i[9]

            # #                 wd_dict['Outstation Sales Retail'] = i[11]
            # #                 wd_dict['Outstation Sales Dealer'] = i[12]
            # #                 wd_dict['Outstation Sales Modern Trade'] = i[13]
            # #                 wd_dict['Outstation Sales Hawker'] = i[14]

            # #                 wd_dict['Other Sales Retail'] = i[16]
            # #                 wd_dict['Other Sales Dealer'] = i[17]
            # #                 wd_dict['OtherSales Modern Trade'] = i[18]

            # #                 wd_dict['Total Retail'] = float(wd_dict['Local Sales Retail']) + float(wd_dict['Outstation Sales Retail']) + float(wd_dict['Other Sales Retail'])
            # #                 wd_dict['Total Dealer'] = float(wd_dict['Local Sales Dealer'] ) + float(wd_dict['Outstation Sales Dealer'] ) + float(wd_dict['Other Sales Dealer'])
            # #                 wd_dict['Total Modern Trade'] = float(wd_dict['Local Sales Modern Trade']) + float(wd_dict['Outstation Sales Modern Trade']) + float(+ wd_dict['OtherSales Modern Trade'])
            # #                 wd_dict['Total Hawker'] = float(wd_dict['Local Sales Hawker']) + float(wd_dict['Outstation Sales Hawker'])

            # #                 wd_dict['Total Local'] = i[10]
            # #                 wd_dict['Total Outstation'] = i[15]
            # #                 wd_dict['Grand Total'] = i[24]

            # #                 wd_dict['Other Issues Damage'] = i[20]
            # #                 wd_dict['Other Issues Return'] = i[21]
            # #                 wd_dict['Other Issues Other'] = i[22]
            # #                 wd_dict['Total Issue'] = i[23]
            # #                 # wd_dict['Wd Name'] = i[0]
            # #                 # wd_dict['Wd ID'] = i[1]
            # #                 # wd_dict['Category'] = i[2]
            # #                 # wd_dict['Sku Id'] = i[3]
            # #                 # wd_dict['Sku Code'] = i[4]
            # #                 # wd_dict['Brand Short Name'] = i[5]
            # #                 # wd_dict['Local Sales Retail'] = i[6]
            # #                 # wd_dict['Local Sales Dealer'] = i[7]
            # #                 # wd_dict['Local Sales Modern Trade'] = i[8]
            # #                 # wd_dict['Local Sales Hawker'] = i[9]
            # #                 # wd_dict['Total Local'] = i[10]
            # #                 # wd_dict['Outstation Sales Retail'] = i[11]
            # #                 # wd_dict['Outstation Sales Dealer'] = i[12]
            # #                 # wd_dict['Outstation Sales Modern Trade'] = i[13]
            # #                 # wd_dict['Outstation Sales Hawker'] = i[14]
            # #                 # wd_dict['Total Outstation'] = i[15]
            # #                 # wd_dict['Other Sales Retail'] = i[16]
            # #                 # wd_dict['Other Sales Dealer'] = i[17]
            # #                 # wd_dict['OtherSales Modern Trade'] = i[18]
            # #                 # wd_dict['Total Other'] = i[19]
            # #                 # wd_dict['Other Issues Damage'] = i[20]
            # #                 # wd_dict['Other Issues Return'] = i[21]
            # #                 # wd_dict['Other Issues Other'] = i[22]
            # #                 # wd_dict['Total Issue'] = i[23]
            # #                 # wd_dict['Grand Total'] = i[24]
            # #                 # wd_dict['Total Retail'] = float(wd_dict['Local Sales Retail']) + float(wd_dict['Outstation Sales Retail']) + float(wd_dict['Other Sales Retail'])
            # #                 # wd_dict['Total Dealer'] = float(wd_dict['Local Sales Dealer'] ) + float(wd_dict['Outstation Sales Dealer'] ) + float(wd_dict['Other Sales Dealer'])
            # #                 # wd_dict['Total Hawker'] = float(wd_dict['Local Sales Hawker']) + float(wd_dict['Outstation Sales Hawker'])
            # #                 # wd_dict['Total Modern Trade'] = float(wd_dict['Local Sales Modern Trade']) + float(wd_dict['Outstation Sales Modern Trade']) + float(wd_dict['OtherSales Modern Trade'])
            # #                 json_list.append(wd_dict)

            # #             df = pd.DataFrame.from_dict(list(json_list))
            # #             df.to_csv (response, index = False)
            # #             return response

            # #             # return Response({"message":"Invalid Transaction Type","data":dataframe_list})
            # #         # else:
            # #         #     return Response({"message":"You have no sales record.",'status': True})
            # #         elif Salesobj:
            # #             if transaction_type:
            # #                 wd_sales_data_serializer = WD_SalesDataSerialize(Salesobj, many = True).data
            # #                 response = HttpResponse(content_type='text/csv')
            # #                 response['Content-Disposition'] = 'attachment; filename="wd_sec_sales_data.csv"'
            # #                 df = pd.DataFrame.from_dict(list(wd_sales_data_serializer))
            # #                 rename_dict = {
            # #                     # 'wd_name':'WD Name','wd_id':'Wd Id',
            # #                     'town_name' :'Town Name','wd_name':'WD Name','wd_id':'Wd Id','brand_category':'Category','sku_code':'Brand Code','sku_short_name':'Brand Short Name','sales_date_time':'Secsale Date',
            # #                     'local_sales_retail':'Local Sales Retail','local_sales_dealer':'Local Sales Dealer','local_sales_modern_trade':'Local Sales Modern Trade','local_sales_hawker':'Local Sales Hawker',
            # #                     'outstation_sales_reatil':'Outstation Sales Retail','outstation_sales_dealer':'Outstation Sales Dealer','outstation_sales_modern_trade':'Outstation Sales Modern Trade','outstation_sales_hawker':'Outstation Sales Hawker',
            # #                     'other_sales_retail':'Other Sales Retail','other_sales_dealer':'Other Sales Dealer','other_sales_modern_trade':'Other Sales Modern Trade',
            # #                     'total_retail':'Total Retail','toatal_Dealer':'Total Dealer','total_Modern_Trade_Sales':'Total Modern Trade Sales','total_Howker':'Total Hawker',
            # #                     'total_local_sales':'Total Local','total_outstation_sales':'Total Outstation Sales',
            # #                     # 'total_other_sales':'Total Other Sales',
            # #                     'grand_total':'Grand Total',
            # #                     'other_issues_damage':'Other Issues Damage','other_issues_return':'Other Issues Return','other_issues_other':'Other Issues Other','total_issue':'Total Issue',
            # #                     'wd_type':'Tranisition Source'
            # #                 }
            # #                 df.rename(columns=rename_dict,inplace=True)
            # #                 df.to_csv (response, index = False)
            # #                 return response
            #     else:
            #         return Response({"message":"You have no sales record.", "data":Salesobj,'status': True})
            else:
                return Response({"message": "Invalid User Type.", 'status': False})
        # except Exception as e:
        #     error=getattr(e, 'message', repr(e))
        #     logger.error(error)
        #     context={'status': False,
        #         'message': 'Something Went Wrong', 'error': error}
        #     return Response(context, status=status.HTTP_200_OK)
