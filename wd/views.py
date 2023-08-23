from datetime import timedelta
from functools import partial
from http.client import ImproperConnectionState
import imp
from django.db.models.expressions import Exists
from django.shortcuts import render
from pymysql import NULL
from master.email import weekly_save_notification_mail
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from dateutil import parser                      
from base.models import User
from branch_user.serializers import WDmaster_wd_town
from master.models import SalesData, SKU_Master_Product, Sales_Hierarchy_Master
from master.serializers import *
from wd.utils import daily_weekly_sale_create_update, freeze_status_val_weekly_and_date, sum_weekly_data, daily_sales_data_save
from wd.serializers import *
from rest_framework import status
import calendar
import datetime
import time
from dateutil.relativedelta import relativedelta
from datetime import date
from django.db.models import Sum
from django.db.models import Q
from django.db import transaction
import logging
logger = logging.getLogger(__name__)
from branch_user.views import current_week
from .helper import week_sele_before_date
from master.task import create_weekly_wd_wise
from rest_framework import generics
from django.template.loader import render_to_string
from django.conf import settings
from secondary_sales.settings import my_eng
from itertools import chain

def access_count(wd_id,town_code,user_id,user_type,date):
    user_id=user_id
    wd_id=wd_id
    town_code=town_code
    user_type=user_type

    
    print(">>>>>>>>MMMMMMMMMMMMMMMMMMMMM",user_id,wd_id,town_code,user_type,date)
    

    gpi_states=WDmaster.objects.filter(wd_ids=user_id).last()
    sales_hir=Sales_Hierarchy_Master.objects.filter(wd_id=user_id).last()
    
    # print(datetime.datetime.today())
    access_log=Access_log.objects.filter(user_id=user_id,user_type=user_type,town_code=town_code,sales_save_date=date,created_by=user_id).last()
    if not access_log:
        Access_log.objects.create(user_id=user_id,user_type=user_type,town_code=town_code,sales_save_date=date,created_by=user_id,gpi_state=gpi_states.wd_state,town=sales_hir.town,statename=gpi_states.wd_state)
        print("############## Success")

    # print(">>>>>>>>MMMMMMMMMMMMMMMMMMMMM",user_id,wd_id,town_code,user_type)
    
    
    else:
        att_update=access_log
        att_update.updated_on=datetime.datetime.today()
        att_update.updated_by=user_id
        att_update.count=access_log.count+1
        att_update.save()
        # Attendence.objects.update(updated_on=datetime.datetime.today())
        print("$$$$$$$$$$$$$$$$$$$$$$$$$")



# Create your views here.

# 
class WDtown(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            if request.user.user_type =="WD":
                data = WDmaster.objects.filter(wd_ids = request.user.user_id, status = True)
                serializer = WDmaster_wd_town(data,many = True)
                dict={"status":True,'status_code':200,"data":serializer.data}
                return Response(dict, status=status.HTTP_200_OK)
            else:
                user_name = request.GET.get('user_name',None)
                data = Sales_Hierarchy_Master.objects.filter(wd_id = request.user.user_id).values('wd_town_id','town_code','town','region')[:1]
                
                dict={"status":True,'status_code':200,"data":data}
                return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)

# brand category APIView==================
class BrandCategory(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            # data =SKU_Master_Product.objects.filter(status = True).values('category_name','category_code').distinct()
            data = [{"category_name":"CIGARETTE","category_code":"CIG"},
                    # {"category_name":"PAN MASALA","category_code":"CHP"},
                    # {"category_name":"Silver Coated Elaichi","category_code":"CHS"},
                    {"category_name":"CANDY","category_code":"CDI"}]
            dict={"status":True,'status_code':200,"data":data}
            return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)
        
####################################
# Start new code.
# from wd.utils import now_date

