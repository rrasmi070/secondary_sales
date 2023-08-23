from branch_user.utills import adminapidaily, adminapiweekly, appendSFA, base64_decode, branch_user_weekly, editable_status, sale_data_obj_with_sequence, sku_remark, top_sku_sales
from itertools import chain
from branch_user.utills import adminapidaily, adminapiweekly, branch_user_weekly, sku_remark, top_sku_sales
from wd import utils
import base64
from wd.serializers import *
from dateutil.relativedelta import relativedelta
import calendar
from cgi import print_arguments
from collections import Counter
import collections
from math import trunc
from tokenize import String
from django.core import mail
from django.db.models.aggregates import Count
from django.http import request
from django.shortcuts import render
from rest_framework.serializers import Serializer
from base.serializers import *
from base.models import *
from wd.helper import week_sele_before_date
from .serializers import *
from master.serializers import *
from master.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from django.conf import settings
import datetime
from datetime import date, datetime, timedelta
from datetime import datetime
import datetime
import datetime
import dateutil.relativedelta
from django.db.models import Sum
from rest_framework import viewsets
from base.paginations import *
from rest_framework import generics, permissions, status, views, filters
import logging
from django.db.models import Q
from dateutil.parser import parse
from datetime import date
from django.http import request
logger = logging.getLogger(__name__)
import re
import json
from itertools import chain

from secondary_sales.settings import my_eng
from master.email_sub import failed_list,cc_list,success_email_list, html_message_weekly
from django.core.mail import EmailMessage

def current_week():
    # sale_date
    now_dt = datetime.datetime.now()
    week_1st_gng = [datetime.datetime(now_dt.date().year, now_dt.date().month, 1).date(
    ), datetime.datetime(now_dt.date().year, now_dt.date().month, 7).date()]
    week_2nd_gng = [datetime.datetime(now_dt.date().year, now_dt.date().month, 8).date(
    ), datetime.datetime(now_dt.date().year, now_dt.date().month, 14).date()]
    week_3rd_gng = [datetime.datetime(now_dt.date().year, now_dt.date().month, 15).date(
    ), datetime.datetime(now_dt.date().year, now_dt.date().month, 21).date()]
    last_date_month = datetime.datetime(now_dt.date().year, now_dt.date(
    ).month, calendar.monthrange(now_dt.date().year, now_dt.date().month)[1]).date()
    week_4th = [datetime.datetime(
        now_dt.date().year, now_dt.date().month, 22), last_date_month]
    print(week_4th[0] - relativedelta(months=1), "====>>===",
          now_dt.date().today().replace(day=1) - datetime.timedelta(days=1))
    week_4_weekly_gng = [week_4th[0] - relativedelta(
        months=1), now_dt.date().today().replace(day=1) - datetime.timedelta(days=1)]

    # current week as per reng====
    week_1st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 8).date(
    ), datetime.datetime(now_dt.date().year, now_dt.date().month, 10).date()]
    week_2st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 15).date(
    ), datetime.datetime(now_dt.date().year, now_dt.date().month, 17).date()]
    week_3st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 22).date(
    ), datetime.datetime(now_dt.date().year, now_dt.date().month, 24).date()]
    last_date_month = datetime.datetime(now_dt.date().year, now_dt.date(
    ).month, calendar.monthrange(now_dt.date().year, now_dt.date().month)[1]).date()
    week_4st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 1).date(
    ), datetime.datetime(now_dt.date().year, now_dt.date().month, 3).date()]

    # dddd = datetime.datetime.combine(week_1st[0], till_date.time())

    if week_1st_gng[0] <= now_dt.date() >= week_1st_gng[1]:
        week_reng = week_1st
        print("hhhh1")
        weekly = "Week1"
        week_rng_val = week_1st_gng
    elif week_2nd_gng[0] <= now_dt.date() >= week_2nd_gng[1]:
        week_reng = week_2st
        print("hhhh1")
        weekly = "Week2"
        week_rng_val = week_1st_gng
    elif week_3rd_gng[0] <= now_dt.date() >= week_3rd_gng[1]:
        week_reng = week_3st
        print("hhhh1")
        weekly = "Week3"
        week_rng_val = week_1st_gng
    elif week_4th[0] <= now_dt.date() >= week_4th[1]:
        week_reng = week_4st
        print("hhhh1")
        weekly = "Week4"
        week_rng_val = week_1st_gng
    return week_reng, weekly, week_rng_val


#>>>>>>>>>>>>>>>>>>>???????????  ADMIN
# def adminapiweekly(wd_id, category, town_id, date_f, week_num, month, year, week):
#     today_date = datetime.datetime.now()
#     # print(date_f)
#     last_date = date_f
#     # breakpoint()
#     week_details = week_sele_before_date("BRANCH USER")
    

#     if week_num is not None:  # this will exicute for BRANCH_USER Weekly data
#         if wd_id:
#             wo_4th = [1, 2, 3]
#             # print(wd_id,"======")
#             # if x in wo_4th:
#             #     week_sale_date = today_date.date() - relativedelta(months=1)
#             # else:
#             #     week_sale_date = today_date.date()
#             wd_town_id_list = Sales_Hierarchy_Master.objects.filter(
#                 wd_id=wd_id).values_list('wd_town_id', flat=True)
            
#             sku_id_list = WdSkuCatagory.objects.filter(
#                 wd_town_id__in=wd_town_id_list).values_list('sku_id', flat=True)
#             topsqu_list = SalesData.objects.filter(sku_id__in=sku_id_list, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, sales_date_time__gte=last_date, transaction_type=week_num).values_list(
#                 'sku_id', flat=True).annotate(sku_totalsale=Sum('grand_total')).order_by('-sku_totalsale')
#             sku_list_top = []
#             sku_id_list3 = list(set(list(sku_id_list)))
#             for i in topsqu_list:
#                 if i in sku_id_list3:
#                     sku_list_top.append(i)
#                     sku_id_list3.remove(i)
#             sku_lists = sku_list_top + sku_id_list3
#             list1 = []
#             for k in sku_lists:
#                 sku = SKU_Master_Product.objects.filter(
#                     sku_id=k, effective_from__lte=date_f, category_code=category).last()
#                 if sku:
#                     list1.append(sku)
#             sku_serializars = SKU_Master_ProductsSerializer(
#                 list1, many=True)
#             sku_serializars_v = sku_serializars.data
#             for i in sku_serializars_v:
#                 sku_id = i.get('sku_id')
#                 if category:
#                     Salesobj = SalesData.objects.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time=week_details[
#                                                         2][1], brand_category=category, transaction_type=week_details[1], town_code__in=town_id).values()
#                 else:
#                     Salesobj = SalesData.objects.filter(
#                         sku_id=sku_id, sales_date_time=week_details[2][1], wd_id=wd_id, town_id__in=wd_town_id_list, transaction_type=week_details[1], town_code__in=town_id).values()
#                 if Salesobj:
#                     i["SalesData"] = Salesobj

#                 else:
#                     i["SalesData"] = [{}]
#         return sku_serializars_v
#         # return Response({"message": "Successful", "status_data": "[status_data_val]", "remarks":" Sku_Serializer", "data": sku_serializars_v, 'status': True})

# def adminapidaily(wd_id,category,town_id,date_f):
#     week_details = week_sele_before_date("BRANCH USER")
    
#     today_date = datetime.datetime.now()
    
#     last_date = today_date + \
#                 dateutil.relativedelta.relativedelta(months=-6)

#     # print("hello")
#     wd_town_id_list = Sales_Hierarchy_Master.objects.filter(
#         wd_id=wd_id).values_list('wd_town_id', flat=True)
#     sku_id_list = WdSkuCatagory.objects.filter(
#         wd_town_id__in=wd_town_id_list).values_list('sku_id', flat=True)
#     topsqu_list = SalesData.objects.filter(sku_id__in=sku_id_list, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, sales_date_time__gte=last_date, transaction_type="DAILY").values_list(
#         'sku_id', flat=True).annotate(sku_totalsale=Sum('grand_total')).order_by('-sku_totalsale')
#     sku_list_top = []
#     freeze_obj = None
#     sku_id_list3 = list(set(list(sku_id_list)))
#     for i in topsqu_list:
#         if i in sku_id_list3:
#             sku_list_top.append(i)
#             sku_id_list3.remove(i)
#     sku_lists = sku_list_top + sku_id_list3
# #
#     list1 = []
#     for k in sku_lists:
#         sku = SKU_Master_Product.objects.filter(
#             sku_id=k, effective_from__lte=date_f, category_code=category).last()
#         if sku:
#             list1.append(sku)
#     sku_serializars = SKU_Master_ProductsSerializer(
#         list1, many=True)
#     sku_serializars_v = sku_serializars.data
#     for i in sku_serializars_v:
#         sku_id = i.get('sku_id')
#         if category:

#             # if  Salesobj :
#             #     SalesData.objects.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list,
#             #                                         brand_category=category, sales_date_time=date_f, transaction_type="DAILY", town_code__in=town_id).values()
#             # else:
#             #     Salesobj = SalesData.objects.filter(
#             #         sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time=date_f, transaction_type="DAILY", town_code__in=town_id).values()
#             #     sku_serializars_v=Salesobj
        
        
#             if category:
#                 Salesobj = SalesData.objects.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time = date_f, brand_category=category, transaction_type='DAILY', town_code__in=town_id).values()
#             else:
#                 Salesobj = SalesData.objects.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list,
#                                                     sales_date_time=date_f, transaction_type="DAILY", town_code__in=town_id).values()

#             if Salesobj:
#                 i["SalesData"] = Salesobj

#             else:
#                 i["SalesData"] = [{}]

               
#     return  sku_serializars_v
#     # return Response({"message": "Successful", "status_data": "[status_data_val]", "remarks":" Sku_Serializer", "data": sku_serializars_v, 'status': True})




class Towm_wise_wd(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            towns = request.GET.get("towns")
            request_type = request.GET.get("request_type")
            base64_bytes = towns.encode("ascii")
            sample_string_bytes = base64.b64decode(base64_bytes)
            sample_string = sample_string_bytes.decode("ascii")
            towns = sample_string.split("_")[0]
            # print(towns)
            town_li = towns.split(',')
            if request_type.upper() =="REPORT":
                user_list = User.objects.filter(locationcode=request.user.locationcode,status = True).values_list("user_id", flat=True)
                wd_list_data = Sales_Hierarchy_Master.objects.filter(wd_id__in=user_list, town_code__in=town_li, status = True).values_list("wd_id", flat=True)
            else:
                user_list = User.objects.filter(locationcode=request.user.locationcode,status = True).values_list("user_id", flat=True)
                wd_list_data = Sales_Hierarchy_Master.objects.filter(wd_id__in=user_list, town_code__in=town_li,status = True).values_list("wd_id", flat=True)
            if wd_list_data:
                # wd_data = User.objects.filter(user_id__in=wd_list_data).values("first_name", "user_id")
                wd_data = User.objects.filter(user_id__in=wd_list_data)
                wdMasterInstance=WDmaster.objects.filter(wd_ids=wd_data.last().user_id)
                wd_data = wd_data.values("first_name", "user_id")
                wd_type=wdMasterInstance.last().wd_type
                wd_data = list(wd_data)
                wd_data=appendSFA(wd_data,wd_type)
                
            else:
                return Response({"status": False, 'message': 'No WD Found.'})
            # serializer_class = Usrer_serializer_town(wd_data).data
            if wd_data:
                return Response({"status": True, 'message': 'Success', "data": wd_data})
            else:
                return Response({"status": False, 'message': 'No WD Found.'})
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)



class Towns_of_WD(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(request.user.locationcode)
        try:
            if request.user.user_type == "BRANCH USER":
                request_type = request.GET.get('request_type', None)
                # wd_id_list = Sales_Hierarchy_Master.objects.filter(region_code = request.user.locationcode).values('town_code','town').distinct()
                if request_type and request_type.upper() == "REPORT":
                    print("--------------------request_type")
                    user_id_li = User.objects.filter(locationcode=request.user.locationcode).exclude(
                        user_type="BRANCH USER").values_list("user_id", flat=True)
                    wd_id_list = WDmaster.objects.filter(wd_ids__in=user_id_li).values('wd_postal_code').distinct()
                else:
                    print("----------none----------request_type-------------------",request.user.locationcode)
                    user_id_li = User.objects.filter(locationcode=request.user.locationcode, status = True).exclude(
                        user_type="BRANCH USER").values_list("user_id", flat=True)
                    wd_id_list = WDmaster.objects.filter(wd_ids__in=user_id_li, status = True).values('wd_postal_code').distinct()
                    print(user_id_li,"-------------user_id_li")
                # wd_id_list = WDmaster.objects.filter(
                #     wd_ids__in=user_id_li).values('wd_postal_code').distinct()

                if wd_id_list:
                    print("-----")
                    serializer = WDmaster_wd_towns(wd_id_list, many=True)
                    wd_id_list = serializer.data
                    # print(wd_id_list)
                    return Response({"status": True, 'message': 'Success', "data": wd_id_list})
                else:
                    return Response({"status": False, 'message': 'No Towns you have'})
            elif request.user.user_type == "WD":
                wd_id_list = WDmaster.objects.filter(
                    wd_ids=request.user.user_id)
                if wd_id_list:
                    serializer = WDmaster_wd_town(wd_id_list, many=True)
                    wd_id_list = serializer.data
                    # print(wd_id_list)
                    return Response({"status": True, 'message': 'Success', "data": wd_id_list})
                else:
                    return Response({"status": False, 'message': 'No Towns you have'})
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)


class Skulist(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            category_data = WdSkuCatagory.objects.filter(
                status=True).distinct()
            serializer = WdSkuCatagorySerializer(category_data, many=True).data
            return Response(serializer)
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)


class GetWD_id_name(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            if request.user.user_type == "BRANCH USER":
                print()
                data = User.objects.filter(locationcode=request.user.locationcode).values(
                ).exclude(user_type='BRANCH USER')
                return Response({'message': 'success', 'd': data.values_list('user_id', flat=True), "dat": list(set(data.values_list('user_id', flat=True)))})
            else:
                data = User.objects.filter(
                    user_id=request.user.user_id).values()
                serialize = UserSerializeID_Name(data, many=True)
                return Response({"data": serialize.data, "status": True, "massage": "Request successfull"})
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,
                       'message': 'Something Went Wrong', 'error': error}
            return Response(context, status=status.HTTP_200_OK)

# from django_filters.rest_framework import DjangoFilterBackend


class GetWDList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = GpiPagination
    # serializer_class = UserSerialize_getWD
    serializer_class = UserSerialize_getWDMaster
    def get_queryset(self):
        #try:
            search_wd = self.request.GET.get('search')
           
            locationcode=self.request.GET.get('locationcode')

            
            if self.request.user.user_type in ["ADMIN","HO"]:
                print('wd_list','jjjjjjjjjjjjjjjjjjjjj', datetime.datetime.now())
                if self.request.user.user_type in ["ADMIN","HO"] and search_wd:
                      
                    wd_list = User.objects.filter(locationcode=locationcode).values_list(
                        'user_id', flat=True).exclude(user_type='BRANCH USER')       
                                       
                    # wd_list = User.objects.all().values_list(
                    #     'user_id', flat=True).exclude(user_type='ADMIN' and  "BRANCH USER" and "HO")
                   
                    # source_list = WDmaster.objects.filter(Q(wd_type__icontains=search_wd) | Q(wd_state__icontains=search_wd) | Q(
                    #     wd_city__icontains=search_wd) | Q(wd_ids__in=wd_list)).values_list('wd_ids', flat=True)
                    # source_list = WDmaster.objects.filter(Q(wd_type__icontains=search_wd) |Q(wd_postal_code__icontains = search_wd) | Q(wd_state__icontains=search_wd) | Q(
                    #     wd_city__icontains=search_wd)).values_list('wd_ids', flat = True)
                    wd_id_li1 = Sales_Hierarchy_Master.objects.filter(Q(wd_id__icontains = search_wd)).values_list('wd_id', flat = True)
                    wd_id_li2 = Sales_Hierarchy_Master.objects.filter(Q(town__icontains = search_wd)).values_list('wd_id', flat = True)
                    wd_id_li3 = Sales_Hierarchy_Master.objects.filter(Q(town_code__icontains = search_wd)).values_list('wd_id', flat = True)
                    source_list_id = list(chain(wd_id_li1,wd_id_li2,wd_id_li3))
                    # source_list_id = Sales_Hierarchy_Master.objects.filter(Q(wd_id__in = search_wd)|Q(town__icontains = search_wd)|Q(town_code__icontains = search_wd)).values_list('wd_id', flat = True)
                    # exclude_list = set(source_list_id).issubset(set(wd_list))
                    # exclude_list = source_list_id if exclude_list else []
                    print(source_list_id,"===>>>>>>>>>>>>>>>>>>>>>===","exclude_list")
                    source_list = WDmaster.objects.filter(wd_ids__in=source_list_id)
                    return source_list
                    data1 = User.objects.filter((Q(user_id__icontains=search_wd) | Q(first_name__icontains=search_wd))).values(
                    ).exclude(user_type='BRANCH USER').values_list('user_id', flat=True)
                    data = User.objects.filter(Q(user_id__in=data1) | Q(
                        user_id__in=source_list)).values()

                    if data:
                        return data
                    else:
                        wd_list = User.objects.filter(locationcode=locationcode).values_list(
                        'user_id', flat=True).exclude(user_type='BRANCH USER')       
                        # wd_list = User.objects.all().values_list(
                        #     'user_id', flat=True).exclude(user_type='BRANCH USER')
                        source_list = WDmaster.objects.filter(Q(wd_type__icontains=search_wd) | Q(wd_state__icontains=search_wd) | Q(
                            wd_city__icontains=search_wd), wd_ids__in=wd_list).values_list('wd_ids', flat=True)
                        data = User.objects.filter(
                            user_id__in=source_list).values()

                        return data
                else:
                    print("=============================>")
                    data = User.objects.all().values_list(
                        'user_id', flat=True).exclude(user_type='BRANCH USER')
                    source_list = WDmaster.objects.filter(wd_ids__in=data)
                    return source_list            
                    
                    
                    return data
                    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    # wd_list = User.objects.filter(locationcode=locationcode).values_list(
                    #     'user_id', flat=True).exclude(user_type='BRANCH USER')                  
                    
                    # source_list = WDmaster.objects.filter(Q(wd_type__icontains=search_wd) | Q(wd_state__icontains=search_wd) | Q(
                    #     wd_city__icontains=search_wd), wd_ids__in=wd_list).values_list('wd_ids', flat=True)
                    # data1 = User.objects.filter((Q(user_id__icontains=search_wd) | Q(first_name__icontains=search_wd)), locationcode=self.request.user.locationcode).values(
                    # ).exclude(user_type='BRANCH USER').values_list('user_id', flat=True)
                    # data = User.objects.filter(Q(user_id__in=data1) | Q(
                    #     user_id__in=source_list)).values()

                    # if data:
                    #     return data
                    # else:
                    #     wd_list = User.objects.filter(locationcode=locationcode).values_list(
                    #         'user_id', flat=True).exclude(user_type='BRANCH USER' and 'ADMIN')
                    #     source_list = WDmaster.objects.filter(Q(wd_type__icontains=search_wd) | Q(wd_state__icontains=search_wd) | Q(
                    #         wd_city__icontains=search_wd), wd_ids__in=wd_list).values_list('wd_ids', flat=True)
                    #     data = User.objects.filter(
                    #         user_id__in=source_list).values()

                    #     return data
                    
                
            elif self.request.user.user_type == "BRANCH USER" and search_wd:
                wd_list = User.objects.filter(locationcode=self.request.user.locationcode).values_list(
                    'user_id', flat=True).exclude(user_type='BRANCH USER')                  
                wd_id_li1 = Sales_Hierarchy_Master.objects.filter(Q(wd_id__icontains = search_wd)).values_list('wd_id', flat = True)
                wd_id_li2 = Sales_Hierarchy_Master.objects.filter(Q(town__icontains = search_wd)).values_list('wd_id', flat = True)
                wd_id_li3 = Sales_Hierarchy_Master.objects.filter(Q(town_code__icontains = search_wd)).values_list('wd_id', flat = True)
                source_list_id = list(chain([wd_id_li1,wd_id_li2,wd_id_li3]))
                exclude_list = set(source_list_id).issubset(set(wd_list))
                exclude_list = source_list_id if exclude_list else []
                source_list = WDmaster.objects.filter(wd_ids__in=exclude_list)
                return source_list
                
                source_list = WDmaster.objects.filter(Q(wd_type__icontains=search_wd) | Q(wd_state__icontains=search_wd) | Q(
                    wd_city__icontains=search_wd), wd_ids__in=wd_list).values_list('wd_ids', flat=True)
                data1 = User.objects.filter((Q(user_id__icontains=search_wd) | Q(first_name__icontains=search_wd)), locationcode=self.request.user.locationcode).values(
                ).exclude(user_type='BRANCH USER').values_list('user_id', flat=True)
                data = User.objects.filter(Q(user_id__in=data1) | Q(
                    user_id__in=source_list)).values()

                if data:
                    return data
                else:
                    wd_list = User.objects.filter(locationcode=self.request.user.locationcode).values_list(
                        'user_id', flat=True).exclude(user_type='BRANCH USER')
                    source_list = WDmaster.objects.filter(Q(wd_type__icontains=search_wd) | Q(wd_state__icontains=search_wd) | Q(
                        wd_city__icontains=search_wd), wd_ids__in=wd_list).values_list('wd_ids', flat=True)
                    data = User.objects.filter(
                        user_id__in=source_list).values()

                    return data
                
            
            
            
            # else:
            #     data = User.objects.filter(
            #         user_id=self.request.user.user_id).values()
            #     return data
                
                
            else:
                if self.request.user.user_type == "BRANCH USER":
                    data = User.objects.filter(locationcode=self.request.user.locationcode).values_list('user_id', flat = True).exclude(user_type='BRANCH USER')
                    source_list = WDmaster.objects.filter(wd_ids__in=data)
                    return source_list
                
                elif self.request.user.user_type == "ADMIN":
                    data = User.objects.filter(locationcode=locationcode).values(
                    ).exclude(user_type='BRANCH USER')
                    # data = User.objects.all().values(
                    # ).exclude(user_type='BRANCH USER')
                    return data
                
                    
            #     else:
            #         data = User.objects.filter(
            #             user_id=self.request.user.user_id).values()
            #         return data
                
                
               
        # except Exception as e:
        #     error = getattr(e, 'message', repr(e))
        #     logger.error(error)
        #     context = {'status': False,
        #                'message': 'Something Went Wrong', 'error': error}
        #     return Response(context, status=status.HTTP_200_OK)