from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
class WDAddSales(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    @csrf_exempt
    def post(self, request):
        try:
            now_dt = datetime.datetime.now()
            # now_dt = now_date
            now_day=str(now_dt.date())
            splited = now_day.split('-')
            till_date = datetime.datetime(2009, 10, 5, 15, 00, 00)
            region = BranchMaster.objects.filter(branch_code=request.user.locationcode).last()
            help_week = week_sele_before_date(request.user.user_type)
            record = request.data
            userid = request.user.id
            location = request.user.locationcode
            wd_id=record[0]['wd_username']
            town_code=record[0]['town_code']
            date=record[0]['sale_date_time']
            category = record[0]['brand_category']
            user_id = request.user.user_id
            user_type=request.user.user_type
            access_count(wd_id,town_code,wd_id,user_type,date)
            
            data_change = daily_sales_data_save(record, userid, location, help_week,user_type)
            if request.user.user_type == "BRANCH USER" and record[0]['week_num']:
                week_date_and_freeze_status = freeze_status_val_weekly_and_date(record[0]['year'], record[0]['month'],record[0]['week_num'])
                if (help_week[2] and (help_week[2][1] > week_date_and_freeze_status[1][1])) or week_date_and_freeze_status:
                    subjects = Subject.objects.filter(use_for__icontains = "save notification").last()
                    email_details = Email_users.objects.filter(is_active = True ,subject = subjects.id)
                    subject = subjects.name
                    recipient_list = email_details.filter(email_to = True).values_list('email',flat=True)
                    cc_email = email_details.filter(email_cc = True).values_list('email',flat=True)
                    branch = BranchMaster.objects.filter(branch_code = request.user.locationcode).last()
                    wd_town = WDmaster.objects.filter(wd_postal_code__icontains = town_code).last()
                    town =  wd_town.wd_postal_code if wd_town else ""
                    updated_data=''
                    month_year = calendar.month_name[(week_date_and_freeze_status[1][1]).month]
                    # lst=[]
                    # for data in data_change:
                    #     temp=[]
                    #     key=list(data.values())[0]
                    #     old_data=data['old_value']
                    #     new_data=data['new_value']
                    #     # print(data,'fsgewygrtfi4uwg4tuy746565rt8i4wtfhgewfyewf78qef')
                    #     temp.append(key)
                    #     temp.append(old_data)
                    #     temp.append(new_data)
                    #     lst.append(temp)
                        #updated_data+="Values: &emsp; "+f"{key}"+"&emsp;"+"&emsp;"+"&emsp;"+f"{old_data}"+"&emsp;"+"&emsp;"+"&emsp;"+"&emsp;"+"&emsp;"+f"{new_data}"+"<br>"
                    print(week_date_and_freeze_status[1][1],'yyyyyyyyyyyyyyyy')    
                    mail_data = Weeklysales_update_log.objects.filter(is_sent = False).values("sku_name","sku_code","sales_type","previous_quantity","new_quantity",)                        
                    html_message = render_to_string('mail/email.html',
                                                    context={'sale_date':week_date_and_freeze_status[1][1],
                                                             #"updated_data":"KEY"+"&emsp; "+"&emsp; "+"&emsp; "+"&emsp; "+"Old Value"+"&emsp; "+"&emsp; "+"&emsp; "+"&emsp; "+"New Value<br>",
                                                             "values":mail_data,
                                                             "month_year":month_year,
                                                            #  "sales_year":"",
                                                              'week':record[0]['week_num'],'wd_id':f"{wd_id}-{town}",'branch':f"{request.user.user_id}-{branch.region}", 'category' : f"{category}"
                                                            })
                    weekly_save_notification_mail(subject,recipient_list,cc_email,html_message)
                    Weeklysales_update_log.objects.update(is_sent = True)
            return Response({'massage': 'Sales data has been saved successfully' ,'status': True,})
            
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)
    