class SalesSkulist(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            userid = User.objects.get(email=request.user)
            print(userid.username)
            data = SalesData.objects.filter(wd_id=userid.username)
            serializer = SalesDataSerializers(data, many=True)
            return Response(serializer.data)
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,
                       'message': 'Something Went Wrong', 'error': error}
            return Response(context, status=status.HTTP_200_OK)


class LockUnlock_user(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        user_name = request.data.get('username', None)
        lock_unlock = request.data.get('lock_unlock', None)

        base64_bytes = user_name.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        user_name = sample_string.split("_")[0]
        try:
            if (user_name is not None) and (lock_unlock is not None):
                if lock_unlock == True:
                    da = User.objects.filter(user_id=user_name).update(
                        lock_unlock=lock_unlock)
                    dict = {'massage': 'User Unlocked .', 'status': True}
                    return Response(dict, status=status.HTTP_200_OK)
                else:
                    da = User.objects.filter(user_id=user_name).update(
                        lock_unlock=lock_unlock)
                    dict = {'massage': 'User Locked .', 'status': True}
                    return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)

# archive 6 month before salesdata =========================


class Schedule_Archcrive(viewsets.ModelViewSet):

    def get_queryset(self):
        now = datetime.datetime.now()
        print(now.time())
        # if now.time() ==
        try:
            till_date = datetime.datetime(2009, 10, 5, 14, 00, 00)
            less = datetime.datetime(2009, 10, 5, 15, 00, 00)
            print("====hiii arch==================", "till_date")
            print(till_date.time(), now.time(),
                  less.time(), "less======00000000000000")
            if till_date.time() < now.time() < less.time():
                before_6mth = now + \
                    dateutil.relativedelta.relativedelta(months=-6)
                print(before_6mth, "======", before_6mth.date())
                arch_data = SalesData.objects.filter(
                    sales_date_time__lte=before_6mth).values()
                print(arch_data.count(), "=====arch_data======")
                dict = []
                transaction_history = {}
                if arch_data:
                    for i in arch_data:
                        i['archived_date'] = datetime.datetime.now()
                        dict.append(i)

                    for data in dict:
                        serializer = Archived_SalesData_Serializer(data=data)
                        if serializer.is_valid():
                            # pass
                            serializer.save()
                            arch_data = SalesData.objects.filter(
                                id=data['id']).delete()
                transact_his = Integration_log_summary.objects.filter(
                    sale_date=now.date(), tranisition_source="SURYA_API")
                if transact_his is not None:
                    transaction_history['total_distributer_sale'] = arch_data.count(
                    )
                    # transaction_history.pop('created_date')
                    transaction_history['last_updated_date'] = datetime.datetime.now(
                    )
                    serializer_class = Integration_log_summarySerializers(
                        transact_his, data=transaction_history, many=True)
                    if serializer_class.is_valid():
                        serializer_class.save()
                else:
                    transaction_history['total_distributer_sale'] = arch_data.count(
                    )
                    transaction_history['tranisition_source'] = "archrive_sales"
                    transaction_history['created_date'] = datetime.datetime.now(
                    )
                    serializer_class = Integration_log_summarySerializers(
                        data=transaction_history, many=True)
                    if serializer_class.is_valid():
                        serializer_class.save()
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)


class Auto_freez(viewsets.ModelViewSet):
    serializer_class = SalesDataSerializer

    def get_queryset(self):
        try:
            date_list = [11, 18, 25, 4]
            now_dt = datetime.datetime.now()
            now_day = str(now_dt.date())
            splited = now_day.split('-')
            print(splited[2], "======")
            
        #     # if from_date.time() < now.time() < till_date.time():

            # now_dt = parse("2022-06-05 15:29:09")
            week_1st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 1).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 7).date()]
            week_2nd = [datetime.datetime(now_dt.date().year, now_dt.date().month, 8).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 14).date()]
            week_3rd = [datetime.datetime(now_dt.date().year, now_dt.date().month, 15).date(),datetime.datetime(now_dt.date().year, now_dt.date().month, 21).date()]
            last_date_month = datetime.datetime(now_dt.date().year, now_dt.date().month, calendar.monthrange(now_dt.date().year,now_dt.date().month)[1]).date()
            # week_4th = [datetime.datetime(now_dt.date().year, now_dt.date().month, 22),last_date_month]
            previus_day = now_dt.replace(day=1) - datetime.timedelta(days=1)
            last_date_month = datetime.datetime(previus_day.date().year, previus_day.date().month, calendar.monthrange(previus_day.date().year,previus_day.date().month)[1]).date()
            week_4th = [datetime.datetime(previus_day.date().year, previus_day.date().month, 22),last_date_month]
            print("Sorry................",week_4th)
            if int(splited[2]) in date_list:
                if int(splited[2]) == 11:
                    data = SalesData.objects.filter(sales_date_time__gte = week_1st[0],sales_date_time__lte = week_1st[1]).update(freeze_status = True)
                    return data
                elif int(splited[2]) == 18:
                    data = SalesData.objects.filter(sales_date_time__gte = week_2nd[0],sales_date_time__lte = week_2nd[1]).update(freeze_status = True)
                    return data
                elif int(splited[2]) == 25:
                    data = SalesData.objects.filter(sales_date_time__gte = week_3rd[0],sales_date_time__lte = week_3rd[1]).update(freeze_status = True)
                    return data
                elif int(splited[2]) == 4:
                    data = SalesData.objects.filter(sales_date_time__gte = week_4th[0],sales_date_time__lte = week_4th[1]).update(freeze_status = True)
                    return data
                else:
                    print("Sorry................")

        
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)


# from wd.utils import now_date


class Gets(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # try:
            
            # print("--------hiiii-------")
            wd_id = request.GET.get('wd_id', None)
            

            base64_bytes = wd_id.encode("ascii")
            sample_string_bytes = base64.b64decode(base64_bytes)
            sample_string = sample_string_bytes.decode("ascii")
            wd_id = sample_string.split("_")[0]
            # print(wd_id)
            
            
            town_id = request.GET.get('town_id', None)
            base64_bytes = town_id.encode("ascii")
            sample_string_bytes = base64.b64decode(base64_bytes)
            sample_string = sample_string_bytes.decode("ascii")
            town_id = sample_string.split("_")[0]
            town_id = [town_id,str(town_id)[1:],"0"+str(town_id)]
            # print(town_id,"===================")
            # breakpoint()

            category = request.GET.get('category', None)
            date_f = str(request.GET.get('date',  datetime.datetime.now().date()))
            
            
            # print("$%%%%%%%%%%%%%%%%%%%%%$$$$$$$$$$$$$$$",wd_id,town_id,category,date_f)

            week_num = request.GET.get('weekly', None)

            user_type = request.user.user_type
            # print(utils.now_date, "==========now_date=======")
            today_date = datetime.datetime.now()
            # today_date = utils.now_date
            last_date = today_date + \
                dateutil.relativedelta.relativedelta(months=-6)

            till_date = datetime.datetime(2009, 10, 5, 14, 59, 59)
            till_date.time()
            Sku_Serializer = []
            status_data = []
            status_data_val = {}
            if date_f:
                # frontend date str conv. to date format
                get_date = datetime.datetime.strptime(
                    date_f, "%Y-%m-%d").date()
                comb_d_t = datetime.datetime.combine(today_date.date(
                ), till_date.time())-timedelta(days=1)  # minus 1 day from current date
            # else:
            #     None
            # day_list=[7,8,14,15,21,22,28,29,30,31,1]
            day_list = [7, 8, 10, 11, 21, 22, 28, 29, 30, 31, 1]

            a = str(today_date.date())
            x = int(str(today_date.date()).split('-')[2])
            lis = [1, 2, 3]

            # set weekly================
            last_date_month = datetime.datetime(today_date.date().year, today_date.date(
            ).month, calendar.monthrange(today_date.date().year, today_date.date().month)[1]).date()
            week_4th = [datetime.datetime(
                today_date.date().year, today_date.date().month, 22).date(), last_date_month]

            week_1st_gng = [datetime.datetime(today_date.date().year, today_date.date().month, 1).date(
            ), datetime.datetime(today_date.date().year, today_date.date().month, 7).date()]
            week_2nd_gng = [datetime.datetime(today_date.date().year, today_date.date().month, 8).date(
            ), datetime.datetime(today_date.date().year, today_date.date().month, 14).date()]
            week_3rd_gng = [datetime.datetime(today_date.date().year, today_date.date().month, 15).date(
            ), datetime.datetime(today_date.date().year, today_date.date().month, 21).date()]
            last_date_month = datetime.datetime(today_date.date().year, today_date.date(
            ).month, calendar.monthrange(today_date.date().year, today_date.date().month)[1]).date()
            # week_4th = [datetime.datetime(today_date.date().year, int(today_date.date().month)-1, 22), week_1st_gng[0] - datetime.timedelta(days=1)]
            week_4th = [datetime.datetime(
                today_date.date().year, today_date.date().month, 22), last_date_month]
            if x in lis and week_4th[0].date() <= get_date <= week_4th[1]:
                # print("hiiii4")
                week_rng = week_4th
            elif week_2nd_gng[0] <= get_date <= week_2nd_gng[1]:
                # print("hiiii2","=======",get_date)
                week_rng = week_2nd_gng
            elif week_3rd_gng[0] <= get_date <= week_3rd_gng[1]:
                # print("hiiii3")
                week_rng = week_4th
            elif week_1st_gng[0] <= get_date <= week_1st_gng[1]:
                # print("hiiii")
                week_rng = week_1st_gng
            else:
                week_rng = None
            # print(week_4th,"====",x,"=====",week_rng)
            # print(week_4th[0].date() ,">= ",get_date ,"<=",week_4th[1])
            week_details = week_sele_before_date(request.user.user_type)
            # print(date_f,"===============================date_f================",get_date < week_details[2][1])
            # print(week_details,"==================>>>>>>>>>>>>", request.user.user_type)
            # breakpoint()
            # return Response({"okk":"======"})
            global_freeze = ''
            list1 = [1, 2, 3, 4, 5, 6, 7]
            list2 = [8, 9, 10, 11, 12, 13, 14]
            list3 = [15, 16, 17, 18, 19, 20, 21]
            list4 = [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 1, 2]
            li = [1, 2]

            StartDate = date_f
            Date = datetime.datetime.strptime(StartDate, "%Y-%m-%d")
            till_date = datetime.datetime(2009, 10, 5, 14, 59, 59)
            till_date.time()
            comb_d_t = datetime.datetime.combine(
                Date.date(), till_date.time())+timedelta(days=1)
            now_current = today_date

            dates = datetime.datetime.strptime(str(date_f), "%Y-%m-%d").date()

            date = dates+datetime.timedelta(days=1)
            combime = datetime.datetime.combine(dates, till_date.time())
            combine_d_t = datetime.datetime.combine(date, till_date.time())
            day_from_date = get_date - datetime.timedelta(days=2)
            beafore_2day = today_date - datetime.timedelta(days=2)

            day_from_date = get_date
            beafore_2day = today_date - datetime.timedelta(days=2)

            not_sales_unfreeze = ""
            not_sales_unfreeze1 = ''
            #>>>> ADMIN section >>>>>> 
            if user_type in ["ADMIN" , "HO"]:
                print(request.user.user_type,"==========================type")
                status_data_val={'freeze_status': True, 'update_status': False, 'lock_status': request.user.lock_unlock}
                if week_num:
                    sku_serializars_v = adminapiweekly(wd_id,category,town_id,date_f,week_num) 
                    
                    
                    return Response({"message": "Successful", "status_data": [status_data_val], "remarks": Sku_Serializer, "data": sku_serializars_v, 'status': True})
                else:
                    sku_serializars_v = adminapidaily(wd_id,category,town_id,date_f)
                    return Response({"message": "Successful", "status_data": [status_data_val], "remarks": Sku_Serializer, "data": sku_serializars_v, 'status': True})
            last_30_day = today_date.date()-datetime.timedelta(days =45)
            last_30_sales = SalesData.objects.filter(sales_date_time__gte=last_30_day)
            if user_type == 'WD':
                if week_num is not None:  # WD's Weekly sale==============================
                    if wd_id:
                        wo_4th = [1]

                        wd_town_id_list = Sales_Hierarchy_Master.objects.filter(
                            wd_id=wd_id).values_list('wd_town_id', flat=True)
                        sku_id_list = WdSkuCatagory.objects.filter(
                            wd_town_id__in=wd_town_id_list).values_list('sku_id', flat=True)
                        topsqu_list = last_30_sales.filter(sku_id__in=sku_id_list, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time__gte=last_date, brand_category=category, transaction_type=week_num).values_list(
                            'sku_id', flat=True).annotate(sku_totalsale=Sum('grand_total')).order_by('-sku_totalsale')
                        sku_list_top = []
                        sku_id_list3 = list(set(list(sku_id_list)))
                        for i in topsqu_list:
                            if i in sku_id_list3:
                                sku_list_top.append(i)
                                sku_id_list3.remove(i)
                        sku_lists = sku_list_top+sku_id_list3
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
                                Salesobj = last_30_sales.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time=week_details[
                                                                    2][1], brand_category=category, transaction_type=week_details[1], town_code__in=town_id).values()
                            else:
                                Salesobj = last_30_sales.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list,
                                                                    sales_date_time=week_details[2][1], transaction_type=week_details[1], town_code__in=town_id).values()

                            if Salesobj:
                                i["SalesData"] = Salesobj

                                if x in day_list:
                                    status_data.append(
                                        {'lock_status': request.user.lock_unlock, "freeze_status": False, "update_status": True})
                                else:
                                    status_data.append(
                                        {'lock_status': request.user.lock_unlock, "freeze_status": True, "update_status": False})

                            else:
                                i["SalesData"] = [{}]

                                if week_details[2] is not None:
                                    not_sales_unfreeze = last_30_sales.filter((Q(transaction_type__contains="Week")), sales_date_time__gte=week_details[2][0], sales_date_time__lte=week_details[
                                                                                  2][1], sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id, freeze_status=True)
                                    not_sales_unfreeze2 = last_30_sales.filter(sales_date_time__gte=week_details[2][0], sales_date_time__lte=week_details[
                                                                                   2][1], wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id, freeze_status=True)
                                    not_sales_unfreeze1 = last_30_sales.filter(
                                        sales_date_time__gte=week_details[2][0], sales_date_time__lte=week_details[2][1], wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id)
                                if not_sales_unfreeze2 and not_sales_unfreeze1:
                                    if len(not_sales_unfreeze2) == len(not_sales_unfreeze1):
                                        global_freeze = True
                                elif x in day_list:
                                    status_data.append(
                                        {'lock_status': request.user.lock_unlock, "freeze_status": False, "update_status": True})
                                else:
                                    status_data.append(
                                        {'lock_status': request.user.lock_unlock, "freeze_status": True, "update_status": False})

                # WD side daily get sales data===========================
                else:
                    if wd_id:
                        wd_town_id_list = Sales_Hierarchy_Master.objects.filter(
                            wd_id=wd_id, town_code__in=town_id).values_list('wd_town_id', flat=True)
                        sku_id_list = WdSkuCatagory.objects.filter(
                            wd_town_id__in=wd_town_id_list).values_list('sku_id', flat=True)
                        topsqu_list = last_30_sales.filter(sku_id__in=sku_id_list, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, sales_date_time__gte=last_date, transaction_type="DAILY").values_list(
                            'sku_id', flat=True).annotate(sku_totalsale=Sum('grand_total')).order_by('-sku_totalsale')
                        sku_list_top = []
                        sku_id_list3 = list(set(list(sku_id_list)))
                        for i in topsqu_list:
                            if i in sku_id_list3:
                                sku_list_top.append(i)
                                sku_id_list3.remove(i)
                        sku_lists = sku_list_top+sku_id_list3
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

                                Salesobj = last_30_sales.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list,
                                                                    brand_category=category, sales_date_time=date_f, transaction_type="DAILY", town_code__in=town_id).values()
                            else:
                                Salesobj = last_30_sales.filter(
                                    sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time=date_f, transaction_type="DAILY", town_code__in=town_id).values()
                            i["SalesData"] = Salesobj
                            till_date.time()

                            cont_list = [8, 15, 22, 1]
                            a = str(today_date.date())
                            x = a.split('-')
                            date = int(x[2])

                            if Salesobj:

                                i["SalesData"] = Salesobj
                                # Salesobjs = last_30_sales.filter(sku_id=sku_id,wd_id=wd_id,town_id__in=wd_town_id_list).last()
                                Salesobjs = last_30_sales.filter(
                                    sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list).last()
                                str_date = Salesobj[0]['sales_date_time']
                                dates = datetime.datetime.strptime(
                                    str(str_date), "%Y-%m-%d").date()
                                user_lock_unlock = User.objects.filter(
                                    user_id=Salesobjs.wd_id).last()

                                date = dates+datetime.timedelta(days=1)
                                combime = datetime.datetime.combine(
                                    dates, till_date.time())
                                combine_d_t = datetime.datetime.combine(
                                    date, till_date.time())
                                day_from_date = get_date - \
                                    datetime.timedelta(days=2)
                                beafore_2day = today_date - \
                                    datetime.timedelta(days=2)

                                if get_date.strftime("%A") == "Saturday" and today_date.time() <= till_date.time() and beafore_2day.date() == get_date:
                                    status_data.append(
                                        {"update_status": True, "user_lock_unlock": request.user.lock_unlock})
                                elif combime <= combine_d_t and combine_d_t > today_date:
                                    status_data.append(
                                        {"update_status": True, "user_lock_unlock": user_lock_unlock.lock_unlock})

                                else:
                                    status_data = [
                                        {'update_status': False, "user_lock_unlock": user_lock_unlock.lock_unlock}]

                            else:
                                i["SalesData"] = [{}]
                                StartDate = date_f
                                Date = datetime.datetime.strptime(
                                    StartDate, "%Y-%m-%d")
                                till_date = datetime.datetime(
                                    2009, 10, 5, 14, 59, 59)
                                till_date.time()
                                comb_d_t = datetime.datetime.combine(
                                    Date.date(), till_date.time())+timedelta(days=1)
                                now_current = today_date

                                day_from_date = get_date
                                beafore_2day = today_date - \
                                    datetime.timedelta(days=2)

                                # print(now_current,"<=",comb_d_t,"======",today_date.date(),get_date)
                                # print("===================",now_current<=comb_d_t , today_date.date()>=get_date)
                                if get_date.strftime("%A") == "Saturday" and today_date.time() <= till_date.time() and beafore_2day.date() == get_date:
                                    status_data.append(
                                        {"update_status": True, "user_lock_unlock": request.user.lock_unlock})
                                elif now_current <= comb_d_t and today_date.date() >= get_date:
                                    status_data.append(
                                        {'update_status': True, "user_lock_unlock": request.user.lock_unlock})
                                else:
                                    status_data.append(
                                        {'update_status': False, "user_lock_unlock": request.user.lock_unlock})

            if user_type == 'BRANCH USER':

                a = date_f
                x = a.split('-')
                date = int(x[2])
                now_day = str(today_date.date())
                splited = now_day.split('-')

                now_date = today_date.date()
                # now_day=str(today_date.date())
                splited = now_day.split('-')

                list1 = [1, 2, 3, 4, 5, 6, 7]
                list2 = [8, 9, 10, 11, 12, 13, 14]
                list3 = [15, 16, 17, 18, 19, 20, 21]
                list4 = [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 1, 2]
                li = [1, 2]

                str_date = str(datetime.datetime(today_date.date(
                ).year, today_date.date().month, 1).date()-datetime.timedelta(days=10))
                get_22th = datetime.datetime(today_date.date().year, today_date.date(
                ).month, 1).date()-datetime.timedelta(days=10)
                get_2nd = datetime.datetime(today_date.date().year, today_date.date(
                ).month, 1).date()+datetime.timedelta(days=1)
                splt = str_date.split('-')
                global_freeze = ''

                if week_num is not None:  # this will exicute for BRANCH_USER Weekly data
                    if wd_id:
                        wo_4th = [1, 2, 3]
                        if x in wo_4th:
                            week_sale_date = today_date.date() - relativedelta(months=1)
                        else:
                            week_sale_date = today_date.date()
                        wd_town_id_list = Sales_Hierarchy_Master.objects.filter(
                            wd_id=wd_id).values_list('wd_town_id', flat=True)
                        sku_id_list = WdSkuCatagory.objects.filter(
                            wd_town_id__in=wd_town_id_list).values_list('sku_id', flat=True)
                        topsqu_list = last_30_sales.filter(sku_id__in=sku_id_list, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, sales_date_time__gte=last_date, transaction_type=week_num).values_list(
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
                                Salesobj = last_30_sales.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time=week_details[
                                                                    2][1], brand_category=category, transaction_type=week_details[1], town_code__in=town_id).values()
                            else:
                                Salesobj = last_30_sales.filter(
                                    sku_id=sku_id, sales_date_time=week_details[2][1], wd_id=wd_id, town_id__in=wd_town_id_list, transaction_type=week_details[1], town_code__in=town_id).values()
                            if Salesobj:
                                # if len(Salesobj)>1:
                                #     a = len(Salesobj)-1
                                #     # print(Salesobj_duplicate,"===============//==========")
                                #     # Salesobj = Salesobj[-1]
                                #     last_30_sales.filter(sku_id=sku_id,sales_date_time = week_details[2][1], wd_id=wd_id,town_id__in=wd_town_id_list,transaction_type=week_details[1],town_code = town_id).order_by('id')[:a].delete()
                                #     Salesobj = last_30_sales.filter(sku_id=sku_id,sales_date_time = week_details[2][1], wd_id=wd_id,town_id__in=wd_town_id_list,transaction_type=week_details[1],town_code = town_id).values()
                                #     # .delete()
                                i["SalesData"] = Salesobj
                                Salesobjfrez = last_30_sales.filter(freeze_status=True, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time=week_details[
                                                                        2][1], brand_category=category, transaction_type=week_details[1], town_code__in=town_id).values()
                                if Salesobjfrez:
                                    status_data.append(
                                        {"freeze_status": True, "update_status": False})
                                else:
                                    status_data.append(
                                        {"freeze_status": False, "update_status": True})

                            else:
                                i["SalesData"] = [{}]
                                a = str(date_f)
                                x = a.split('-')
                                date = int(x[2])
                                dt = int(str(today_date.date()).split('-')[2])
                                if week_details[2] is not None:
                                    not_sales_unfreeze = last_30_sales.filter((Q(transaction_type__contains=week_details[1])), sales_date_time__gte=week_details[2][0], sales_date_time__lte=week_details[2][1], sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id, freeze_status=True)

                                if dt <= 11 and get_date.month == today_date.date().month and get_date.year == today_date.date().year and get_date <= today_date.date():
                                    status_data = [
                                        {"freeze_status": False, "update_status": True}]
                                    i["SalesData"] = [{"freeze_status": False}]
                                elif dt <= 17 and get_date.month == today_date.date().month and get_date.year == today_date.date().year and get_date <= today_date.date():
                                    status_data = [
                                        {"freeze_status": False, "update_status": True}]
                                    i["SalesData"] = [{"freeze_status": False}]
                                elif dt <= 23 and get_date.month == today_date.date().month and get_date.year == today_date.date().year and get_date <= today_date.date():
                                    status_data = [
                                        {"freeze_status": False, "update_status": True}]
                                    i["SalesData"] = [{"freeze_status": False}]
                                elif dt <= 2 and get_date.month == today_date.date().month and get_date.year == today_date.date().year and get_date <= today_date.date():
                                    i["SalesData"] = [{"freeze_status": False}]
                                    status_data = [
                                        {"freeze_status": False, "update_status": True}]
                                else:
                                    i["SalesData"] = [{"freeze_status": False}]
                                    status_data = [
                                        {"freeze_status": True, "update_status": False}]

                else:  # this will exicute for BRANCH_USER Weekly data========================
                    if wd_id:
                        previus_day = now_date.replace(day=1) - datetime.timedelta(days=1)
                        prev_week_4th = datetime.datetime(previus_day.year, previus_day.month, 22).date()
                        wd_town_id_list = Sales_Hierarchy_Master.objects.filter(
                            wd_id=wd_id).values_list('wd_town_id', flat=True)
                        sku_id_list = WdSkuCatagory.objects.filter(
                            wd_town_id__in=wd_town_id_list).values_list('sku_id', flat=True)
                        topsqu_list = last_30_sales.filter(sku_id__in=sku_id_list, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, sales_date_time__gte=last_date, transaction_type="DAILY").values_list(
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

                                Salesobj = last_30_sales.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list,
                                                                    brand_category=category, sales_date_time=date_f, transaction_type="DAILY", town_code__in=town_id).values()
                            else:
                                Salesobj = last_30_sales.filter(
                                    sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time=date_f, transaction_type="DAILY", town_code__in=town_id).values()
                            print(Salesobj,"=====",category,date_f,wd_id,wd_town_id_list,town_id,sku_id)
                            if Salesobj:

                                i["SalesData"] = Salesobj

                                list1 = [1, 2, 3, 4, 5, 6, 7]
                                list2 = [8, 9, 10, 11, 12, 13, 14]
                                list3 = [15, 16, 17, 18, 19, 20, 21]
                                list4 = [22, 23, 24, 25, 26,
                                         27, 28, 29, 30, 31, 1, 2, 3]
                                li = [1, 2]

                                freeze_obj = last_30_sales.filter(
                                    sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, sales_date_time=date_f, transaction_type="DAILY", freeze_status=0)
                                if int(splited[2]) in list4 and (get_date >= week_4th[0].date() or get_date >= prev_week_4th) and get_date <= now_date:
                                    if freeze_obj:
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                    else:
                                        status_data.append(
                                            {"freeze_status": True, "update_status": False})

                                elif 1 <= date <= 10 and int(splited[2]) <= 10 and get_date <= now_date and int(today_date.date().year) == int(x[0]) and int(today_date.date().month) == int(x[1]):
                                    if freeze_obj:
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                    else:
                                        status_data.append(
                                            {"freeze_status": True, "update_status": False})

                                elif 8 <= date <= 17 and int(splited[2]) <= 17 and get_date <= now_date and int(today_date.date().year) == int(x[0]) and int(today_date.date().month) == int(x[1]):
                                    if freeze_obj:
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                    else:
                                        status_data.append(
                                            {"freeze_status": True, "update_status": False})

                                elif 15 <= date <= 23 and int(splited[2]) <= 23 and get_date <= now_date and int(today_date.date().year) == int(x[0]) and int(today_date.date().month) == int(x[1]):
                                    if freeze_obj:
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                    else:
                                        status_data.append(
                                            {"freeze_status": True, "update_status": False})

                                else:
                                    status_data.append(
                                        {"freeze_status": True, "update_status": False})

                            else:
                                not_sales_unfreeze2 = None
                                not_sales_unfreeze1 = None
                                not_sales_unfreeze = ''
                                i["SalesData"] = [{}]
                                print(week_4th[0].date(),"==================>>>")
                                # breakpoint()
                                if week_details[2] is not None and get_date < week_details[2][1]:
                                    not_sales_unfreeze = last_30_sales.filter((Q(transaction_type__contains=week_details[1])), sales_date_time__gte=str(week_details[2][0]), sales_date_time__lte=str(
                                        week_details[2][1]), sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id, freeze_status=True)
                                #     not_sales_unfreeze2 = last_30_sales.filter(sales_date_time__gte = week_rng[0] ,sales_date_time__lte = week_rng[1],wd_id=wd_id,town_id__in=wd_town_id_list,brand_category=category,town_code = town_id,freeze_status = True)
                                #     not_sales_unfreeze1 = last_30_sales.filter(sales_date_time__gte = week_rng[0] ,sales_date_time__lte = week_rng[1],wd_id=wd_id,town_id__in=wd_town_id_list,brand_category=category,town_code = town_id)
                                # # print(not_sales_unfreeze2)
                                # if not_sales_unfreeze2 and not_sales_unfreeze1:
                                #     if len(not_sales_unfreeze2) == len(not_sales_unfreeze1):
                                #         global_freeze = True

                                list1 = [1, 2, 3, 4, 5, 6, 7]
                                list2 = [8, 9, 10, 11, 12, 13, 14]
                                list3 = [15, 16, 17, 18, 19, 20, 21]
                                list4 = [22, 23, 24, 25, 26,
                                         27, 28, 29, 30, 31, 1, 2, 3]
                                li = [1, 2]

                                if not_sales_unfreeze:
                                    status_data.append(
                                        {"freeze_status": True, "update_status": False})
                                    i["SalesData"] = [{"freeze_status": True}]
                                else:
                                    ## Remove week_details[2] 28-07-22
                                    if int(splited[2]) in list4 and (get_date >= week_4th[0].date() or get_date >= prev_week_4th) and get_date <= now_date:
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                        i["SalesData"] = [
                                            {"freeze_status": False}]

                                    elif 1 <= date <= 10 and int(splited[2]) <= 10 and get_date <= now_date and int(today_date.date().year) == int(x[0]) and int(today_date.date().month) == int(x[1]):
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                        i["SalesData"] = [
                                            {"freeze_status": False}]

                                    elif 8 <= date <= 17 and int(splited[2]) <= 17 and get_date <= now_date and int(today_date.date().year) == int(x[0]) and int(today_date.date().month) == int(x[1]):
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                        i["SalesData"] = [
                                            {"freeze_status": False}]

                                    elif 15 <= date <= 23 and int(splited[2]) <= 23 and get_date <= now_date and int(today_date.date().year) == int(x[0]) and int(today_date.date().month) == int(x[1]):
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                        i["SalesData"] = [
                                            {"freeze_status": False}]

                                    else:
                                        status_data.append(
                                            {"freeze_status": True, "update_status": False})
                                        i["SalesData"] = [
                                            {"freeze_status": True}]
            status_data_val = None
            not_sales_unfreez = None
            not_sales_unfreeze_len = None
            no_recore = {}
            seeze_count = 0

            print(week_num,"======================")
            # This line for WD and brench_user also for Weekly data
            if week_details[2] is not None and week_num:
                not_sales_unfreez = last_30_sales.filter(
                    sales_date_time=week_details[2][1], transaction_type=week_details[1], wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id).all()
                print(not_sales_unfreez, "=========vv1=======", not_sales_unfreez)
                if not_sales_unfreez:
                    not_sales_unfreeze_len = len(not_sales_unfreez)

            # This line for WD and brench_user also for daily data
            elif week_details[2] is not None and (not week_num):
                print(not_sales_unfreez, "=========vv2=======", not_sales_unfreez)

                not_sales_unfreez = last_30_sales.filter(
                    sales_date_time=week_details[2][1], transaction_type=week_details[1], wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id).all()
                if not_sales_unfreez:
                    not_sales_unfreeze_len = len(not_sales_unfreez)

            elif request.user.user_type == "BRANCH USER" and (not week_num):
    
                if week_details[2] is not None:
                    print(not_sales_unfreez,
                          "=========vv3=======", not_sales_unfreez)
                    if week_details[2][0] <= get_date <= week_details[2][1]:
                        not_sales_unfreez = last_30_sales.filter(sales_date_time__lte=week_details[2][1], transaction_type=week_details[
                                                                     1], wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id, freeze_status=False).count()

            elif request.user.user_type == "WD" and (not week_num):
                if week_details[2] is not None:
                    print(not_sales_unfreez,
                          "=========vv4=======", not_sales_unfreez)
                    if date_f < week_details[2][1]:
                        not_sales_unfreez = last_30_sales.filter(sales_date_time__lte=week_details[2][1], transaction_type=week_details[
                                                                     1], wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id, freeze_status=False).count()

            # for i in status_data:

            if request.user.user_type == "WD" and (not week_num):
                if week_details[2] is not None:
                    if week_details[2][0] <= get_date <= week_details[2][1]:
                        if not_sales_unfreez == 0 or (not (combime <= combine_d_t and combine_d_t > today_date)):
                            if get_date.strftime("%A") == "Saturday" and today_date.time() <= till_date.time() and beafore_2day.date() == get_date:
                                status_data_val = {"update_status": True, "user_lock_unlock": request.user.lock_unlock}
                                # status_data.append(
                                #     {"update_status": True, "user_lock_unlock": request.user.lock_unlock})
                            else:
                                status_data_val = {
                                    'freeze_status': True, 'update_status': False, 'user_lock_unlock': request.user.lock_unlock}
                        elif now_current <= comb_d_t and today_date.date() >= get_date:
                            status_data_val = {"update_status": True, "user_lock_unlock": request.user.lock_unlock}
                            status_data.append(
                                {'update_status': True, "user_lock_unlock": request.user.lock_unlock})
                        else:
                            status_data.append(
                                {'update_status': False, "user_lock_unlock": request.user.lock_unlock})
                    elif week_details[2][0] > get_date:
                        status_data_val = {
                            'freeze_status': True, 'update_status': False, 'user_lock_unlock': request.user.lock_unlock}
                    elif today_date.date() < get_date:
                        status_data_val = {
                            'freeze_status': True, 'update_status': False, 'user_lock_unlock': request.user.lock_unlock}
                    else:
                        status_data_val = {
                            'freeze_status': False, 'update_status': True, 'user_lock_unlock': request.user.lock_unlock}
                else:
                    try:
                        status_data_val = status_data[0]
                    except Exception as e:
                        status_data_val = {}

                # ===================
            elif request.user.user_type == "WD" and week_num:
                # status_data_val = status_data[0]
                if not_sales_unfreez:
                    seeze_count = 0
                    for row in not_sales_unfreez:
                        if row.freeze_status == True:
                            seeze_count = seeze_count + 1
                    if seeze_count == not_sales_unfreeze_len:
                        status_data_val = {
                            'freeze_status': True, 'update_status': False, 'user_lock_unlock': request.user.lock_unlock}
                    else:
                        status_data_val = {
                            'freeze_status': False, 'update_status': True, 'user_lock_unlock': request.user.lock_unlock}
                else:
                    status_data_val = {
                        'freeze_status': False, 'update_status': True, 'user_lock_unlock': request.user.lock_unlock}

            elif request.user.user_type == "BRANCH USER" and (not week_num):
                if week_details[2] is not None:
                    if week_details[2][0] <= get_date <= week_details[2][1]:
                        not_sales_unfreeze_len = len(not_sales_unfreez)
                        seeze_count = 0
                        if not_sales_unfreez:
                            for row in not_sales_unfreez:
                                if row.freeze_status == True:
                                    seeze_count = seeze_count + 1
                            if seeze_count == not_sales_unfreeze_len:
                                status_data_val = {
                                    'freeze_status': True, 'update_status': False}
                            else:
                                status_data_val = {
                                    'freeze_status': False, 'update_status': True}
                        else:
                            status_data_val = {
                                'freeze_status': False, 'update_status': True}
                    elif week_details[2][0] > get_date or get_date > today_date.date():
                        status_data_val = {
                            'freeze_status': True, 'update_status': False}
                    else:
                        status_data_val = {
                            'freeze_status': False, 'update_status': True}
                else:
                    try:
                        status_data_val = status_data[0]
                    except Exception as e:
                        status_data_val = no_recore

            else:  # this condition will exicute branch_user with Weekly condition
                if not_sales_unfreez:
                    seeze_count = 0
                    for row in not_sales_unfreez:
                        if row.freeze_status == True:
                            seeze_count = seeze_count + 1
                    if seeze_count == not_sales_unfreeze_len:
                        status_data_val = {
                            'freeze_status': True, 'update_status': False}
                    else:
                        status_data_val = {
                            'freeze_status': False, 'update_status': True}
                else:
                    status_data_val = {
                        'freeze_status': False, 'update_status': True}

            # print(status_data_val)
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

            return Response({"message": "Successful", "status_data": [status_data_val], "remarks": Sku_Serializer, "data": sku_serializars_v, 'status': True})
        
        # except Exception as e:
        #     error = getattr(e, 'message', repr(e))
        #     logger.error(error)
        #     context = {'status': False,'message':'Something Went Wrong'}
        #     return Response(context, status=status.HTTP_200_OK)