class WD_Total_Sales(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data =  request.data
        try:
            if request.data['transaction_type']:
                transaction_typ = request.data['transaction_type']
            else:
                transaction_typ = "DAILY"
            users = User.objects.filter(user_id = request.data['wd_id'], locationcode = request.user.locationcode)
            if not users:
                return Response({"messsage":"Invalid User", "status":False})
                
            total_data = Total_sku_sales.objects.filter(sale_date = request.data['sale_date'], category = request.data['category'], wd_id = request.data['wd_id'], transaction_type = transaction_typ).last()
            if total_data is None:
                request.data['created_date'] = datetime.datetime.now()
                request.data['transaction_type'] = transaction_typ
                serializer = Total_sku_sales_serializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"messsage":"Success", "status":True, "data":serializer.data})
                else:
                    return Response(serializer.errors)
            else:
                request.data['updated_date'] = datetime.datetime.now()
                request.data['transaction_type'] = transaction_typ
                serializer = Total_sku_sales_serializer(total_data,request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"messsage":"Success", "status":True,"data":serializer.data})
                else:
                    return Response(serializer.errors)
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)

        # return Response({"message":"Success", "status": True})

    def get(self, request):
        sale_date = request.data.get()
        category = request.data.get()
        wd_id = request.data.get()
        transaction_type = request.data.get()

        total_data = Total_sku_sales.objects.filter(sale_date = sale_date, category = category, wd_id = wd_id, transaction_type = transaction_type)
        if total_data:
            serialiser = Total_sku_sales_serializer(data = total_data, many = True)
            return Response({"message":"Success", "status": True, "data":serialiser.data})
        else:
            return Response({"message":"No Record.", "status": False, "data":None})