class manualy_crate_weekly(APIView):
    def get(self, request):
        date_list = [11, 18, 25, 4]
        now = datetime.datetime.now()
        now_day = str(now.date())
        splited = now_day.split('-')
        # print(splited[2],"======")
        week_reng = 0
        weekly = 0

        try :
            now_dt = datetime.datetime.now()
            week_1st = [datetime.datetime(now_dt.date().year, now_dt.date().month, 1).date(), datetime.datetime(now_dt.date().year, now_dt.date().month, 7).date()]
            week_2nd = [datetime.datetime(now_dt.date().year, now_dt.date().month, 8).date(), datetime.datetime(now_dt.date().year, now_dt.date().month, 14).date()]
            week_3rd = [datetime.datetime(now_dt.date().year, now_dt.date().month, 15).date(), datetime.datetime(now_dt.date().year, now_dt.date().month, 21).date()]
            last_date_month = datetime.datetime(now_dt.date().year, now_dt.date().month, calendar.monthrange(now_dt.date().year, now_dt.date().month)[1]).date()
            week_4th = [datetime.datetime(
                now_dt.date().year, now_dt.date().month, 22), last_date_month]
            week_4_weekly = [
                week_4th[0] - relativedelta(months=1), now.date().today().replace(day=1) - timedelta(days=1)]
            if int(splited[2]) in date_list:
                if int(splited[2]) == 11:
                    data = SalesData.objects.filter(
                        sales_date_time__gte=week_1st[0], sales_date_time__lte=week_1st[1], freeze_status=False).update(freeze_status=True)
                    return data
                elif int(splited[2]) == 18:
                    data = SalesData.objects.filter(
                        sales_date_time__gte=week_2nd[0], sales_date_time__lte=week_2nd[1], freeze_status=False).update(freeze_status=True)
                    return data
                elif int(splited[2]) == 25:
                    data = SalesData.objects.filter(
                        sales_date_time__gte=week_3rd[0], sales_date_time__lte=week_3rd[1], freeze_status=False).update(freeze_status=True)
                    return data
                elif int(splited[2]) == 4:
                    data = SalesData.objects.filter(
                        sales_date_time__gte=week_4_weekly[0], sales_date_time__lte=week_4_weekly[1], freeze_status=False).update(freeze_status=True)
                    return data
                else:
                    print("Sorry................")

            
            if int(splited[2]) == 1:
                week_reng = week_4_weekly
                weekly = "Week4"
            elif int(splited[2]) == 8:
                week_reng = week_1st
                weekly = "Week1"
            elif int(splited[2]) == 15:
                week_reng = week_2nd
                weekly = "Week2"
            elif int(splited[2]) == 20:
                week_reng = week_3rd
                weekly = "Week3"
            else:
                weekly = ""

            week_val = weekly
            week_val_rng = week_reng
            print(week_val, "========", week_val_rng)
            # add weekly on date constant================>
            date_list_2d = [8,9,10, 15,16,17, 22,23, 1,2,3]
            today = datetime.datetime.now()
            now_day = str(today.date())
            splited_today = now_day.split('-')
            # print(splited_today[2])
            help_week = week_sele_before_date("BRANCH USER")
            # try:
            if help_week[0]:
                print("==============hiiii", help_week)
                # breakpoint()
                if int(splited_today[2]) in date_list_2d:
                    week_data_sum = SalesData.objects.filter(transaction_type='DAILY', sales_date_time__gte=help_week[2][0], sales_date_time__lte=help_week[2][1]).values('wd_id', 'sku_id', 'town_code', 'brand_category').annotate(Sum('local_sales_retail'),
                                                        Sum('local_sales_dealer'), Sum('local_sales_modern_trade'), Sum('local_sales_hawker'), Sum('total_local_sales'), Sum('outstation_sales_reatil'),
                                                        Sum('outstation_sales_dealer'), Sum('outstation_sales_modern_trade'), Sum('outstation_sales_hawker'), Sum('total_outstation_sales'), Sum('other_sales_retail'), Sum('other_sales_dealer'),
                                                        Sum('other_sales_modern_trade'), Sum('total_other_sales'), Sum('other_issues_damage'), Sum('other_issues_return'), Sum('other_issues_other'), Sum('total_issue'), Sum('grand_total'), Sum('value'))
                    if week_data_sum:
                        for week_sale in week_data_sum:
                            source_data = WDmaster.objects.filter(
                                wd_ids=week_sale['wd_id']).last()
                            wd_town_code = Sales_Hierarchy_Master.objects.filter(
                                wd_id=week_sale['wd_id']).last()
                            # print(week_sale['town_code'],help_week[2][1]+datetime.timedelta(days=1))
                            # breakpoint()
                            town_name = WDmaster.objects.filter(
                                wd_ids=week_sale['wd_id'], wd_postal_code__icontains=week_sale['town_code']).values('wd_postal_code').last()
                            wd_town_code = Sales_Hierarchy_Master.objects.filter(
                                wd_id=week_sale['wd_id'], town_code=week_sale['town_code']).values_list('wd_town_id', flat=True)
                            wdobj = WdSkuCatagory.objects.filter(
                                wd_town_id__in=wd_town_code, sku_id=week_sale['sku_id']).last()
                            if wdobj:
                                town_id = wdobj.wd_town_id
                            else:
                                town_id = None

                            week_sale_data = SalesData.objects.filter(
                                sales_date_time=help_week[2][1], wd_id=week_sale['wd_id'], sku_id=week_sale['sku_id'], town_id=town_id, transaction_type=help_week[1], town_code=week_sale['town_code'])
                            if source_data:
                                source_user = source_data.wd_type
                                wd_type = source_data.wd_type
                            else:
                                source_user = None
                                wd_type = "Secondary_sale"

                            if town_name:
                                wd_name = source_data.wd_name
                            else:
                                wd_name = None
                            # print(week_sale['wd_id'],"=======week_val_rng=======",week_sale['sku_id'])
                            if not week_sale_data and town_id is not None:
                                print("create==============")
                                sele_week_obj = SalesData()
                                sele_week_obj.statename=source_data.wd_state
                                sele_week_obj.wd_name = wd_name
                                sele_week_obj.town_name = source_data.wd_postal_code
                                sele_week_obj.wd_type = wd_type
                                sele_week_obj.town_code = week_sale['town_code']
                                sele_week_obj.town_id = town_id
                                sele_week_obj.sku_id = week_sale['sku_id']
                                sele_week_obj.wd_id = week_sale['wd_id']
                                sele_week_obj.sales_date_time = help_week[2][1]
                                # -datetime.timedelta(days=1)
                                sele_week_obj.transaction_source = source_user
                                sele_week_obj.created_by = 'auto_scheduler'
                                sele_week_obj.transaction_type = help_week[1]
                                sele_week_obj.created_date = datetime.datetime.now()
                                sele_week_obj.local_sales_retail = round(week_sale['local_sales_retail__sum'], 3)
                                sele_week_obj.local_sales_dealer = round(week_sale['local_sales_dealer__sum'], 3)
                                sele_week_obj.local_sales_modern_trade = round(week_sale['local_sales_modern_trade__sum'], 3)
                                sele_week_obj.local_sales_hawker = round(week_sale['local_sales_hawker__sum'], 3)
                                sele_week_obj.outstation_sales_reatil = round(week_sale['outstation_sales_reatil__sum'], 3)
                                sele_week_obj.outstation_sales_dealer = round(week_sale['outstation_sales_dealer__sum'], 3)
                                sele_week_obj.outstation_sales_modern_trade = round(week_sale['outstation_sales_modern_trade__sum'], 3)
                                sele_week_obj.outstation_sales_hawker = round(week_sale['outstation_sales_hawker__sum'], 3)
                                sele_week_obj.other_sales_retail = round(week_sale['other_sales_retail__sum'], 3)
                                sele_week_obj.other_sales_dealer = round(week_sale['other_sales_dealer__sum'], 3)
                                sele_week_obj.other_sales_modern_trade = round(week_sale['other_sales_modern_trade__sum'], 3)
                                sele_week_obj.other_issues_other = round(week_sale['other_issues_other__sum'], 3)
                                sele_week_obj.other_issues_damage = round(week_sale['other_issues_damage__sum'], 3)
                                sele_week_obj.other_issues_return = round(week_sale['other_issues_return__sum'], 3)
                                sele_week_obj.total_local_sales = round(week_sale['total_local_sales__sum'], 3)
                                sele_week_obj.total_outstation_sales = round(week_sale['total_outstation_sales__sum'], 3)
                                sele_week_obj.total_other_sales = round(week_sale['total_other_sales__sum'], 3)
                                sele_week_obj.total_issue = round(week_sale['total_issue__sum'], 3)
                                sele_week_obj.grand_total = round(week_sale['grand_total__sum'], 3)

                                sele_week_obj.brand_category = week_sale['brand_category']
                                # sele_week_obj.last_updated_date = datetime.datetime.now()

                                unit_value = SKU_Master_Product.objects.filter(
                                    sku_id=week_sale['sku_id']).last()
                                if unit_value:
                                    sku_code = unit_value.sku_code
                                    sku_short_name = unit_value.sku_short_name
                                    sele_week_obj.company = unit_value.company
                                else:
                                    sku_code = None
                                    sku_short_name = unit_val.sku_short_name
                                    sele_week_obj.company = "unit_value.company"
                                category_data = WdSkuCatagory.objects.filter(
                                    wd_town_id=town_id, sku_id=week_sale['sku_id']).last()

                                if category_data:
                                    sele_week_obj.cnf_id = category_data.cnf_id
                                    unit_val = category_data.last_price
                                else:
                                    sele_week_obj.cnf_id = None
                                    unit_val = 0
                                wdregion = User.objects.filter(
                                    user_id=week_sale['wd_id']).last()
                                region = BranchMaster.objects.filter(
                                    branch_code=wdregion.locationcode).last()
                                sele_week_obj.sku_code = sku_code
                                sele_week_obj.sku_short_name = sku_short_name
                                sele_week_obj.region = region.region
                                sele_week_obj.unit_price = unit_val
                                sele_week_obj.value = sele_week_obj.grand_total * sele_week_obj.unit_price
                                sele_week_obj.distrcode = str(
                                    week_sale['wd_id'])+"-"+str(week_sale['town_code'])

                                sele_week_obj.save()
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)


class Schedule_Week_Generate(viewsets.ModelViewSet):
    serializer_class = SalesDataSerializer
    def get_queryset(self):
        try:
            print("=========================week generate=====>>")
            # breakpoint()
            help_week = week_sele_before_date("BRANCH USER")
            today = datetime.datetime.now()
            now_day = str(today.date())
            splited_today = now_day.split('-')
            date_list_2d =  [1,8, 15, 22]
            
            if help_week[0]:
                
                if int(splited_today[2]) in date_list_2d:
                    week_data_sum = SalesData.objects.filter(transaction_type='DAILY', sales_date_time__gte=help_week[2][0], sales_date_time__lte=help_week[2][1]).values('wd_id', 'sku_id', 'town_code', 'brand_category').annotate(Sum('local_sales_retail'),
                                                        Sum('local_sales_dealer'), Sum('local_sales_modern_trade'), Sum('local_sales_hawker'), Sum('total_local_sales'), Sum('outstation_sales_reatil'),
                                                        Sum('outstation_sales_dealer'), Sum('outstation_sales_modern_trade'), Sum('outstation_sales_hawker'), Sum('total_outstation_sales'), Sum('other_sales_retail'), Sum('other_sales_dealer'),
                                                        Sum('other_sales_modern_trade'), Sum('total_other_sales'), Sum('other_issues_damage'), Sum('other_issues_return'), Sum('other_issues_other'), Sum('total_issue'), Sum('grand_total'), Sum('value'))
                    if week_data_sum:
                        for week_sale in week_data_sum:
                            source_data = WDmaster.objects.filter(
                                wd_ids=week_sale['wd_id']).last()
                            wd_town_code = Sales_Hierarchy_Master.objects.filter(
                                wd_id=week_sale['wd_id']).last()
                            # print(week_sale['town_code'],help_week[2][1]+datetime.timedelta(days=1))
                            # breakpoint()
                            town_name = WDmaster.objects.filter(
                                wd_ids=week_sale['wd_id'], wd_postal_code__icontains=week_sale['town_code']).values('wd_postal_code').last()
                            wd_town_code = Sales_Hierarchy_Master.objects.filter(
                                wd_id=week_sale['wd_id'], town_code=week_sale['town_code']).values_list('wd_town_id', flat=True)
                            wdobj = WdSkuCatagory.objects.filter(
                                wd_town_id__in=wd_town_code, sku_id=week_sale['sku_id']).last()
                            if wdobj:
                                town_id = wdobj.wd_town_id
                            else:
                                town_id = None

                            week_sale_data = SalesData.objects.filter(
                                sales_date_time=help_week[2][1], wd_id=week_sale['wd_id'], sku_id=week_sale['sku_id'], town_id=town_id, transaction_type=help_week[1], town_code=week_sale['town_code'])
                            if source_data:
                                source_user = source_data.wd_type
                                wd_type = source_data.wd_type
                            else:
                                source_user = None
                                wd_type = "Secondary_sale"

                            if town_name:
                                wd_name = source_data.wd_name
                            else:
                                wd_name = None
                            # print(week_sale['wd_id'],"=======week_val_rng=======",week_sale['sku_id'])
                            if not week_sale_data and town_id is not None:
                                print("create==============")
                                sele_week_obj = SalesData()
                                sele_week_obj.wd_name = wd_name
                                sele_week_obj.town_name = source_data.wd_postal_code
                                sele_week_obj.wd_type = wd_type
                                sele_week_obj.town_code = week_sale['town_code']
                                sele_week_obj.town_id = town_id
                                sele_week_obj.sku_id = week_sale['sku_id']
                                sele_week_obj.wd_id = week_sale['wd_id']
                                sele_week_obj.sales_date_time = help_week[2][1]
                                # -datetime.timedelta(days=1)
                                sele_week_obj.transaction_source = source_user
                                sele_week_obj.created_by = 'auto_scheduler'
                                sele_week_obj.transaction_type = help_week[1]
                                sele_week_obj.created_date = datetime.datetime.now()
                                sele_week_obj.local_sales_retail = round(week_sale['local_sales_retail__sum'], 2)
                                sele_week_obj.local_sales_dealer = round(week_sale['local_sales_dealer__sum'], 2)
                                sele_week_obj.local_sales_modern_trade = round(week_sale['local_sales_modern_trade__sum'], 2)
                                sele_week_obj.local_sales_hawker = round(week_sale['local_sales_hawker__sum'], 2)
                                sele_week_obj.outstation_sales_reatil = round(week_sale['outstation_sales_reatil__sum'], 2)
                                sele_week_obj.outstation_sales_dealer = round(week_sale['outstation_sales_dealer__sum'], 2)
                                sele_week_obj.outstation_sales_modern_trade = round(week_sale['outstation_sales_modern_trade__sum'], 2)
                                sele_week_obj.outstation_sales_hawker = round(week_sale['outstation_sales_hawker__sum'], 2)
                                sele_week_obj.other_sales_retail = round(week_sale['other_sales_retail__sum'], 2)
                                sele_week_obj.other_sales_dealer = round(week_sale['other_sales_dealer__sum'], 2)
                                sele_week_obj.other_sales_modern_trade = round(week_sale['other_sales_modern_trade__sum'], 2)
                                sele_week_obj.other_issues_other = round(week_sale['other_issues_other__sum'], 2)
                                sele_week_obj.other_issues_damage = round(week_sale['other_issues_damage__sum'], 2)
                                sele_week_obj.other_issues_return = round(week_sale['other_issues_return__sum'], 2)
                                sele_week_obj.total_local_sales = round(week_sale['total_local_sales__sum'], 2)
                                sele_week_obj.total_outstation_sales = round(week_sale['total_outstation_sales__sum'], 2)
                                sele_week_obj.total_other_sales = round(week_sale['total_other_sales__sum'], 2)
                                sele_week_obj.total_issue = round(week_sale['total_issue__sum'], 2)
                                sele_week_obj.grand_total = round(week_sale['grand_total__sum'], 2)

                                sele_week_obj.brand_category = week_sale['brand_category']
                                # sele_week_obj.last_updated_date = datetime.datetime.now()

                                unit_value = SKU_Master_Product.objects.filter(
                                    sku_id=week_sale['sku_id']).last()
                                if unit_value:
                                    sku_code = unit_value.sku_code
                                    sku_short_name = unit_value.sku_short_name
                                    sele_week_obj.company = unit_value.company
                                else:
                                    sku_code = None
                                    sku_short_name = unit_val.sku_short_name
                                    sele_week_obj.company = "unit_value.company"
                                category_data = WdSkuCatagory.objects.filter(
                                    wd_town_id=town_id, sku_id=week_sale['sku_id']).last()

                                if category_data:
                                    sele_week_obj.cnf_id = category_data.cnf_id
                                    unit_val = category_data.last_price
                                else:
                                    sele_week_obj.cnf_id = None
                                    unit_val = 0
                                wdregion = User.objects.filter(
                                    user_id=week_sale['wd_id']).last()
                                region = BranchMaster.objects.filter(
                                    branch_code=wdregion.locationcode).last()
                                sele_week_obj.sku_code = sku_code
                                sele_week_obj.sku_short_name = sku_short_name
                                sele_week_obj.region = region.region
                                sele_week_obj.unit_price = unit_val
                                sele_week_obj.value = sele_week_obj.grand_total * sele_week_obj.unit_price
                                sele_week_obj.distrcode = str(
                                    week_sale['wd_id'])+"-"+str(week_sale['town_code'])

                                sele_week_obj.save()
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)
        
        
# Start  Weekly update code >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Schedule_Week_update_code(generics.ListCreateAPIView):
    serializer_class = SalesDataSerializer
    def get_queryset(self):
        try:
            print("=========================week generate=====>>")
            # breakpoint()
            help_week = week_sele_before_date("BRANCH USER")
            today = datetime.datetime.now()
            now_day = str(today.date())
           
            
            if help_week[0]:
                
               
                    week_data_sum = SalesData.objects.filter(transaction_type='DAILY', sales_date_time__gte=help_week[2][0], sales_date_time__lte=help_week[2][1]).values('wd_id', 'sku_id', 'town_code', 'brand_category').annotate(Sum('local_sales_retail'),
                                                        Sum('local_sales_dealer'), Sum('local_sales_modern_trade'), Sum('local_sales_hawker'), Sum('total_local_sales'), Sum('outstation_sales_reatil'),
                                                        Sum('outstation_sales_dealer'), Sum('outstation_sales_modern_trade'), Sum('outstation_sales_hawker'), Sum('total_outstation_sales'), Sum('other_sales_retail'), Sum('other_sales_dealer'),
                                                        Sum('other_sales_modern_trade'), Sum('total_other_sales'), Sum('other_issues_damage'), Sum('other_issues_return'), Sum('other_issues_other'), Sum('total_issue'), Sum('grand_total'), Sum('value'))
                    if week_data_sum:
                        week_sale_data = SalesData.objects.filter(
                            sales_date_time=help_week[2][1],  town_id=town_id, transaction_type=help_week[1], freeze_status=True).delete()
                
                        for week_sale in week_data_sum:
                            source_data = WDmaster.objects.filter(
                                wd_ids=week_sale['wd_id']).last()
                            wd_town_code = Sales_Hierarchy_Master.objects.filter(
                                wd_id=week_sale['wd_id']).last()
                            # print(week_sale['town_code'],help_week[2][1]+datetime.timedelta(days=1))
                            # breakpoint()
                            town_name = WDmaster.objects.filter(
                                wd_ids=week_sale['wd_id'], wd_postal_code__icontains=week_sale['town_code']).values('wd_postal_code').last()
                            wd_town_code = Sales_Hierarchy_Master.objects.filter(
                                wd_id=week_sale['wd_id'], town_code=week_sale['town_code']).values_list('wd_town_id', flat=True)
                            wdobj = WdSkuCatagory.objects.filter(
                                wd_town_id__in=wd_town_code, sku_id=week_sale['sku_id']).last()
                            if wdobj:
                                town_id = wdobj.wd_town_id
                            else:
                                town_id = None

                            week_sale_data = SalesData.objects.filter(
                                sales_date_time=help_week[2][1], wd_id=week_sale['wd_id'], sku_id=week_sale['sku_id'], town_id=town_id, transaction_type=help_week[1], town_code=week_sale['town_code'])
                            if source_data:
                                source_user = source_data.wd_type
                                wd_type = source_data.wd_type
                            else:
                                source_user = None
                                wd_type = "Secondary_sale"

                            if town_name:
                                wd_name = source_data.wd_name
                            else:
                                wd_name = None
                            # print(week_sale['wd_id'],"=======week_val_rng=======",week_sale['sku_id'])
                            if not week_sale_data and town_id is not None:
                                print("create==============")
                                sele_week_obj = SalesData()
                                sele_week_obj.wd_name = wd_name
                                sele_week_obj.town_name = source_data.wd_postal_code
                                sele_week_obj.wd_type = wd_type
                                sele_week_obj.town_code = week_sale['town_code']
                                sele_week_obj.town_id = town_id
                                sele_week_obj.sku_id = week_sale['sku_id']
                                sele_week_obj.wd_id = week_sale['wd_id']
                                sele_week_obj.sales_date_time = help_week[2][1]
                                # -datetime.timedelta(days=1)
                                sele_week_obj.transaction_source = source_user
                                sele_week_obj.created_by = 'auto_scheduler'
                                sele_week_obj.transaction_type = help_week[1]
                                sele_week_obj.created_date = datetime.datetime.now()
                                sele_week_obj.local_sales_retail = round(week_sale['local_sales_retail__sum'], 2)
                                sele_week_obj.local_sales_dealer = round(week_sale['local_sales_dealer__sum'], 2)
                                sele_week_obj.local_sales_modern_trade = round(week_sale['local_sales_modern_trade__sum'], 2)
                                sele_week_obj.local_sales_hawker = round(week_sale['local_sales_hawker__sum'], 2)
                                sele_week_obj.outstation_sales_reatil = round(week_sale['outstation_sales_reatil__sum'], 2)
                                sele_week_obj.outstation_sales_dealer = round(week_sale['outstation_sales_dealer__sum'], 2)
                                sele_week_obj.outstation_sales_modern_trade = round(week_sale['outstation_sales_modern_trade__sum'], 2)
                                sele_week_obj.outstation_sales_hawker = round(week_sale['outstation_sales_hawker__sum'], 2)
                                sele_week_obj.other_sales_retail = round(week_sale['other_sales_retail__sum'], 2)
                                sele_week_obj.other_sales_dealer = round(week_sale['other_sales_dealer__sum'], 2)
                                sele_week_obj.other_sales_modern_trade = round(week_sale['other_sales_modern_trade__sum'], 2)
                                sele_week_obj.other_issues_other = round(week_sale['other_issues_other__sum'], 2)
                                sele_week_obj.other_issues_damage = round(week_sale['other_issues_damage__sum'], 2)
                                sele_week_obj.other_issues_return = round(week_sale['other_issues_return__sum'], 2)
                                sele_week_obj.total_local_sales = round(week_sale['total_local_sales__sum'], 2)
                                sele_week_obj.total_outstation_sales = round(week_sale['total_outstation_sales__sum'], 2)
                                sele_week_obj.total_other_sales = round(week_sale['total_other_sales__sum'], 2)
                                sele_week_obj.total_issue = round(week_sale['total_issue__sum'], 2)
                                sele_week_obj.grand_total = round(week_sale['grand_total__sum'], 2)

                                sele_week_obj.brand_category = week_sale['brand_category']
                                # sele_week_obj.last_updated_date = datetime.datetime.now()

                                unit_value = SKU_Master_Product.objects.filter(
                                    sku_id=week_sale['sku_id']).last()
                                if unit_value:
                                    sku_code = unit_value.sku_code
                                    sku_short_name = unit_value.sku_short_name
                                    sele_week_obj.company = unit_value.company
                                else:
                                    sku_code = None
                                    sku_short_name = unit_val.sku_short_name
                                    sele_week_obj.company = "unit_value.company"
                                category_data = WdSkuCatagory.objects.filter(
                                    wd_town_id=town_id, sku_id=week_sale['sku_id']).last()

                                if category_data:
                                    sele_week_obj.cnf_id = category_data.cnf_id
                                    unit_val = category_data.last_price
                                else:
                                    sele_week_obj.cnf_id = None
                                    unit_val = 0
                                wdregion = User.objects.filter(
                                    user_id=week_sale['wd_id']).last()
                                region = BranchMaster.objects.filter(
                                    branch_code=wdregion.locationcode).last()
                                sele_week_obj.sku_code = sku_code
                                sele_week_obj.sku_short_name = sku_short_name
                                sele_week_obj.region = region.region
                                sele_week_obj.unit_price = unit_val
                                sele_week_obj.value = sele_week_obj.grand_total * sele_week_obj.unit_price
                                sele_week_obj.distrcode = str(
                                    week_sale['wd_id'])+"-"+str(week_sale['town_code'])

                                sele_week_obj.save()
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)
# END >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class manualy_crate_weekly_by_date(APIView):
       def get(self,request):
            # try:
                from_date = request.GET.get('from_date')
                to_date = request.GET.get('to_date')
                week_value = request.GET.get('week_value')
                transaction_value_li = ["Week1","Week2","Week3","Week4"]
                wd_id = request.GET.get('wd_id', None)
                help_week = None
                if week_value in transaction_value_li:
                    help_week = [0,week_value,[from_date,to_date]]
                    
                
                if wd_id:
                    week_data_sum = SalesData.objects.filter(transaction_type='DAILY', wd_id =wd_id, sales_date_time__gte=help_week[2][0], sales_date_time__lte=help_week[2][1]).values('wd_id', 'sku_id', 'town_code', 'brand_category').annotate(Sum('local_sales_retail'),
                                                                Sum('local_sales_dealer'), Sum('local_sales_modern_trade'), Sum('local_sales_hawker'), Sum('total_local_sales'), Sum('outstation_sales_reatil'),
                                                                Sum('outstation_sales_dealer'), Sum('outstation_sales_modern_trade'), Sum('outstation_sales_hawker'), Sum('total_outstation_sales'), Sum('other_sales_retail'), Sum('other_sales_dealer'),
                                                                Sum('other_sales_modern_trade'), Sum('total_other_sales'), Sum('other_issues_damage'), Sum('other_issues_return'), Sum('other_issues_other'), Sum('total_issue'), Sum('grand_total'), Sum('value'))
                else:
                    week_data_sum = SalesData.objects.filter(transaction_type='DAILY', sales_date_time__gte=help_week[2][0], sales_date_time__lte=help_week[2][1]).values('wd_id', 'sku_id', 'town_code', 'brand_category').annotate(Sum('local_sales_retail'),
                                                                    Sum('local_sales_dealer'), Sum('local_sales_modern_trade'), Sum('local_sales_hawker'), Sum('total_local_sales'), Sum('outstation_sales_reatil'),
                                                                    Sum('outstation_sales_dealer'), Sum('outstation_sales_modern_trade'), Sum('outstation_sales_hawker'), Sum('total_outstation_sales'), Sum('other_sales_retail'), Sum('other_sales_dealer'),
                                                                    Sum('other_sales_modern_trade'), Sum('total_other_sales'), Sum('other_issues_damage'), Sum('other_issues_return'), Sum('other_issues_other'), Sum('total_issue'), Sum('grand_total'), Sum('value'))
        
                print(week_data_sum,"=====>>")
                # breakpoint()
                if help_week:
                    if week_data_sum:
                        for week_sale in week_data_sum:
                            source_data = WDmaster.objects.filter(
                                wd_ids=week_sale['wd_id']).last()
                            wd_town_code = Sales_Hierarchy_Master.objects.filter(
                                wd_id=week_sale['wd_id']).last()
                            # print(week_sale['town_code'],help_week[2][1]+datetime.timedelta(days=1))
                            # breakpoint()
                            town_name = WDmaster.objects.filter(
                                wd_ids=week_sale['wd_id'], wd_postal_code__icontains=week_sale['town_code']).values('wd_postal_code').last()
                            wd_town_code = Sales_Hierarchy_Master.objects.filter(
                                wd_id=week_sale['wd_id'], town_code=week_sale['town_code']).values_list('wd_town_id', flat=True)
                            wdobj = WdSkuCatagory.objects.filter(
                                wd_town_id__in=wd_town_code, sku_id=week_sale['sku_id']).last()
                            if wdobj:
                                town_id = wdobj.wd_town_id
                            else:
                                town_id = None
        
                            week_sale_data = SalesData.objects.filter(
                                sales_date_time=help_week[2][1], wd_id=week_sale['wd_id'], sku_id=week_sale['sku_id'], town_id=town_id, transaction_type=help_week[1], town_code=week_sale['town_code']).last()
                            if source_data:
                                source_user = source_data.wd_type
                                wd_type = source_data.wd_type
                            else:
                                source_user = None
                                wd_type = "Secondary_sale"
        
                            if town_name:
                                wd_name = source_data.wd_name
                            else:
                                wd_name = None
                            # print(week_sale['wd_id'],"=======week_val_rng=======",week_sale['sku_id'])
                            if not week_sale_data and town_id is not None:
                                print("create==============")
                                sele_week_obj = SalesData()
                                sele_week_obj.wd_name = wd_name
                                sele_week_obj.town_name = source_data.wd_postal_code
                                sele_week_obj.wd_type = wd_type
                                sele_week_obj.town_code = week_sale['town_code']
                                sele_week_obj.town_id = town_id
                                sele_week_obj.sku_id = week_sale['sku_id']
                                sele_week_obj.wd_id = week_sale['wd_id']
                                sele_week_obj.sales_date_time = help_week[2][1]
                                # -datetime.timedelta(days=1)
                                sele_week_obj.transaction_source = source_user
                                sele_week_obj.created_by = 'auto_scheduler'
                                sele_week_obj.transaction_type = help_week[1]
                                sele_week_obj.created_date = datetime.datetime.now()
                                sele_week_obj.local_sales_retail = round(week_sale['local_sales_retail__sum'], 3)
                                sele_week_obj.local_sales_dealer = round(week_sale['local_sales_dealer__sum'], 3)
                                sele_week_obj.local_sales_modern_trade = round(week_sale['local_sales_modern_trade__sum'], 3)
                                sele_week_obj.local_sales_hawker = round(week_sale['local_sales_hawker__sum'], 3)
                                sele_week_obj.outstation_sales_reatil = round(week_sale['outstation_sales_reatil__sum'], 3)
                                sele_week_obj.outstation_sales_dealer = round(week_sale['outstation_sales_dealer__sum'], 3)
                                sele_week_obj.outstation_sales_modern_trade = round(week_sale['outstation_sales_modern_trade__sum'], 3)
                                sele_week_obj.outstation_sales_hawker = round(week_sale['outstation_sales_hawker__sum'], 3)
                                sele_week_obj.other_sales_retail = round(week_sale['other_sales_retail__sum'], 3)
                                sele_week_obj.other_sales_dealer = round(week_sale['other_sales_dealer__sum'], 3)
                                sele_week_obj.other_sales_modern_trade = round(week_sale['other_sales_modern_trade__sum'], 3)
                                sele_week_obj.other_issues_other = round(week_sale['other_issues_other__sum'], 3)
                                sele_week_obj.other_issues_damage = round(week_sale['other_issues_damage__sum'], 3)
                                sele_week_obj.other_issues_return = round(week_sale['other_issues_return__sum'], 3)
                                sele_week_obj.total_local_sales = round(week_sale['total_local_sales__sum'], 3)
                                sele_week_obj.total_outstation_sales = round(week_sale['total_outstation_sales__sum'], 3)
                                sele_week_obj.total_other_sales = round(week_sale['total_other_sales__sum'], 3)
                                sele_week_obj.total_issue = round(week_sale['total_issue__sum'], 3)
                                sele_week_obj.grand_total = round(week_sale['grand_total__sum'], 3)
                                sele_week_obj.cnf_id = wdobj.cnf_id
        
                                sele_week_obj.brand_category = week_sale['brand_category']
                                # sele_week_obj.last_updated_date = datetime.datetime.now()
        
                                unit_value = SKU_Master_Product.objects.filter(
                                    sku_id=week_sale['sku_id']).last()
                                if unit_value:
                                    sku_code = unit_value.sku_code
                                    sku_short_name = unit_value.sku_short_name
                                    sele_week_obj.company = unit_value.company
                                else:
                                    sku_code = None
                                    sku_short_name = unit_val.sku_short_name
                                    sele_week_obj.company = "unit_value.company"
                                category_data = WdSkuCatagory.objects.filter(
                                    wd_town_id=town_id, sku_id=week_sale['sku_id']).last()
        
                                if category_data:
                                    sele_week_obj.cnf_id = category_data.cnf_id
                                    unit_val = category_data.last_price
                                else:
                                    sele_week_obj.cnf_id = None
                                    unit_val = 0
                                wdregion = User.objects.filter(
                                    user_id=week_sale['wd_id']).last()
                                region = BranchMaster.objects.filter(
                                    branch_code=wdregion.locationcode).last()
                                sele_week_obj.sku_code = sku_code
                                sele_week_obj.sku_short_name = sku_short_name
                                sele_week_obj.region = region.region
                                sele_week_obj.unit_price = unit_val
                                sele_week_obj.value = sele_week_obj.grand_total * sele_week_obj.unit_price
                                sele_week_obj.distrcode = str(
                                    week_sale['wd_id'])+"-"+str(week_sale['town_code'])
        
                                sele_week_obj.save()
                            elif week_sale_data and town_id is not None:
                                print("update==============")
                                sele_week_obj = week_sale_data
                                sele_week_obj.wd_name = wd_name
                                sele_week_obj.town_name = source_data.wd_postal_code
                                sele_week_obj.wd_type = wd_type
                                sele_week_obj.town_code = week_sale['town_code']
                                sele_week_obj.town_id = town_id
                                sele_week_obj.sku_id = week_sale['sku_id']
                                sele_week_obj.wd_id = week_sale['wd_id']
                                sele_week_obj.sales_date_time = help_week[2][1]
                                # -datetime.timedelta(days=1)
                                sele_week_obj.transaction_source = source_user
                                sele_week_obj.created_by = 'auto_scheduler'
                                sele_week_obj.transaction_type = help_week[1]
                                # sele_week_obj.created_date = datetime.datetime.now()
                                sele_week_obj.local_sales_retail = round(week_sale['local_sales_retail__sum'], 3)
                                sele_week_obj.local_sales_dealer = round(week_sale['local_sales_dealer__sum'], 3)
                                sele_week_obj.local_sales_modern_trade = round(week_sale['local_sales_modern_trade__sum'], 3)
                                sele_week_obj.local_sales_hawker = round(week_sale['local_sales_hawker__sum'], 3)
                                sele_week_obj.outstation_sales_reatil = round(week_sale['outstation_sales_reatil__sum'], 3)
                                sele_week_obj.outstation_sales_dealer = round(week_sale['outstation_sales_dealer__sum'], 3)
                                sele_week_obj.outstation_sales_modern_trade = round(week_sale['outstation_sales_modern_trade__sum'], 3)
                                sele_week_obj.outstation_sales_hawker = round(week_sale['outstation_sales_hawker__sum'], 3)
                                sele_week_obj.other_sales_retail = round(week_sale['other_sales_retail__sum'], 3)
                                sele_week_obj.other_sales_dealer = round(week_sale['other_sales_dealer__sum'], 3)
                                sele_week_obj.other_sales_modern_trade = round(week_sale['other_sales_modern_trade__sum'], 3)
                                sele_week_obj.other_issues_other = round(week_sale['other_issues_other__sum'], 3)
                                sele_week_obj.other_issues_damage = round(week_sale['other_issues_damage__sum'], 3)
                                sele_week_obj.other_issues_return = round(week_sale['other_issues_return__sum'], 3)
                                sele_week_obj.total_local_sales = round(week_sale['total_local_sales__sum'], 3)
                                sele_week_obj.total_outstation_sales = round(week_sale['total_outstation_sales__sum'], 3)
                                sele_week_obj.total_other_sales = round(week_sale['total_other_sales__sum'], 3)
                                sele_week_obj.total_issue = round(week_sale['total_issue__sum'], 3)
                                sele_week_obj.grand_total = round(week_sale['grand_total__sum'], 3)
                                sele_week_obj.cnf_id = wdobj.cnf_id
        
                                sele_week_obj.brand_category = week_sale['brand_category']
                                sele_week_obj.last_updated_date = datetime.datetime.now()
        
                                unit_value = SKU_Master_Product.objects.filter(
                                    sku_id=week_sale['sku_id']).last()
                                if unit_value:
                                    sku_code = unit_value.sku_code
                                    sku_short_name = unit_value.sku_short_name
                                    sele_week_obj.company = unit_value.company
                                else:
                                    sku_code = None
                                    sku_short_name = unit_val.sku_short_name
                                    sele_week_obj.company = "unit_value.company"
                                category_data = WdSkuCatagory.objects.filter(
                                    wd_town_id=town_id, sku_id=week_sale['sku_id']).last()
        
                                if category_data:
                                    sele_week_obj.cnf_id = category_data.cnf_id
                                    unit_val = category_data.last_price
                                else:
                                    sele_week_obj.cnf_id = None
                                    unit_val = 0
                                wdregion = User.objects.filter(
                                    user_id=week_sale['wd_id']).last()
                                region = BranchMaster.objects.filter(
                                    branch_code=wdregion.locationcode).last()
                                sele_week_obj.sku_code = sku_code
                                sele_week_obj.sku_short_name = sku_short_name
                                sele_week_obj.region = region.region
                                sele_week_obj.unit_price = unit_val
                                sele_week_obj.value = float(sele_week_obj.grand_total) * sele_week_obj.unit_price
                                sele_week_obj.distrcode = str(
                                    week_sale['wd_id'])+"-"+str(week_sale['town_code'])
        
                                sele_week_obj.save()
            # except Exception as e:
            #     from django.core.mail import EmailMessage
            #     error = getattr(e, 'message', repr(e))
            #     logger.error(error)
            #     context = {'status': False,'message':'Something Went Wrong'}
            #     subject = "Weekly Update Scheduller"
            #     recipient_list = ['rasmis@triazinesoft.com']
            #     cc_email = ['rasmis@triazinesoft.com']
            #     html_message = str(context)
            #     reset_email = EmailMessage(
            #                         subject = subject,
            #                         body = html_message,
            #                         from_email = settings.EMAIL_HOST_USER,
            #                         to = recipient_list,
            #                         cc = cc_email,
            #                         reply_to = cc_email,
            #                         )
            #     reset_email.content_subtype = "html"
            #     reset_email.send(fail_silently=True)
            #     return Response(context, status=status.HTTP_200_OK)