class Sku_remarks_views(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            skuremark_obj=Sku_remarks.objects.filter(wd_id=request.data.get('wd_id'),sales_date_time=request.data.get('sales_date_time')).last()
            if skuremark_obj:
                serializer = Sku_remarksSerializer(skuremark_obj,data = request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response({'status': False,'data':serializer.errors})
            else:
                serializer = Sku_remarksSerializer(data = request.data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response({'status': False,'data':serializer.errors})
            return Response({'massage': 'Remark has been successfully saved','status': True,'data':serializer.data})
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)




# search filter implimented for search wd form branch_user======
class wd_search(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            search=request.GET.get("search",None)
            if search is not None:
                search=search.strip()
                if self.request.user.user_type == "BRANCH USER":
                    user_obj = User.objects.filter(Q(user_id__icontains=search)|Q(first_name__icontains=search),locationcode = self.request.user.locationcode).exclude(user_type = 'BRANCH USER')
                    print(request.user.user_id,"========",user_obj)
                    # return data
                # user_obj=User.objects.filter(Q(user_id__icontains=search)|Q(first_name__icontains=search))
                    if user_obj:
                        serializer = wd_searchSerializer(user_obj,many=True)
                        list_data={'massage': 'successfully','status': True,"results":serializer.data}
                        return Response(list_data)
                    else:
                        hie_obj=Sales_Hierarchy_Master.objects.filter(town_code__icontains=search).values_list('wd_id',flat=True).distinct()
                        user_obj=User.objects.filter(user_id__in=hie_obj)
                        serializer = wd_searchSerializer(user_obj,many=True)
                        list_data={'massage': 'successfully','status': True,"results":serializer.data}
                        return Response(list_data)
                else:
                    user_obj = User.objects.filter(Q(user_id__icontains=search)|Q(first_name__icontains=search)).exclude(user_type = 'BRANCH USER')
                    print(user_obj,"====kkk")
                    serializer = wd_searchSerializer(user_obj,many=True)
                    list_data={'massage': 'successfully','status': True,"results":serializer.data}
                    return Response(list_data)

            list_data={'massage': 'successfully','status': True,"results":[]}
            return Response(list_data)
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)


class WDAddSales_New(APIView):
        permission_classes = (IsAuthenticated,)
        @csrf_exempt
        def post(self, request):
            try:
                now_dt = datetime.datetime.now()
                # now_dt = now_date
                now_day=str(now_dt.date())
                splited = now_day.split('-')
                till_date = datetime.datetime(2009, 10, 5, 15, 00, 00)
                region = BranchMaster.objects.filter(branch_code=request.user.locationcode).last()
                help_week = week_sele_before_date(request.user.user_type)
                record = request.data
                userid = request.user
                location = request.user.locationcode
                wd_id=record[0]['wd_username']
                town_code=record[0]['town_code']
                date=record[0]['sale_date_time']
                category = record[0]['brand_category']
                inser_status = Apistatus.objects.filter(running_date = now_dt.date(),sfa_bulk_flag=True,api="SFA_API")
                if inser_status:
                    context = {'status': False,'message':'We are synking the SFA data, Please reload the page.'}
                    return Response(context, status=status.HTTP_200_OK)
                
                # if not record[0]['week_num'] and parser.parse(date).date() == now_dt.date() and now_dt.time() < till_date.time():
                #     context = {'status': False,'message':'You can save only last working day sale before 3 PM'}
                #     return Response(context, status=status.HTTP_200_OK)
                
                user_id = request.user.user_id
                user_type=request.user.user_type
                access_count(wd_id,town_code,wd_id,user_type,date)
                db_engine = my_eng
                data_change = daily_weekly_sale_create_update(record, userid, location, help_week,user_type,db_engine)
                print(data_change,"----------------------data_change")
                if request.user.user_type == "BRANCH USER" and record[0]['week_num']:
                    week_date_and_freeze_status = freeze_status_val_weekly_and_date(record[0]['year'], record[0]['month'],record[0]['week_num'])
                    if (help_week[2] and (help_week[2][1] > week_date_and_freeze_status[1][1])) or week_date_and_freeze_status:
                        subjects = Subject.objects.filter(use_for__icontains = "save notification").last()
                        email_details = Email_users.objects.filter(is_active = True ,subject = subjects.id)
                        subject = subjects.name
                        recipient_list = email_details.filter(email_to = True).values_list('email',flat=True)
                        cc_email = email_details.filter(email_cc = True).values_list('email',flat=True)
                        # print("--------------------->>>>>>>>>>>>",[request.user.email])
                        # print("------///----------------------chain=======//",list(recipient_list)+[request.user.email])
                        # recipient_lists = list(recipient_list)+[request.user.email]
                        recipient_lists = recipient_list
                        branch = BranchMaster.objects.filter(branch_code = request.user.locationcode).last()
                        wd_town = WDmaster.objects.filter(wd_postal_code__icontains = town_code).last()
                        town =  wd_town.wd_postal_code if wd_town else ""
                        updated_data=''
                        month_year = calendar.month_name[(week_date_and_freeze_status[1][1]).month]
                        # lst=[]
                        # for data in data_change:
                        #     temp=[]
                        #     key=list(data.values())[0]
                        #     old_data=data['old_value']
                        #     new_data=data['new_value']
                        #     # print(data,'fsgewygrtfi4uwg4tuy746565rt8i4wtfhgewfyewf78qef')
                        #     temp.append(key)
                        #     temp.append(old_data)
                        #     temp.append(new_data)
                        #     lst.append(temp)
                            #updated_data+="Values: &emsp; "+f"{key}"+"&emsp;"+"&emsp;"+"&emsp;"+f"{old_data}"+"&emsp;"+"&emsp;"+"&emsp;"+"&emsp;"+"&emsp;"+f"{new_data}"+"<br>"
                        print(week_date_and_freeze_status[1][1],'yyyyyyyyyyyyyyyy')    
                        mail_data = Weeklysales_update_log.objects.filter(branch_id = request.user.user_id,is_sent = False).values("sku_name","sku_code","sales_type","previous_quantity","new_quantity",)                        
                        if mail_data:
                            html_message = render_to_string('mail/email.html',
                                                            context={'sale_date':week_date_and_freeze_status[1][1],
                                                                    #"updated_data":"KEY"+"&emsp; "+"&emsp; "+"&emsp; "+"&emsp; "+"Old Value"+"&emsp; "+"&emsp; "+"&emsp; "+"&emsp; "+"New Value<br>",
                                                                    "values":mail_data,
                                                                    "month_year":month_year,
                                                                    #  "sales_year":"",
                                                                    'week':record[0]['week_num'],'wd_id':f"{wd_id}-{town}",'branch':f"{request.user.user_id}-{branch.region}", 'category' : f"{category}"
                                                                    })
                            weekly_save_notification_mail(subject,recipient_lists,cc_email,html_message)
                            Weeklysales_update_log.objects.update(is_sent = True)
                return Response({'massage': 'Sales data has been saved successfully' ,'status': True,})
                
            except Exception as e:
                error = getattr(e, 'message', repr(e))
                logger.error(error)
                context = {'status': False,'message':'Something Went Wrong'}
                return Response(context, status=status.HTTP_200_OK)