# Start >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Schedule_Week_update_code(generics.ListCreateAPIView):
    serializer_class = SalesDataSerializer
    def get_queryset(self):
        try:
            print("=========================week generate=====>>")
            # breakpoint()
            help_week = week_sele_before_date("BRANCH USER")
            today = datetime.datetime.now()
            now_day = str(today.date())
           
            # help_week = ['lllll',"Week3",['2022-12-15','2022-12-21']]
            if help_week[0]:
                
               
                    week_data_sum = SalesData.objects.filter(transaction_type='DAILY', sales_date_time__gte=help_week[2][0], sales_date_time__lte=help_week[2][1]).values('wd_id', 'sku_id', 'town_code', 'brand_category').annotate(Sum('local_sales_retail'),
                                                        Sum('local_sales_dealer'), Sum('local_sales_modern_trade'), Sum('local_sales_hawker'), Sum('total_local_sales'), Sum('outstation_sales_reatil'),
                                                        Sum('outstation_sales_dealer'), Sum('outstation_sales_modern_trade'), Sum('outstation_sales_hawker'), Sum('total_outstation_sales'), Sum('other_sales_retail'), Sum('other_sales_dealer'),
                                                        Sum('other_sales_modern_trade'), Sum('total_other_sales'), Sum('other_issues_damage'), Sum('other_issues_return'), Sum('other_issues_other'), Sum('total_issue'), Sum('grand_total'), Sum('value'))
                    # print(len(week_data_sum),">>>>")
                    if week_data_sum:
                        week_sale_data = SalesData.objects.filter(
                            sales_date_time=help_week[2][1], transaction_type=help_week[1],freeze_status=False)
                        # q = week_sale_data
                        week_sale_data.delete()
                        # week_sale_data1 = SalesData.objects.filter(
                        #     sales_date_time=help_week[2][1], transaction_type=help_week[1], freeze_status=False)
                        # print(help_week[2][1],"=======//",q,"==========nn",week_sale_data1)
                        # breakpoint()
                        for week_sale in week_data_sum:
                            # print("enter=========/////")
                            source_data = WDmaster.objects.filter(
                                wd_ids=week_sale['wd_id']).last()
                            wd_town_code = Sales_Hierarchy_Master.objects.filter(
                                wd_id=week_sale['wd_id']).last()
                            # print(week_sale['town_code'],help_week[2][1]+datetime.timedelta(days=1))
                            # breakpoint()
                            town_name = WDmaster.objects.filter(
                                wd_ids=week_sale['wd_id'], wd_postal_code__icontains=week_sale['town_code']).values('wd_postal_code').last()
                            wd_town_code = Sales_Hierarchy_Master.objects.filter(
                                wd_id=week_sale['wd_id'], town_code=week_sale['town_code']).values_list('wd_town_id', flat=True)
                            wdobj = WdSkuCatagory.objects.filter(
                                wd_town_id__in=wd_town_code, sku_id=week_sale['sku_id']).last()
                            if wdobj:
                                town_id = wdobj.wd_town_id
                            else:
                                town_id = None

                            week_sale_data = SalesData.objects.filter(
                                sales_date_time=help_week[2][1], wd_id=week_sale['wd_id'], sku_id=week_sale['sku_id'], town_id=town_id, transaction_type=help_week[1], town_code=week_sale['town_code'])
                            if source_data:
                                source_user = source_data.wd_type
                                wd_type = source_data.wd_type
                            else:
                                source_user = None
                                wd_type = "Secondary_sale"

                            if town_name:
                                wd_name = source_data.wd_name
                            else:
                                wd_name = None
                            # print(week_sale['wd_id'],"=======week_val_rng=======",week_sale['sku_id'])
                            print(week_sale_data,'-------', town_id)
                            if not week_sale_data and town_id is not None:
                                print("create==============>>")
                                sele_week_obj = SalesData()
                                sele_week_obj.wd_name = wd_name
                                sele_week_obj.town_name = source_data.wd_postal_code
                                sele_week_obj.wd_type = wd_type
                                sele_week_obj.town_code = week_sale['town_code']
                                sele_week_obj.town_id = town_id
                                sele_week_obj.sku_id = week_sale['sku_id']
                                sele_week_obj.wd_id = week_sale['wd_id']
                                sele_week_obj.sales_date_time = help_week[2][1]
                                # -datetime.timedelta(days=1)
                                sele_week_obj.transaction_source = source_user
                                sele_week_obj.created_by = 'auto_scheduler'
                                sele_week_obj.transaction_type = help_week[1]
                                sele_week_obj.created_date = datetime.datetime.now()
                                sele_week_obj.local_sales_retail = round(week_sale['local_sales_retail__sum'], 2)
                                sele_week_obj.local_sales_dealer = round(week_sale['local_sales_dealer__sum'], 2)
                                sele_week_obj.local_sales_modern_trade = round(week_sale['local_sales_modern_trade__sum'], 2)
                                sele_week_obj.local_sales_hawker = round(week_sale['local_sales_hawker__sum'], 2)
                                sele_week_obj.outstation_sales_reatil = round(week_sale['outstation_sales_reatil__sum'], 2)
                                sele_week_obj.outstation_sales_dealer = round(week_sale['outstation_sales_dealer__sum'], 2)
                                sele_week_obj.outstation_sales_modern_trade = round(week_sale['outstation_sales_modern_trade__sum'], 2)
                                sele_week_obj.outstation_sales_hawker = round(week_sale['outstation_sales_hawker__sum'], 2)
                                sele_week_obj.other_sales_retail = round(week_sale['other_sales_retail__sum'], 2)
                                sele_week_obj.other_sales_dealer = round(week_sale['other_sales_dealer__sum'], 2)
                                sele_week_obj.other_sales_modern_trade = round(week_sale['other_sales_modern_trade__sum'], 2)
                                sele_week_obj.other_issues_other = round(week_sale['other_issues_other__sum'], 2)
                                sele_week_obj.other_issues_damage = round(week_sale['other_issues_damage__sum'], 2)
                                sele_week_obj.other_issues_return = round(week_sale['other_issues_return__sum'], 2)
                                sele_week_obj.total_local_sales = round(week_sale['total_local_sales__sum'], 2)
                                sele_week_obj.total_outstation_sales = round(week_sale['total_outstation_sales__sum'], 2)
                                sele_week_obj.total_other_sales = round(week_sale['total_other_sales__sum'], 2)
                                sele_week_obj.total_issue = round(week_sale['total_issue__sum'], 2)
                                sele_week_obj.grand_total = round(week_sale['grand_total__sum'], 2)

                                sele_week_obj.brand_category = week_sale['brand_category']
                                # sele_week_obj.last_updated_date = datetime.datetime.now()

                                unit_value = SKU_Master_Product.objects.filter(
                                    sku_id=week_sale['sku_id']).last()
                                if unit_value:
                                    sku_code = unit_value.sku_code
                                    sku_short_name = unit_value.sku_short_name
                                    sele_week_obj.company = unit_value.company
                                else:
                                    sku_code = None
                                    sku_short_name = unit_val.sku_short_name
                                    sele_week_obj.company = "unit_value.company"
                                category_data = WdSkuCatagory.objects.filter(
                                    wd_town_id=town_id, sku_id=week_sale['sku_id']).last()

                                if category_data:
                                    sele_week_obj.cnf_id = category_data.cnf_id
                                    unit_val = category_data.last_price
                                else:
                                    sele_week_obj.cnf_id = None
                                    unit_val = 0
                                wdregion = User.objects.filter(
                                    user_id=week_sale['wd_id']).last()
                                region = BranchMaster.objects.filter(
                                    branch_code=wdregion.locationcode).last()
                                sele_week_obj.sku_code = sku_code
                                sele_week_obj.sku_short_name = sku_short_name
                                sele_week_obj.region = region.region
                                sele_week_obj.unit_price = unit_val
                                sele_week_obj.value = sele_week_obj.grand_total * sele_week_obj.unit_price
                                sele_week_obj.distrcode = str(
                                    week_sale['wd_id'])+"-"+str(week_sale['town_code'])

                                sele_week_obj.save()
        except Exception as e:
                from django.core.mail import EmailMessage
                error = getattr(e, 'message', repr(e))
                logger.error(error)
                context = {'status': False,'message':'Something Went Wrong'}
                subject = "UAT-Weekly Update Scheduller"
                recipient_list = ['rasmis@triazinesoft.com']
                cc_email = ['rasmis@triazinesoft.com']
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
                return Response(context, status=status.HTTP_200_OK)

class Gets_sales(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            
            # print("--------hiiii-------")
            wd_id = request.GET.get('wd_id', None)
            

            base64_bytes = wd_id.encode("ascii")
            sample_string_bytes = base64.b64decode(base64_bytes)
            sample_string = sample_string_bytes.decode("ascii")
            wd_id = sample_string.split("_")[0]
            # print(wd_id)
            
            
            town_id = request.GET.get('town_id', None)
            base64_bytes = town_id.encode("ascii")
            sample_string_bytes = base64.b64decode(base64_bytes)
            sample_string = sample_string_bytes.decode("ascii")
            town_id = sample_string.split("_")[0]
            town_id = [town_id,str(town_id)[1:],"0"+str(town_id)]
            # print(town_id,"===================")
            # breakpoint()

            category = request.GET.get('category', None)
            date_f = str(request.GET.get('date', datetime.datetime.now().date()))
            
            
            # print("$%%%%%%%%%%%%%%%%%%%%%$$$$$$$$$$$$$$$",wd_id,town_id,category,date_f)

            week_num = request.GET.get('weekly', None)

            user_type = request.user.user_type
            # print(utils.now_date, "==========now_date=======")
            today_date = datetime.datetime.now()
            # today_date = utils.now_date
            last_date = today_date + \
                dateutil.relativedelta.relativedelta(months=-6)

            till_date = datetime.datetime(2009, 10, 5, 14, 59, 59)
            till_date.time()
            Sku_Serializer = []
            status_data = []
            status_data_val = {}
            if date_f:
                # frontend date str conv. to date format
                get_date = datetime.datetime.strptime(
                    date_f, "%Y-%m-%d").date()
                comb_d_t = datetime.datetime.combine(today_date.date(
                ), till_date.time())-timedelta(days=1)  # minus 1 day from current date
            # else:
            #     None
            # day_list=[7,8,14,15,21,22,28,29,30,31,1]
            day_list = [7, 8, 10, 11, 21, 22, 28, 29, 30, 31, 1]

            a = str(today_date.date())
            x = int(str(today_date.date()).split('-')[2])
            lis = [1, 2, 3]

            # set weekly================
            last_date_month = datetime.datetime(today_date.date().year, today_date.date(
            ).month, calendar.monthrange(today_date.date().year, today_date.date().month)[1]).date()
            week_4th = [datetime.datetime(
                today_date.date().year, today_date.date().month, 22).date(), last_date_month]

            week_1st_gng = [datetime.datetime(today_date.date().year, today_date.date().month, 1).date(
            ), datetime.datetime(today_date.date().year, today_date.date().month, 7).date()]
            week_2nd_gng = [datetime.datetime(today_date.date().year, today_date.date().month, 8).date(
            ), datetime.datetime(today_date.date().year, today_date.date().month, 14).date()]
            week_3rd_gng = [datetime.datetime(today_date.date().year, today_date.date().month, 15).date(
            ), datetime.datetime(today_date.date().year, today_date.date().month, 21).date()]
            last_date_month = datetime.datetime(today_date.date().year, today_date.date(
            ).month, calendar.monthrange(today_date.date().year, today_date.date().month)[1]).date()
            # week_4th = [datetime.datetime(today_date.date().year, int(today_date.date().month)-1, 22), week_1st_gng[0] - datetime.timedelta(days=1)]
            week_4th = [datetime.datetime(
                today_date.date().year, today_date.date().month, 22), last_date_month]
            if x in lis and week_4th[0].date() <= get_date <= week_4th[1]:
                # print("hiiii4")
                week_rng = week_4th
            elif week_2nd_gng[0] <= get_date <= week_2nd_gng[1]:
                # print("hiiii2","=======",get_date)
                week_rng = week_2nd_gng
            elif week_3rd_gng[0] <= get_date <= week_3rd_gng[1]:
                # print("hiiii3")
                week_rng = week_4th
            elif week_1st_gng[0] <= get_date <= week_1st_gng[1]:
                # print("hiiii")
                week_rng = week_1st_gng
            else:
                week_rng = None
            # print(week_4th,"====",x,"=====",week_rng)
            # print(week_4th[0].date() ,">= ",get_date ,"<=",week_4th[1])
            week_details = week_sele_before_date(request.user.user_type)
            # print(date_f,"===============================date_f================",get_date < week_details[2][1])
            # print(week_details,"==================>>>>>>>>>>>>", request.user.user_type)
            # breakpoint()
            # return Response({"okk":"======"})
            global_freeze = ''
            list1 = [1, 2, 3, 4, 5, 6, 7]
            list2 = [8, 9, 10, 11, 12, 13, 14]
            list3 = [15, 16, 17, 18, 19, 20, 21]
            list4 = [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 1, 2]
            li = [1, 2]

            StartDate = date_f
            Date = datetime.datetime.strptime(StartDate, "%Y-%m-%d")
            till_date = datetime.datetime(2009, 10, 5, 14, 59, 59)
            till_date.time()
            comb_d_t = datetime.datetime.combine(
                Date.date(), till_date.time())+timedelta(days=1)
            now_current = today_date

            dates = datetime.datetime.strptime(str(date_f), "%Y-%m-%d").date()

            date = dates+datetime.timedelta(days=1)
            combime = datetime.datetime.combine(dates, till_date.time())
            combine_d_t = datetime.datetime.combine(date, till_date.time())
            day_from_date = get_date - datetime.timedelta(days=2)
            beafore_2day = today_date - datetime.timedelta(days=2)

            day_from_date = get_date
            beafore_2day = today_date - datetime.timedelta(days=2)

            not_sales_unfreeze = ""
            not_sales_unfreeze1 = ''
            #>>>> ADMIN section >>>>>> 
            if user_type in ["ADMIN" , "HO"]:
                print(request.user.user_type,"==========================type")
                status_data_val={'freeze_status': True, 'update_status': False, 'lock_status': request.user.lock_unlock}
                month = request.GET.get('month', None)
                year = request.GET.get('year', None)
                week = request.GET.get('week', None)
                if week_num:
                    # freeze_status_val = freeze_status_val_weekly(year, month, transaction_type)
                    sku_serializars_v = adminapiweekly(wd_id, category, town_id, date_f, week_num, month, year, week) 
                    
                    
                    return Response({"message": "Successful", "status_data": [status_data_val], "remarks": Sku_Serializer, "data": sku_serializars_v, 'status': True})
                else:
                    sku_serializars_v = adminapidaily(wd_id,category,town_id,date_f)
                    return Response({"message": "Successful", "status_data": [status_data_val], "remarks": Sku_Serializer, "data": sku_serializars_v, 'status': True})
                
            if user_type == 'WD':
                if week_num is not None:  # WD's Weekly sale==============================
                    if wd_id:
                        wo_4th = [1]

                        wd_town_id_list = Sales_Hierarchy_Master.objects.filter(
                            wd_id=wd_id).values_list('wd_town_id', flat=True)
                        sku_id_list = WdSkuCatagory.objects.filter(status = True,
                            wd_town_id__in=wd_town_id_list).values_list('sku_id', flat=True)
                        topsqu_list = SalesData.objects.filter(sku_id__in=sku_id_list, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time__gte=last_date, brand_category=category, transaction_type=week_num).values_list(
                            'sku_id', flat=True).annotate(sku_totalsale=Sum('grand_total')).order_by('-sku_totalsale')
                        sku_list_top = []
                        sku_id_list3 = list(set(list(sku_id_list)))
                        for i in topsqu_list:
                            if i in sku_id_list3:
                                sku_list_top.append(i)
                                sku_id_list3.remove(i)
                        sku_lists = sku_list_top+sku_id_list3
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
                                Salesobj = SalesData.objects.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time=week_details[
                                                                    2][1], brand_category=category, transaction_type=week_details[1], town_code__in=town_id).values()
                            else:
                                Salesobj = SalesData.objects.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list,
                                                                    sales_date_time=week_details[2][1], transaction_type=week_details[1], town_code__in=town_id).values()

                            if Salesobj:
                                i["SalesData"] = Salesobj

                                if x in day_list:
                                    status_data.append(
                                        {'lock_status': request.user.lock_unlock, "freeze_status": False, "update_status": True})
                                else:
                                    status_data.append(
                                        {'lock_status': request.user.lock_unlock, "freeze_status": True, "update_status": False})

                            else:
                                i["SalesData"] = [{}]

                                if week_details[2] is not None:
                                    not_sales_unfreeze = SalesData.objects.filter((Q(transaction_type__contains="Week")), sales_date_time__gte=week_details[2][0], sales_date_time__lte=week_details[
                                                                                  2][1], sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id, freeze_status=True)
                                    not_sales_unfreeze2 = SalesData.objects.filter(sales_date_time__gte=week_details[2][0], sales_date_time__lte=week_details[
                                                                                   2][1], wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id, freeze_status=True)
                                    not_sales_unfreeze1 = SalesData.objects.filter(
                                        sales_date_time__gte=week_details[2][0], sales_date_time__lte=week_details[2][1], wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id)
                                if not_sales_unfreeze2 and not_sales_unfreeze1:
                                    if len(not_sales_unfreeze2) == len(not_sales_unfreeze1):
                                        global_freeze = True
                                elif x in day_list:
                                    status_data.append(
                                        {'lock_status': request.user.lock_unlock, "freeze_status": False, "update_status": True})
                                else:
                                    status_data.append(
                                        {'lock_status': request.user.lock_unlock, "freeze_status": True, "update_status": False})

                # WD side daily get sales data===========================
                else:
                    if wd_id:
                        wd_town_id_list = Sales_Hierarchy_Master.objects.filter(
                            wd_id=wd_id, town_code__in=town_id).values_list('wd_town_id', flat=True)
                        sku_id_list = WdSkuCatagory.objects.filter(status = True,
                            wd_town_id__in=wd_town_id_list).values_list('sku_id', flat=True)
                        topsqu_list = SalesData.objects.filter(sku_id__in=sku_id_list, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, sales_date_time__gte=last_date, transaction_type="DAILY").values_list(
                            'sku_id', flat=True).annotate(sku_totalsale=Sum('grand_total')).order_by('-sku_totalsale')
                        sku_list_top = []
                        sku_id_list3 = list(set(list(sku_id_list)))
                        for i in topsqu_list:
                            if i in sku_id_list3:
                                sku_list_top.append(i)
                                sku_id_list3.remove(i)
                        sku_lists = sku_list_top+sku_id_list3
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

                                Salesobj = SalesData.objects.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list,
                                                                    brand_category=category, sales_date_time=date_f, transaction_type="DAILY", town_code__in=town_id).values()
                            else:
                                Salesobj = SalesData.objects.filter(
                                    sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time=date_f, transaction_type="DAILY", town_code__in=town_id).values()
                            i["SalesData"] = Salesobj
                            till_date.time()

                            cont_list = [8, 15, 22, 1]
                            a = str(today_date.date())
                            x = a.split('-')
                            date = int(x[2])

                            if Salesobj:

                                i["SalesData"] = Salesobj
                                # Salesobjs = SalesData.objects.filter(sku_id=sku_id,wd_id=wd_id,town_id__in=wd_town_id_list).last()
                                Salesobjs = SalesData.objects.filter(
                                    sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list).last()
                                str_date = Salesobj[0]['sales_date_time']
                                dates = datetime.datetime.strptime(
                                    str(str_date), "%Y-%m-%d").date()
                                user_lock_unlock = User.objects.filter(
                                    user_id=Salesobjs.wd_id).last()

                                date = dates+datetime.timedelta(days=1)
                                combime = datetime.datetime.combine(
                                    dates, till_date.time())
                                combine_d_t = datetime.datetime.combine(
                                    date, till_date.time())
                                day_from_date = get_date - \
                                    datetime.timedelta(days=2)
                                beafore_2day = today_date - \
                                    datetime.timedelta(days=2)

                                if get_date.strftime("%A") == "Saturday" and today_date.time() <= till_date.time() and beafore_2day.date() == get_date:
                                    status_data.append(
                                        {"update_status": True, "user_lock_unlock": request.user.lock_unlock})
                                elif combime <= combine_d_t and combine_d_t > today_date:
                                    status_data.append(
                                        {"update_status": True, "user_lock_unlock": user_lock_unlock.lock_unlock})

                                else:
                                    status_data = [
                                        {'update_status': False, "user_lock_unlock": user_lock_unlock.lock_unlock}]

                            else:
                                i["SalesData"] = [{}]
                                StartDate = date_f
                                Date = datetime.datetime.strptime(
                                    StartDate, "%Y-%m-%d")
                                till_date = datetime.datetime(
                                    2009, 10, 5, 14, 59, 59)
                                till_date.time()
                                comb_d_t = datetime.datetime.combine(
                                    Date.date(), till_date.time())+timedelta(days=1)
                                now_current = today_date

                                day_from_date = get_date
                                beafore_2day = today_date - \
                                    datetime.timedelta(days=2)

                                # print(now_current,"<=",comb_d_t,"======",today_date.date(),get_date)
                                # print("===================",now_current<=comb_d_t , today_date.date()>=get_date)
                                if get_date.strftime("%A") == "Saturday" and today_date.time() <= till_date.time() and beafore_2day.date() == get_date:
                                    status_data.append(
                                        {"update_status": True, "user_lock_unlock": request.user.lock_unlock})
                                elif now_current <= comb_d_t and today_date.date() >= get_date:
                                    status_data.append(
                                        {'update_status': True, "user_lock_unlock": request.user.lock_unlock})
                                else:
                                    status_data.append(
                                        {'update_status': False, "user_lock_unlock": request.user.lock_unlock})

            if user_type == 'BRANCH USER':

                a = date_f
                x = a.split('-')
                date = int(x[2])
                now_day = str(today_date.date())
                splited = now_day.split('-')

                now_date = today_date.date()
                # now_day=str(today_date.date())
                splited = now_day.split('-')

                list1 = [1, 2, 3, 4, 5, 6, 7]
                list2 = [8, 9, 10, 11, 12, 13, 14]
                list3 = [15, 16, 17, 18, 19, 20, 21]
                list4 = [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 1, 2]
                li = [1, 2]

                str_date = str(datetime.datetime(today_date.date(
                ).year, today_date.date().month, 1).date()-datetime.timedelta(days=10))
                get_22th = datetime.datetime(today_date.date().year, today_date.date(
                ).month, 1).date()-datetime.timedelta(days=10)
                get_2nd = datetime.datetime(today_date.date().year, today_date.date(
                ).month, 1).date()+datetime.timedelta(days=1)
                splt = str_date.split('-')
                global_freeze = ''
                print("------------------------------------------------------")

                if week_num is not None:  # this will exicute for BRANCH_USER Weekly data
                    month = request.GET.get('month', None)
                    year = request.GET.get('year', None)
                    week = request.GET.get('week', None)
                    
                    wd_town_id_list = Sales_Hierarchy_Master.objects.filter(wd_id=wd_id).values_list('wd_town_id', flat=True)
                    till_date = date_f
                    unique_top_sku_li = top_sku_sales(wd_id,category,wd_town_id_list,last_date,till_date)
                    transaction_type = week                    
                    sale_data = branch_user_weekly(unique_top_sku_li,wd_id,town_id,wd_town_id_list,category,transaction_type,month,year)
                    
                    # sku_serializars_v = sale_data
                    sku_serializars_v = sale_data[0]
                    Sku_Serializer = sku_remark(wd_id,date_f) if sku_remark(wd_id,date_f) else []
                    # status_data_val = {'freeze_status': True, 'update_status': False}
                    # print
                    status_data_val = {'freeze_status': sale_data[1], 'update_status': False if sale_data[1] == True else True}
                    # print(sale_data,"====================hiiiii")
                    return Response({"message": "Successful=======", "status_data": [status_data_val], "remarks": Sku_Serializer, "data": sku_serializars_v, 'status': True})

                else:  # this will exicute for BRANCH_USER Weekly data========================
                    if wd_id:
                        previus_day = now_date.replace(day=1) - datetime.timedelta(days=1)
                        prev_week_4th = datetime.datetime(previus_day.year, previus_day.month, 22).date()
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

                                Salesobj = SalesData.objects.filter(sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list,
                                                                    brand_category=category, sales_date_time=date_f, transaction_type="DAILY", town_code__in=town_id).values()
                            else:
                                Salesobj = SalesData.objects.filter(
                                    sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, sales_date_time=date_f, transaction_type="DAILY", town_code__in=town_id).values()
                            print(Salesobj,"=====",category,date_f,wd_id,wd_town_id_list,town_id,sku_id)
                            if Salesobj:

                                i["SalesData"] = Salesobj

                                list1 = [1, 2, 3, 4, 5, 6, 7]
                                list2 = [8, 9, 10, 11, 12, 13, 14]
                                list3 = [15, 16, 17, 18, 19, 20, 21]
                                list4 = [22, 23, 24, 25, 26,
                                         27, 28, 29, 30, 31, 1, 2, 3]
                                li = [1, 2]

                                freeze_obj = SalesData.objects.filter(
                                    sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, sales_date_time=date_f, transaction_type="DAILY", freeze_status=0)
                                if int(splited[2]) in list4 and (get_date >= week_4th[0].date() or get_date >= prev_week_4th) and get_date <= now_date:
                                    if freeze_obj:
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                    else:
                                        status_data.append(
                                            {"freeze_status": True, "update_status": False})

                                elif 1 <= date <= 10 and int(splited[2]) <= 10 and get_date <= now_date and int(today_date.date().year) == int(x[0]) and int(today_date.date().month) == int(x[1]):
                                    if freeze_obj:
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                    else:
                                        status_data.append(
                                            {"freeze_status": True, "update_status": False})

                                elif 8 <= date <= 17 and int(splited[2]) <= 17 and get_date <= now_date and int(today_date.date().year) == int(x[0]) and int(today_date.date().month) == int(x[1]):
                                    if freeze_obj:
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                    else:
                                        status_data.append(
                                            {"freeze_status": True, "update_status": False})

                                elif 15 <= date <= 23 and int(splited[2]) <= 23 and get_date <= now_date and int(today_date.date().year) == int(x[0]) and int(today_date.date().month) == int(x[1]):
                                    if freeze_obj:
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                    else:
                                        status_data.append(
                                            {"freeze_status": True, "update_status": False})

                                else:
                                    status_data.append(
                                        {"freeze_status": True, "update_status": False})

                            else:
                                not_sales_unfreeze2 = None
                                not_sales_unfreeze1 = None
                                not_sales_unfreeze = ''
                                i["SalesData"] = [{}]
                                print(week_4th[0].date(),"==================>>>")
                                # breakpoint()
                                if week_details[2] is not None and get_date < week_details[2][1]:
                                    not_sales_unfreeze = SalesData.objects.filter((Q(transaction_type__contains=week_details[1])), sales_date_time__gte=str(week_details[2][0]), sales_date_time__lte=str(
                                        week_details[2][1]), sku_id=sku_id, wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id, freeze_status=True)
                                #     not_sales_unfreeze2 = SalesData.objects.filter(sales_date_time__gte = week_rng[0] ,sales_date_time__lte = week_rng[1],wd_id=wd_id,town_id__in=wd_town_id_list,brand_category=category,town_code = town_id,freeze_status = True)
                                #     not_sales_unfreeze1 = SalesData.objects.filter(sales_date_time__gte = week_rng[0] ,sales_date_time__lte = week_rng[1],wd_id=wd_id,town_id__in=wd_town_id_list,brand_category=category,town_code = town_id)
                                # # print(not_sales_unfreeze2)
                                # if not_sales_unfreeze2 and not_sales_unfreeze1:
                                #     if len(not_sales_unfreeze2) == len(not_sales_unfreeze1):
                                #         global_freeze = True

                                list1 = [1, 2, 3, 4, 5, 6, 7]
                                list2 = [8, 9, 10, 11, 12, 13, 14]
                                list3 = [15, 16, 17, 18, 19, 20, 21]
                                list4 = [22, 23, 24, 25, 26,
                                         27, 28, 29, 30, 31, 1, 2, 3]
                                li = [1, 2]

                                if not_sales_unfreeze:
                                    status_data.append(
                                        {"freeze_status": True, "update_status": False})
                                    i["SalesData"] = [{"freeze_status": True}]
                                else:
                                    ## Remove week_details[2] 28-07-22
                                    if int(splited[2]) in list4 and (get_date >= week_4th[0].date() or get_date >= prev_week_4th) and get_date <= now_date:
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                        i["SalesData"] = [
                                            {"freeze_status": False}]

                                    elif 1 <= date <= 10 and int(splited[2]) <= 10 and get_date <= now_date and int(today_date.date().year) == int(x[0]) and int(today_date.date().month) == int(x[1]):
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                        i["SalesData"] = [
                                            {"freeze_status": False}]

                                    elif 8 <= date <= 17 and int(splited[2]) <= 17 and get_date <= now_date and int(today_date.date().year) == int(x[0]) and int(today_date.date().month) == int(x[1]):
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                        i["SalesData"] = [
                                            {"freeze_status": False}]

                                    elif 15 <= date <= 23 and int(splited[2]) <= 23 and get_date <= now_date and int(today_date.date().year) == int(x[0]) and int(today_date.date().month) == int(x[1]):
                                        status_data.append(
                                            {"freeze_status": False, "update_status": True})
                                        i["SalesData"] = [
                                            {"freeze_status": False}]

                                    else:
                                        status_data.append(
                                            {"freeze_status": True, "update_status": False})
                                        i["SalesData"] = [
                                            {"freeze_status": True}]
            status_data_val = None
            not_sales_unfreez = None
            not_sales_unfreeze_len = None
            no_recore = {}
            seeze_count = 0

            print(week_num,"======================")
            # This line for WD and brench_user also for Weekly data
            if week_details[2] is not None and week_num:
                not_sales_unfreez = SalesData.objects.filter(
                    sales_date_time=week_details[2][1], transaction_type=week_details[1], wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id).all()
                print(not_sales_unfreez, "=========vv1=======", not_sales_unfreez)
                if not_sales_unfreez:
                    not_sales_unfreeze_len = len(not_sales_unfreez)

            # This line for WD and brench_user also for daily data
            elif week_details[2] is not None and (not week_num):
                print(not_sales_unfreez, "=========vv2=======", not_sales_unfreez)

                not_sales_unfreez = SalesData.objects.filter(
                    sales_date_time=week_details[2][1], transaction_type=week_details[1], wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id).all()
                if not_sales_unfreez:
                    not_sales_unfreeze_len = len(not_sales_unfreez)

            elif request.user.user_type == "BRANCH USER" and (not week_num):
    
                if week_details[2] is not None:
                    print(not_sales_unfreez,
                          "=========vv3=======", not_sales_unfreez)
                    if week_details[2][0] <= get_date <= week_details[2][1]:
                        not_sales_unfreez = SalesData.objects.filter(sales_date_time__lte=week_details[2][1], transaction_type=week_details[
                                                                     1], wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id, freeze_status=False).count()

            elif request.user.user_type == "WD" and (not week_num):
                if week_details[2] is not None:
                    print(not_sales_unfreez,
                          "=========vv4=======", not_sales_unfreez)
                    if date_f < week_details[2][1]:
                        not_sales_unfreez = SalesData.objects.filter(sales_date_time__lte=week_details[2][1], transaction_type=week_details[
                                                                     1], wd_id=wd_id, town_id__in=wd_town_id_list, brand_category=category, town_code__in=town_id, freeze_status=False).count()

            # for i in status_data:

            if request.user.user_type == "WD" and (not week_num):
                if week_details[2] is not None:
                    if week_details[2][0] <= get_date <= week_details[2][1]:
                        if not_sales_unfreez == 0 or (not (combime <= combine_d_t and combine_d_t > today_date)):
                            if get_date.strftime("%A") == "Saturday" and today_date.time() <= till_date.time() and beafore_2day.date() == get_date:
                                status_data_val = {"update_status": True, "user_lock_unlock": request.user.lock_unlock}
                                # status_data.append(
                                #     {"update_status": True, "user_lock_unlock": request.user.lock_unlock})
                            else:
                                status_data_val = {
                                    'freeze_status': True, 'update_status': False, 'user_lock_unlock': request.user.lock_unlock}
                        elif now_current <= comb_d_t and today_date.date() >= get_date:
                            status_data_val = {"update_status": True, "user_lock_unlock": request.user.lock_unlock}
                            status_data.append(
                                {'update_status': True, "user_lock_unlock": request.user.lock_unlock})
                        else:
                            status_data.append(
                                {'update_status': False, "user_lock_unlock": request.user.lock_unlock})
                    elif week_details[2][0] > get_date:
                        status_data_val = {
                            'freeze_status': True, 'update_status': False, 'user_lock_unlock': request.user.lock_unlock}
                    elif today_date.date() < get_date:
                        status_data_val = {
                            'freeze_status': True, 'update_status': False, 'user_lock_unlock': request.user.lock_unlock}
                    else:
                        status_data_val = {
                            'freeze_status': False, 'update_status': True, 'user_lock_unlock': request.user.lock_unlock}
                else:
                    try:
                        status_data_val = status_data[0]
                    except Exception as e:
                        status_data_val = {}

                # ===================
            elif request.user.user_type == "WD" and week_num:
                # status_data_val = status_data[0]
                if not_sales_unfreez:
                    seeze_count = 0
                    for row in not_sales_unfreez:
                        if row.freeze_status == True:
                            seeze_count = seeze_count + 1
                    if seeze_count == not_sales_unfreeze_len:
                        status_data_val = {
                            'freeze_status': True, 'update_status': False, 'user_lock_unlock': request.user.lock_unlock}
                    else:
                        status_data_val = {
                            'freeze_status': False, 'update_status': True, 'user_lock_unlock': request.user.lock_unlock}
                else:
                    status_data_val = {
                        'freeze_status': False, 'update_status': True, 'user_lock_unlock': request.user.lock_unlock}

            elif request.user.user_type == "BRANCH USER" and (not week_num):
                if week_details[2] is not None:
                    if week_details[2][0] <= get_date <= week_details[2][1]:
                        not_sales_unfreeze_len = len(not_sales_unfreez)
                        seeze_count = 0
                        if not_sales_unfreez:
                            for row in not_sales_unfreez:
                                if row.freeze_status == True:
                                    seeze_count = seeze_count + 1
                            if seeze_count == not_sales_unfreeze_len:
                                status_data_val = {
                                    'freeze_status': True, 'update_status': False}
                            else:
                                status_data_val = {
                                    'freeze_status': False, 'update_status': True}
                        else:
                            status_data_val = {
                                'freeze_status': False, 'update_status': True}
                    elif week_details[2][0] > get_date or get_date > today_date.date():
                        status_data_val = {
                            'freeze_status': True, 'update_status': False}
                    else:
                        status_data_val = {
                            'freeze_status': False, 'update_status': True}
                else:
                    try:
                        status_data_val = status_data[0]
                    except Exception as e:
                        status_data_val = no_recore

            else:  # this condition will exicute branch_user with Weekly condition
                if not_sales_unfreez:
                    seeze_count = 0
                    for row in not_sales_unfreez:
                        if row.freeze_status == True:
                            seeze_count = seeze_count + 1
                    if seeze_count == not_sales_unfreeze_len:
                        status_data_val = {
                            'freeze_status': True, 'update_status': False}
                    else:
                        status_data_val = {
                            'freeze_status': False, 'update_status': True}
                else:
                    status_data_val = {
                        'freeze_status': False, 'update_status': True}

            # print(status_data_val)
            # if wd_id:
            #     if week_num:
            #         pass
            #     else:
            #         skuremark_obj = Sku_remarks.objects.filter(
            #             wd_id=wd_id, sales_date_time=date_f)

            #         if skuremark_obj:
            #             remark = Sku_remarksSerializer(
            #                 skuremark_obj, many=True).data
            #             Sku_Serializer.append(remark)
            #         else:
            #             Sku_Serializer
            Sku_Serializer = sku_remark(wd_id,date_f)
            print(week_details[2][1]==parse(date_f).date(),"------------kk",date_f)
            if request.user.user_type == "WD" and week_details[1]:
                start_time = datetime.datetime(2009, 10, 5, 0, 0, 1)
                combine_0_time = datetime.datetime.combine(week_details[2][1], start_time.time())
                combine_3pm_time = datetime.datetime.combine(week_details[2][1] + datetime.timedelta(days=2), till_date.time())
                print(week_details, combine_0_time,combine_3pm_time,"======ll",date_f)
                if combine_0_time <=today_date <= combine_3pm_time and week_details[2][1]== parse(date_f).date():
                    status_data_val = {'freeze_status': False, 'update_status': True, 'user_lock_unlock': request.user.lock_unlock}
            return Response({"message": "Successful", "status_data": [status_data_val], "remarks": Sku_Serializer, "data": sku_serializars_v, 'status': True})
        
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)

import pandas as pd
class Gets_sales_new(APIView):
    def get(self, request):
        try:
            request_user = request.user
            wd_id = request.GET.get('wd_id', None)
            town_id = request.GET.get('town_id', None)
            
            wd_id = base64_decode(wd_id)
            town_id = base64_decode(town_id)
            # print(town_id,"===================")
            # breakpoint()
            today_date = datetime.datetime.now()
            category = request.GET.get('category', None)
            sale_date = str(request.GET.get('date', datetime.datetime.now().date()))
            last_date = today_date + dateutil.relativedelta.relativedelta(months=-6)
            print(type(parse(sale_date).date()),"<=",type(today_date.date()))
            if not (parse(sale_date).date() <= today_date.date()):
                context = {'status': False,'message':"You can only select back date"}
                return Response(context, status=status.HTTP_200_OK)

            week_num = request.GET.get('weekly', None)
            transaction_type = "DAILY" if not week_num else week_num

            # till_date = datetime.datetime(2009, 10, 5, 15, 00, 00)
            # print(transaction_type == "DAILY" and parse(sale_date).date() == today_date.date() and today_date.time() < till_date.time(),"============")
            # if transaction_type == "DAILY" and parse(sale_date).date() == today_date.date() and today_date.time() < till_date.time():
            #     context = {'status': False,'message':'You can select only last working day sale before 3 PM'}
            #     return Response(context, status=status.HTTP_200_OK)
            
            month = request.GET.get('month', None)
            year = request.GET.get('year', None)
            week = request.GET.get('week', None)
            save_button_satus = editable_status(request_user, transaction_type, month, year, sale_date)
            wd_town_id_list = Sales_Hierarchy_Master.objects.filter(wd_id=wd_id,town_code__in=[town_id,re.sub('\W+','',town_id),str(town_id),str(town_id)[1:],'0'+str(town_id)]).values_list('wd_town_id', flat=True)
            top_sku_sale = top_sku_sales(wd_id,category,wd_town_id_list,last_date,sale_date)
            sku_sequence = [dict(i) for i in top_sku_sale]
            print(sku_sequence,"-----------top_sku_sale")
            
            if request_user.user_type in ['HO', 'ADMIN']:
                save_button_satus={'freeze_status': True, 'update_status': False, 'lock_status': request.user.lock_unlock}
                Sku_Serializer = sku_remark(wd_id,sale_date) if sku_remark(wd_id,sale_date) else []
                
                if transaction_type == 'DAILY':
                    print("===========",'DAILY')
                    start = datetime.datetime.now()
                    # objs=SalesData.objects.all()
                    # sales_objects = objs.filter(wd_id = wd_id,sales_date_time = sale_date, transaction_type = transaction_type)
                    sales_objects = SalesData.objects.filter(wd_id = wd_id,sales_date_time = sale_date, transaction_type = transaction_type,town_code__in=[town_id,re.sub('\W+','',town_id),str(town_id),str(town_id)[1:],'0'+str(town_id)]).values()
                    ex_time = (datetime.datetime.now()-start)
                    print(ex_time,"========ex_time")
                    salesdf = pd.DataFrame.from_records(sales_objects)
                    sku_sales_obj_serializer = sale_data_obj_with_sequence(sku_sequence,salesdf, sales_objects)
                    # sku_sales_obj_serializer = SalesSerializer(sku_sequence,many = True,context = {'wd_id': wd_id,'sale_date':sale_date,'sales_objects':sales_objects,'town_id_list': wd_town_id_list})
                    
                else:
                    print("===========",'Weekly')
                    sales_objects = SalesData.objects.filter(wd_id = wd_id, sales_date_time__month = month, sales_date_time__year = year, transaction_type = transaction_type,town_code__in=[town_id,re.sub('\W+','',town_id),str(town_id),str(town_id)[1:],'0'+str(town_id)]).values()
                    salesdf = pd.DataFrame.from_records(sales_objects)
                    sku_sales_obj_serializer = sale_data_obj_with_sequence(sku_sequence,salesdf, sales_objects)
                    # sku_sales_obj_serializer = SalesSerializer(sku_sequence,many = True,context = {'wd_id': wd_id,'sale_date':sale_date,'sales_objects':sales_objects,'town_id_list': wd_town_id_list})
                return Response({"message": "Successful", "status_data": [save_button_satus], "remarks": Sku_Serializer, "data": sku_sales_obj_serializer, 'status': True})
                    # sku_serializars_v = adminapidaily(wd_id,category,town_id,sale_date)
                    
                    
                    
            elif request_user.user_type == "WD":
                Sku_Serializer = sku_remark(wd_id,sale_date) if sku_remark(wd_id,sale_date) else []
                if transaction_type == 'DAILY':
                    print("===========",'DAILY')
                    user_type = "WD"
                    weekly_sale = 'daily'
                    freeze_status = save_button_satus['freeze_status']
                    start = datetime.datetime.now()
                    sales_objects = SalesData.objects.filter(wd_id = wd_id,sales_date_time = sale_date, transaction_type = transaction_type,town_code__in=[town_id,re.sub('\W+','',town_id),str(town_id),str(town_id)[1:],'0'+str(town_id)]).values()
                    ex_time = (datetime.datetime.now()-start)
                    # print(ex_time,"========ex_time")
                    salesdf = pd.DataFrame.from_records(sales_objects)
                    print(salesdf,"================sales_objects--------view")
                    sku_sales_obj_serializer = sale_data_obj_with_sequence(sku_sequence, salesdf, sales_objects, user_type, weekly_sale,freeze_status)
                    # sku_sales_obj_serializer = SalesSerializer(sku_sequence,many = True,context = {'wd_id': wd_id,'sale_date':sale_date,'sales_objects':sales_objects,'town_id_list': wd_town_id_list})
                    
                else:
                    user_type = "WD"
                    weekly_sale = 'Weekly'
                    freeze_status = save_button_satus['freeze_status']
                    print("===========",'Weekly')
                    week_value = week_sele_before_date('WD')
                    sales_objects = SalesData.objects.filter(wd_id = wd_id, sales_date_time = week_value[2][1], transaction_type = transaction_type, town_code__in=[town_id,re.sub('\W+','',town_id),str(town_id),str(town_id)[1:],'0'+str(town_id)]).values()
                    salesdf = pd.DataFrame.from_records(sales_objects)
                    sku_sales_obj_serializer = sale_data_obj_with_sequence(sku_sequence, salesdf, sales_objects, user_type, weekly_sale,freeze_status)
                    # sku_sales_obj_serializer = SalesSerializer(sku_sequence,many = True,context = {'wd_id': wd_id,'sale_date':sale_date,'sales_objects':sales_objects,'town_id_list': wd_town_id_list})
                return Response({"message": "Successful", "status_data": [save_button_satus], "remarks": Sku_Serializer, "data": sku_sales_obj_serializer, 'status': True})
            
            
            
            elif request_user.user_type == "BRANCH USER":
                print("-----fff----lkj")
                Sku_Serializer = sku_remark(wd_id,sale_date) if sku_remark(wd_id,sale_date) else []
                if transaction_type == 'DAILY':
                    user_type = "BRANCH USER"
                    weekly_sale = 'daily'
                    freeze_status = save_button_satus['freeze_status']
                    print("=====111======",'DAILY')
                    sales_objects = SalesData.objects.filter(wd_id = wd_id,sales_date_time = sale_date, transaction_type = transaction_type,town_code__in=[town_id,re.sub('\W+','',town_id),str(town_id),str(town_id)[1:],'0'+str(town_id)]).values()
                    salesdf = pd.DataFrame.from_records(sales_objects)
                    sku_sales_obj_serializer = sale_data_obj_with_sequence(sku_sequence, salesdf, sales_objects, user_type, weekly_sale,freeze_status)
                    # sku_sales_obj_serializer = sale_data_obj_with_sequence(sku_sequence,salesdf, sales_objects)
                    # # breakpoint()
                    # sku_sales_obj_serializer = SalesSerializer(sku_sequence,many = True,context = {'wd_id': wd_id,'sale_date':sale_date,'sales_objects':sales_objects,'town_id_list': wd_town_id_list})
                    # sku_sales_obj_serializer = sku_sales_obj_serializer.data
                else:
                    user_type = "BRANCH USER"
                    weekly_sale = 'weekly'
                    freeze_status = save_button_satus['freeze_status']
                    print(freeze_status,"----------===========",'Weekly')
                    sales_objects = SalesData.objects.filter(wd_id = wd_id, sales_date_time__month = month, sales_date_time__year = year, transaction_type = transaction_type,town_code__in=[town_id,re.sub('\W+','',town_id),str(town_id),str(town_id)[1:],'0'+str(town_id)]).values()
                    salesdf = pd.DataFrame.from_records(sales_objects)
                    sku_sales_obj_serializer = sale_data_obj_with_sequence(sku_sequence, salesdf, sales_objects, user_type, weekly_sale,freeze_status)
                    # sku_sales_obj_serializer = SalesSerializer(sku_sequence,many = True,context = {'wd_id': wd_id,'sale_date':sale_date,'sales_objects':sales_objects,'town_id_list': wd_town_id_list})
                return Response({"message": "Successful", "status_data": [save_button_satus], "remarks": Sku_Serializer, "data": sku_sales_obj_serializer, 'status': True})
                
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'+str(repr(e))}
            return Response(context, status=status.HTTP_200_OK)
        
class Check_timeing(generics.GenericAPIView):
    serializer_class = SaleSaveUpdateSerializer
    def post(self, request):
        data = request.data
        for i in data:
            sales = SalesData.objects.filter(brand_category = i['brand_category'], wd_id = i['wd_id'], sku_id = i['sku_id'], sales_date_time = i['sales_date_time']).last()
            print(sales,"---------")
            if sales:
                serializer_class = self.serializer_class(sales , data = i, partial = True)
                if serializer_class.is_valid():
                    serializer_class.save()
                else:
                    print(serializer_class.errors,"=========") 
            else :
                print("---------------------------------------99")
                serializer_class = self.serializer_class(data = i)
                if serializer_class.is_valid():
                    serializer_class.save()
                else:
                    print(serializer_class.errors,"==========lll") 
        context = {"message" : "Success.", 'data':'serializer_class.errors'}
        return Response(context, status=status.HTTP_200_OK)
    
from sqlalchemy import create_engine
class Create_Update_Weekly_Sales_temp(generics.ListCreateAPIView):   # temporaryly commented------------
    serializer_class = SaleSaveUpdateSerializer
    
    def get_queryset(self):
        try:
            
            from_date = self.request.query_params.get('from_date', None)
            to_date = self.request.query_params.get('to_date', None)
            week_value = self.request.query_params.get('week_value', None)
            transaction_value_li = ["Week1","Week2","Week3","Week4"]
            wd_id = self.request.query_params.get('wd_id', None)
            if from_date and to_date and week_value :
                print("---------->>",from_date,to_date,week_value)
                if week_value in transaction_value_li:
                    help_week = [0,week_value,[from_date,to_date]]
                
            else:
                help_week = week_sele_before_date("BRANCH USER")
                if not help_week[1]:
                    print("------<<-")
                    return WdSkuCatagory.objects.none()
            # breakpoint()
            today = datetime.datetime.now()
            sales_hierarchy_master = Sales_Hierarchy_Master.objects.all().values()
            wd_master = WDmaster.objects.all().values()
            mapping_master = WdSkuCatagory.objects.all().values()
            product_master = SKU_Master_Product.objects.all().values()
            
            sales_hierarchy_master_df = pd.DataFrame(sales_hierarchy_master)
            sales_hierarchy_master_df = sales_hierarchy_master_df.rename({'town':'town_name','wd_town_id':'town_id'}, axis=1)
            sales_hierarchy_master_unique_town_id_df = sales_hierarchy_master_df.groupby(['town_name','wd_id']).tail(1)
            sales_hierarchy_master_unique_town_wd_df = sales_hierarchy_master_df.groupby(['town_name','wd_id','town_id']).tail(1)
            
            # sales_hierarchy_master_unique_town_id_df.to_csv('heirarchy.xls', header=True, index=False)
            # df.drop(columns=['column_nameA', 'column_nameB'])

            # print("------------ll",sales_hierarchy_master_df)
            wd_master_df = pd.DataFrame(wd_master)
            wd_master_df = wd_master_df.rename({'wd_ids':'wd_id','wd_state':'gpi_state',}, axis=1)
            product_master_df = pd.DataFrame(product_master)        
            product_master_df = product_master_df.rename({'category_code':'brand_category'}, axis=1)
            mapping_master_df = pd.DataFrame(mapping_master)
            mapping_master_df = mapping_master_df.rename({'wd_town_id':'town_id','last_price':'unit_price'}, axis=1)
            # print("=================",mapping_master_df,"=========================ngf")
            # mapping_master_df = mapping_master_df.groupby(['town_id','sku_code']).tail(1)
            
            # take town_code as per town_id from heirarchy master =================
            heirarchy_n_mapping_merge = pd.merge(mapping_master_df,sales_hierarchy_master_unique_town_wd_df[['town_id','town_code','town_name']], on = ['town_id'], how='outer')
            # heirarchy_n_mapping_merge = heirarchy_n_mapping_merge.drop_duplicates()
            heirarchy_n_mapping_merge = heirarchy_n_mapping_merge.groupby(['town_id','sku_code','town_code']).tail(1)
            
            
            # print("==========================######===")
            # heirarchy_n_mapping_merge = heirarchy_n_mapping_merge.groupby(['town_id','sku_code']).tail(1)
            print(heirarchy_n_mapping_merge,'-------pp----------')
            week_data_sum = SalesData.objects.filter(transaction_type='DAILY', sales_date_time__gte=help_week[2][0], sales_date_time__lte=help_week[2][1]).values('wd_id', 'sku_id', 'town_code', 'sku_code').annotate(Sum('local_sales_retail'),
                                                            Sum('local_sales_dealer'), Sum('local_sales_modern_trade'), Sum('local_sales_hawker'), Sum('total_local_sales'), Sum('outstation_sales_reatil'),
                                                            Sum('outstation_sales_dealer'), Sum('outstation_sales_modern_trade'), Sum('outstation_sales_hawker'), Sum('total_outstation_sales'), Sum('other_sales_retail'), Sum('other_sales_dealer'),
                                                            Sum('other_sales_modern_trade'), Sum('total_other_sales'), Sum('other_issues_damage'), Sum('other_issues_return'), Sum('other_issues_other'), Sum('total_issue'), Sum('grand_total'), Sum('value'))
            print(len(week_data_sum),"--------------------------------------kk")
            # breakpoint()
            if week_data_sum:
                weekly_sales_df = pd.DataFrame(week_data_sum)
                weekly_sales_df = pd.merge(weekly_sales_df,wd_master_df[['wd_id','wd_type','wd_name','gpi_state']], on=['wd_id'],how='outer',suffixes = ('_left', '_right'))
                # weekly_sales_df = pd.merge(weekly_sales_df, sales_hierarchy_master_df[['wd_id','town_code','town_name','region']], on=['wd_id','town_code'], how='outer', suffixes = ('_left', '_right'))
                weekly_sales_df = pd.merge(weekly_sales_df, sales_hierarchy_master_unique_town_id_df[['wd_id','town_code','town_name','town_id','region']], on=['wd_id','town_code'], how='outer', suffixes = ('_left', '_right'))
                weekly_sales_df = pd.merge(weekly_sales_df, product_master_df[['sku_code','sku_id','sku_short_name','brand_category','company']], on=['sku_code','sku_id'], how='outer', suffixes = ('_left', '_right'))
                weekly_sales_df = pd.merge(weekly_sales_df, heirarchy_n_mapping_merge[['sku_id','sku_code','cnf_id','unit_price','town_name']], on=['sku_id','sku_code','town_name'], how='outer', suffixes = ('_left', '_right'))
                weekly_sales_df['transaction_type'] = help_week[1]
                weekly_sales_df['sales_date_time'] = help_week[2][1]
                weekly_sales_df['created_date'] = datetime.datetime.now()
                weekly_sales_df['created_by'] = "auto scheduler"
                weekly_sales_df['status'] = True
                weekly_sales_df['freeze_status'] = False

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
                
                
                week_data_sum = SalesData.objects.filter(transaction_type = help_week[1], sales_date_time__gte=help_week[2][0], sales_date_time__lte=help_week[2][1]).delete()
                # my_eng = my_eng
                weekly_sales_df_ren = weekly_sales_df_ren[weekly_sales_df_ren['wd_id'].notna()]
                weekly_sales_df_ren = weekly_sales_df_ren[weekly_sales_df_ren['sku_id'].notna()]
                weekly_sales_df_ren = weekly_sales_df_ren[weekly_sales_df_ren['town_name'].notna()]
                weekly_sales_df_ren = weekly_sales_df_ren.drop_duplicates()
                # print(weekly_sales_df_ren,"-----------------weekly_sales_df_ren-----------------")
                # pd.merge(weekly_sales_df)
                # weekly_sales_df_ren.to_csv('file2.xls', header=True, index=False)
                print("-------------",weekly_sales_df,"=========================")
                weekly_sales_df_ren.to_sql('transaction_salesdata', my_eng, if_exists='append', index=False)
                return SalesData.objects.none()
        
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong','error':error}
            # subject = "UAT | SFA/SFA_lite Issue"
            subject = "Create_Update_Weekly_Sales"
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
            today_date = datetime.datetime.now()
            reset_email.send(fail_silently=True)
            # self.get_queryset()
            return Response(context, status=status.HTTP_200_OK)
        
        

class Create_Update_Weekly_Sales(generics.ListCreateAPIView):
    serializer_class = SaleSaveUpdateSerializer
    
    def get_queryset(self):
        try:
            pass
            from_date = self.request.query_params.get('from_date', None)
            to_date = self.request.query_params.get('to_date', None)
            week_value = self.request.query_params.get('week_value', None)
            transaction_value_li = ["Week1","Week2","Week3","Week4"]
            wd_id = self.request.query_params.get('wd_id', None)
        except:
            from_date = None
            to_date = None
            wd_id = None
            week_value = None
        try:
            if from_date and to_date and week_value :
                print("--------------------------->>manual",from_date,to_date,week_value)
                if week_value in transaction_value_li:
                    help_week = [0,week_value,[from_date,to_date]]
                
            else:
                print("-------------------------scheduler")
                help_week = week_sele_before_date("BRANCH USER")
                if not help_week[1]:
                    print("------<<-")
                    return WdSkuCatagory.objects.none()
            # breakpoint()
            today = datetime.datetime.now()
            sales_hierarchy_master = Sales_Hierarchy_Master.objects.all().values('wd_id','wd_town_id','region','town_code','town')
            wd_master = WDmaster.objects.all().values('wd_ids','wd_postal_code','wd_state','wd_type','wd_name')
            mapping_master = WdSkuCatagory.objects.all().values('wd_town_id','sku_code', 'sku_id','cnf_id','last_price')
            product_master = SKU_Master_Product.objects.all().values('sku_id','sku_code','sku_short_name','category_code','company')
            product_master_df = pd.DataFrame(product_master)        
            product_master_df = product_master_df.rename({'category_code':'brand_category'}, axis=1)
            mapping_master_df = pd.DataFrame(mapping_master)
            mapping_master_rename_df = mapping_master_df.rename(columns = {'wd_town_id':'town_id','last_price':'unit_price'})
            sales_hierarchy_master_df = pd.DataFrame(sales_hierarchy_master)
            sales_hierarchy_master_df = sales_hierarchy_master_df.rename({'town':'town_name','wd_town_id':'town_id'}, axis=1)
            sales_hierarchy_master_unique_town_name_df = sales_hierarchy_master_df.drop_duplicates(subset=['town_name'], keep = 'last')
            sales_hierarchy_master_unique_town_id_df = sales_hierarchy_master_df.drop_duplicates(subset=['town_name','town_id'], keep = 'last')
            town_code_town_name = pd.merge(sales_hierarchy_master_unique_town_name_df[['town_name']], sales_hierarchy_master_df[['town_name','town_code']], on =['town_name'], how = 'left')
            sales_hierarchy_unique_town_id_code_name_df = pd.merge(sales_hierarchy_master_unique_town_id_df[['town_name','town_id']], town_code_town_name,  on =['town_name'], how = 'left')
            print(sales_hierarchy_master_unique_town_id_df.columns,"----------------------->>",mapping_master_rename_df.columns)
            mapping_hierarchy_merge_df = pd.merge(mapping_master_rename_df[['town_id','sku_code', 'sku_id','cnf_id','unit_price']],sales_hierarchy_master_unique_town_id_df[['town_name','town_id','region','wd_id']], on = 'town_id', how = 'left')
            


            # print("------------ll",sales_hierarchy_master_df)
            
            # print("------------ll",sales_hierarchy_master_df)
            wd_master_df = pd.DataFrame(wd_master)
            wd_master_df = wd_master_df.rename({'wd_ids':'wd_id','wd_state':'gpi_state'}, axis=1)
            mapping_hierarchy_wd_type_merge_df = pd.merge(mapping_hierarchy_merge_df, wd_master_df[['wd_id','gpi_state','wd_type','wd_name']], on = ['wd_id'], how='left')
            mapping_hierarchy_wd_type_sku_merge_df = pd.merge(mapping_hierarchy_wd_type_merge_df, product_master_df[['sku_id','company','sku_short_name','brand_category']], on = 'sku_id', how = 'left')
            week_data_sum = SalesData.objects.filter(transaction_type='DAILY', sales_date_time__gte=help_week[2][0], sales_date_time__lte=help_week[2][1]).values('wd_id', 'sku_id', 'town_code', 'sku_code','town_name').annotate(Sum('local_sales_retail'),
                                                            Sum('local_sales_dealer'), Sum('local_sales_modern_trade'), Sum('local_sales_hawker'), Sum('total_local_sales'), Sum('outstation_sales_reatil'),
                                                            Sum('outstation_sales_dealer'), Sum('outstation_sales_modern_trade'), Sum('outstation_sales_hawker'), Sum('total_outstation_sales'), Sum('other_sales_retail'), Sum('other_sales_dealer'),
                                                            Sum('other_sales_modern_trade'), Sum('total_other_sales'), Sum('other_issues_damage'), Sum('other_issues_return'), Sum('other_issues_other'), Sum('total_issue'), Sum('grand_total'), Sum('value'))
            if week_data_sum:
                weekly_sales_df = pd.DataFrame(week_data_sum)
                weekly_sales_df = pd.merge(weekly_sales_df, mapping_hierarchy_wd_type_sku_merge_df, on=['wd_id','sku_id','sku_code','town_name'], how='left')
                weekly_sales_df['transaction_type'] = help_week[1]
                weekly_sales_df['sales_date_time'] = help_week[2][1]
                weekly_sales_df['created_date'] = datetime.datetime.now()
                weekly_sales_df['created_by'] = "auto scheduler"
                weekly_sales_df['status'] = True
                weekly_sales_df['freeze_status'] = False
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
                
                week_data_sum = SalesData.objects.filter(transaction_type = help_week[1], sales_date_time__gte=help_week[2][0], sales_date_time__lte=help_week[2][1]).delete()
            weekly_sales_df_ren = weekly_sales_df_ren.drop_duplicates(subset = ['wd_id','town_name','sku_id','sku_code','sales_date_time'], keep = 'last')
            weekly_sales_df_ren.to_sql('transaction_salesdata', my_eng, if_exists='append', index=False)
            print(weekly_sales_df_ren,'---------------------------')
            print(weekly_sales_df_ren.columns,'---------------------------columns')
            
            
            email_from = settings.EMAIL_HOST_USER
            cc_email = cc_list
            # ,'saurabha@triazinesoft.com','mayankg@triazinesoft.com'
            recipient_list = success_email_list
            subject = html_message_weekly
            # recipient_list = ["VIPULSHARMA-gpi@modi-ent.com","ankit.rakwal@esobene.com"]
            html_message = 'Weekly Scheduler has been successfully completed.'
            reset_email = EmailMessage(
                        subject = subject,
                        body = html_message,
                        from_email = email_from,
                        to = recipient_list,
                        cc = cc_email,
                        reply_to = cc_email,
                        )
            reset_email.content_subtype = "html"
            reset_email.send(fail_silently=True)
            return SalesData.objects.none()
           
        
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong','error':error}
            # subject = "UAT | SFA/SFA_lite Issue"
            subject = "Create_Update_Weekly_Sales"
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
            today_date = datetime.datetime.now()
            reset_email.send(fail_silently=True)
            # self.get_queryset()
            return Response(context, status=status.HTTP_200_OK)