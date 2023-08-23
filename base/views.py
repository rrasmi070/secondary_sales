import calendar
from functools import partial
from operator import index
import random
from tokenize import String
from django.core import mail
from django.db import connection
from django.db.models.fields import EmailField
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.utils import translation
from pymysql import NULL
from base.serializers import *
from base.models import *
from master.models import *
from master.serializers import SalesDataSerializer, Integration_log_summary
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (AllowAny,IsAuthenticated)
from django.conf import settings
import os
import datetime
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from django.contrib.auth.hashers import make_password ,check_password
from django.db.models import Q
from base.tests import generate_access_token, generate_refresh_token
import jwt
import logging
import string
import random
from urllib.parse import urlparse, urljoin
import random
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context
from dateutil.relativedelta import relativedelta
from base.serializers import AdminUserSerializer
# Archived_SalesData_Serializer, BranchMasterSerializers, User_serializer, UserssSerializer
from wd.helper import week_checkbox_wd, week_sele_before_date
# from base.permissions import IsWD
logger = logging.getLogger(__name__)
from rest_framework_simplejwt.tokens import RefreshToken
from secondary_sales.settings import *
from django.db import transaction
from django.db.models import F,Count,Sum
import logging
logger = logging.getLogger(__name__)
import requests
import base64
from random import randrange
import secrets
from rest_framework import generics
from dateutil.parser import parse
import math
from django.http import JsonResponse


# Custom 404 render==============
def custom404(request, exception=None):
    return JsonResponse({
        'status_code': 404,
        'error': 'The resource was not found'
    })
    
def main_home(request):
    return JsonResponse({
        'status_code': 200,
        'massage': 'This is a base url'
    })


# refresh Token API==============
class UserRefreshTokenGeneratorGenerics(generics.GenericAPIView):
    serializer_class = UserRefreshTokenSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                context = {'status': True,'message': 'Token find successfully','access':(str(serializer.data['access'])).strip("b'")}
                return Response(context, status=status.HTTP_200_OK)
            context = {'status': False,'token_expaired':True}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {'status': False,'token_expaired':True}
            return Response(context, status=status.HTTP_200_OK)

# concurrent login--------------------
def save_refresh_token(pk, refresh_token):
    try:
        User.objects.filter(id = pk).update(token = (str(refresh_token)).strip("b'"),is_logedin = True)
    except Exception as e:
        error = getattr(e, 'message', repr(e))
        logger.error(error)
        context = {'status': False,'message':'Something Went Wrong'}
        return Response(context, status=status.HTTP_200_OK)


# lock user wrong attempt login--------------------
def wrong_attempt(pk):
    try:
        id = pk
        today_date = datetime.datetime.now()
        user = User.objects.get(id = id)
        if user and user.first_attempt:
            user.last_attempt = today_date
            user.invalid_login = (user.invalid_login)+1
            user.save()
            # user.update(last_attempt = today_date, invalid_login = (user.invalid_login)+1)
        else:
            user.first_attempt = today_date
            user.invalid_login = 1
            user.save()
            # user.update(first_attempt = today_date, invalid_login = 1)        
    except Exception as e:
        error = getattr(e, 'message', repr(e))
        logger.error(error)
        context = {'status': False,'message':'Something Went Wrong'}
        return Response(context, status=status.HTTP_200_OK)    


def login_success_reset_invalid_attempt(pk):
    try:
        id = pk
        User.objects.filter(id = id).update(first_attempt=None, last_attempt = None,invalid_login = 0)
    except Exception as e:
        error = getattr(e, 'message', repr(e))
        logger.error(error)
        context = {'status': False,'message':'Something Went Wrong'}
        return Response(context, status=status.HTTP_200_OK) 
    
# Attendance Count =========================
def attendence_count(user_id,user_type):
    user_id=user_id
    user_type=user_type
    print(datetime.datetime.today())
    data=Attendence.objects.filter(user_id=user_id,user_type=user_type,added_on__date=datetime.datetime.today()).last()
    gpi_state=WDmaster.objects.filter(wd_ids=user_id).last()
    sales_hir=Sales_Hierarchy_Master.objects.filter(wd_id=user_id).last()
    gpi_states = gpi_state.wd_state if gpi_state else "BRANCH USER"
    statename = gpi_state.wd_state if gpi_state else "BRANCH USER"
    sales_hir = sales_hir.town if sales_hir else "BRANCH USER"
    if not data:
        savedata=Attendence.objects.create(user_id=user_id,user_type=user_type,added_on=datetime.datetime.today(),gpi_state=gpi_states,town=sales_hir,statename=statename)
        print("##############   Success",Attendence)
        savedata.save()

    else:
        att_update=data
        att_update.updated_on=datetime.datetime.today()
        att_update.login_count=data.login_count+1
        att_update.save()
        

class Custom_Login(APIView):
    serializer_class = UserSerializers

    def post(self, request):
        try:
            user= request.data.get('user_type')
            user_type = user.upper()
            username = request.data.get('username')
            password = request.data.get('password')
            
            today_date = datetime.datetime.now()
                        
            base64_bytes = password.encode("ascii")
            sample_string_bytes = base64.b64decode(base64_bytes)
            sample_string = sample_string_bytes.decode("ascii")
            password = sample_string.split("_")[0]
            
            response = Response()
            errors1={"execution_time":datetime.datetime.now(),"user_id":username,"message":"login api execution start"}
            errors=getattr(errors1, 'message', repr(errors1))
            logger.error(errors)
            if (username is not None) and (password is not None) and (user_type is not None):
                user_pass = User.objects.filter(Q(email__iexact=username)|Q(user_type__iexact=user_type)).values('password','id','first_login','user_type')
                user_detail = user_pass.filter(user_id = username).values('password','id','locationcode')
                user_details = User.objects.filter(Q(user_id__iexact=username)|Q(email__iexact=username),status=True).last()
                
                
                if user_details:
                    # check user is locked due to wrong credential==============>>
                    # 5 m. locking timing=========
                    if user_details.invalid_login >= 4 and today_date < (user_details.last_attempt + datetime.timedelta(minutes=15)):
                        active_on = (user_details.last_attempt + datetime.timedelta(minutes=15)) - today_date
                        remain_time = (((str(active_on)).replace(":", ".")).split("."))
                        time = math.ceil((float(remain_time[1]+"."+remain_time[2])))
                        dict = {'massage': 'Hi, You are locked.','active_on':time,'status': False}
                        return Response(dict, status=status.HTTP_200_OK)
                    elif user_details.invalid_login >= 4 and today_date > (user_details.last_attempt + datetime.timedelta(minutes=15)):
                        User.objects.filter(id = user_details.id).update(first_attempt=None ,last_attempt=None,invalid_login = 0)
                    
                    
                    if user_type == user_details.user_type:
                        if user_pass:
                            
                            user_data = check_password(password, user_detail[0]['password'])
                            if user_data:
                                if user_details.is_logedin == True:
                                    access_token = generate_access_token(user_details.id)
                                    dict = {'massage': 'Hi, You are already login on other device. Do you want to login on this device? (Y/N)',"logged_in":True , 'status': False}
                                    return Response(dict, status=status.HTTP_200_OK)
                                user_id = user_detail[0]['id']
                                access_token = generate_access_token(user_id)
                                refresh_token = generate_refresh_token(user_id)
                                             
                            #>>>>>ADMIN and HO
                                if user_details.user_type in ["ADMIN" , "HO"]:
                                    print("admin")
                                    userdata=User.objects.filter(user_id = user_details.user_id).last()
                                    if userdata:
                                        login_success_reset_invalid_attempt(user_detail[0]['id'])
                                        save_refresh_token(user_detail[0]['id'], refresh_token)
                                        
                                        # print(userdata.first_name )
                                        serializer=AdminUserSerializer(userdata)
                                        # access_token = generate_access_token(user_id)
                                        # refresh_token = generate_refresh_token(user_id)
                                        
                                        
                                        response.data = {"access": access_token,"refresh": refresh_token, "userdata":[serializer.data], 'status': True, 'massage': 'ADMIN Login Successfully++++++>>>',}
                                        return response
                                    else:
                                        return Response({"access": access_token,"refresh": refresh_token, 'status': True, 'massage': 'You profile is not compleeted, Please contact your Branch manager',})
                                        
                                if user_details.user_type == "WD":
                                    userdata=WDmaster.objects.filter(wd_ids = user_details.user_id).last()
                                    
                                    if userdata:
                                        login_success_reset_invalid_attempt(user_detail[0]['id'])
                                        save_refresh_token(user_detail[0]['id'], refresh_token)
                                        serializer = WDmastersSerializers(userdata)
                                        attendence_count(user_id=username,user_type=user_type)
                                        response.data = {"access": access_token,"refresh": refresh_token, "userdata":[serializer.data], 'status': True, 'massage': 'Login Successfully++++++>>>',}
                                        return response
                                    else:
                                        return Response({"access": access_token,"refresh": refresh_token, 'status': True, 'massage': 'You profile is not compleeted, Please contact your Branch manager',})
                                        
                                
                                # #>>>>>ADMIN and HO
                                # if user_details.user_type == "ADMIN" or "HO":
                                #     print("admin")
                                #     userdata=User.objects.filter(user_id = user_details.user_id).last()
                                #     if userdata:
                                #         login_success_reset_invalid_attempt(user_detail[0]['id'])
                                #         save_refresh_token(user_detail[0]['id'], refresh_token)
                                        
                                #         # print(userdata.first_name )
                                #         serializer=AdminUserSerializer(userdata)
                                #         # access_token = generate_access_token(user_id)
                                #         # refresh_token = generate_refresh_token(user_id)
                                        
                                        
                                #         response.data = {"access": access_token,"refresh": refresh_token, "userdata":[serializer.data], 'status': True, 'massage': 'ADMIN Login Successfully++++++>>>',}
                                #         return response
                                #     else:
                                #         return Response({"access": access_token,"refresh": refresh_token, 'status': True, 'massage': 'You profile is not compleeted, Please contact your Branch manager',})
                                        
                                
                                
                                
                                
                                
                                if user_details.user_type == "BRANCH USER" :
                                    # BranchMaster.objects.filter(branch_id = user_detail[0]['id'])
                                  
                             
                                    userdata=BranchMaster.objects.filter(branch_code = user_detail[0]['locationcode']).last()
                                    print("branch master @@@@@@@@@@@@@@@")
                                    if userdata:
                                        login_success_reset_invalid_attempt(user_detail[0]['id'])
                                        save_refresh_token(user_detail[0]['id'], refresh_token)
                                        serializer = BranchMasterSerializer(userdata)
                                        attendence_count(user_id=username,user_type=user_type)
                                        response.data = {"access": access_token,"refresh": refresh_token, "userdata":[serializer.data], 'status': True, 'massage': 'Login Successfully',}
                                        return response

                                    else:
                                        return Response({"access": access_token,"refresh": refresh_token, 'status': True, 'massage': 'You profile is not compleeted, Please contact ADMIN',})
                                    
                            
                            
                            else:
                                wrong_attempt(user_detail[0]['id'])
                                dict = {'massage': 'Incorrect login credentials. Please try again.', 'status': False}
                                return Response(dict, status=status.HTTP_200_OK)
                        else:
                            wrong_attempt(user_detail[0]['id'])
                            dict = {'massage': 'Incorrect login credentials. Please try again.', 'status': False}
                            return Response(dict, status=status.HTTP_200_OK)
                    else:
                        dict = {'massage': 'Please select correct user type.', 'status': False}
                        return Response(dict, status=status.HTTP_200_OK)
                else:
                    # wrong_attempt(user_detail[0]['id'])
                    dict = {'massage': 'Incorrect login credentials. Please try again. ', 'status': False}
                    return Response(dict, status=status.HTTP_200_OK)
            else:
                dict = {'massage': 'Please enter Username, Password and usertype.', 'status': False}
                return Response(dict, status=status.HTTP_200_OK)
            # errors1={"execution_time":datetime.datetime.now(),"user_id":username,"message":"login api execution end"}
            # errors=getattr(errors1, 'message', repr(errors1))
            # logger.error(errors)
            # return response
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)
           

        
class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        old_password = request.data.get('old_password')
        print(old_password)
        # new_password = request.data['new_password']
        confirm_password = request.data.get('confirm_password')
        print(confirm_password)
        if not old_password:
            dict = {'massage': 'Please enter current password.', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)
        if not confirm_password:
            dict = {'massage': 'please enter confirm password.', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)


        try:
            user = User.objects.filter(email = request.user).last()
            password_list = Password_History.objects.filter(user_id = request.user.user_id).order_by('-id')[:5]
            print(user.check_password(old_password))
            if user is not None:
                
                if not user.check_password(old_password):
                    dict = {'massage': 'Current password incorrect.', 'status': False}
                    return Response(dict, status=status.HTTP_200_OK)
                elif user.check_password(confirm_password):
                    dict = {'massage': 'New password and Current password can not be same', 'status': False}
                    return Response(dict, status=status.HTTP_200_OK)
                elif password_list:
                    for i in password_list:
                        if check_password(confirm_password,i.password) == True:
                            dict = {'massage': 'You can not use recently used password', 'status': False}
                            return Response(dict, status=status.HTTP_200_OK)
                        
                    else:
                        # this code is, if the user is changeing the password before=====
                        user.check_password(old_password)
                        user.set_password(confirm_password)
                        user.first_login = False
                        user.raw_password = None
                        user.last_reset_time = None   
                        user.save()
                        mk_password = make_password(confirm_password)
                        Password_History.objects.create(
                                user_id = request.user.user_id,user_type = request.user.user_type,
                                create_date = datetime.datetime.now(),password = mk_password
                                )
                        dict = {'massage': "Password updated successfully.", 'status': True}
                        return Response(dict, status=status.HTTP_200_OK)
                    # return Response(dict, status=status.HTTP_200_OK)  
                    # return Response(dict, status=status.HTTP_200_OK)
                else:
                    # this code is, if the user is changeing the password first time
                    user.check_password(old_password)
                    user.set_password(confirm_password)
                    user.first_login = False
                    user.raw_password = None
                    user.last_reset_time = None
                    user.save()
                    mk_password = make_password(confirm_password)
                    Password_History.objects.create(
                            user_id = request.user.user_id,user_type = request.user.user_type,
                            create_date = datetime.datetime.now(),password = mk_password
                            )
                    dict = {'massage': "Password updated successfully.", 'status': True}
                    return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)


from master.email_sub import reset_pass_to_email,reset_pass_cc_list,reset_pass_sub

#reset mail funciton

def resetmail_func(user_id,password,region,subject,to_user_li,cc_user_li):
    
    subject = subject
    html_message = '<h3>Your New Password:</h3>'
    html_message += '<p> Username <b>: '+str(user_id)+'</b> </p>'
    html_message += '<p>Your New Password : <b>' +password+ '</b> </p>'
    html_message += '<p>Your Branch is : <b>' +str(region)+ '</b> </p>'
    email_from = settings.EMAIL_HOST_USER
    #cc_email = ['kamalkantu@triazinesoft.com']
    cc_email = reset_pass_cc_list
    # recipient_list = ["rasmis@triazinesoft.com"].append(location_obj.email)
    recipient_list = reset_pass_to_email
    reset_email = EmailMessage(
                subject = subject,
                body = html_message,
                from_email = email_from,
                to = to_user_li,
                cc = cc_user_li,
                reply_to = cc_user_li,
                )
    reset_email.content_subtype = "html"
    reset_email.send(fail_silently=True)
    return True
    


class ResetPassword(APIView):
    def post(self, request):
        try:
            request.data['user_id']=request.data['email']
            
            # password_range = randrange(8, 15)
            # password = res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = password_range))
            # print(password,"=================")
            num = randrange(6, 7)
            # password = str(''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation)for x in range(num)))
            password = (''.join(secrets.choice(string.ascii_letters + string.digits)for x in range(num))+"@"+''.join(secrets.choice(string.digits)for x in range(num)))
            
            request.data['password'] = make_password(password)
            # request.data['istemporary'] = "1"

            userinfo=User.objects.filter(user_id=request.data['user_id']).last()
          
            email_subject = Subject.objects.filter(use_for__icontains = "reset_password").last()
            emails = Email_users.objects.filter(subject = email_subject.id,is_active = True)
            subject = email_subject.name
            cc_user_li = emails.filter(email_cc = True).values_list('email', flat = True)
            to_user_li = emails.filter(email_to = True).values_list('email', flat = True)
            print(subject,cc_user_li,to_user_li)
            # breakpoint()
            currenttime=datetime.datetime.now()
            if userinfo:
                branch_name=None
                admin_type = None
                timediff=userinfo.last_reset_time + datetime.timedelta(minutes=180) if userinfo.last_reset_time else None
                print(userinfo.locationcode,'aa')
                                
                if userinfo.user_type in ['WD','BRANCH USER']:
                    branch_name=BranchMaster.objects.filter(branch_code=userinfo.locationcode).last()
                    if timediff and (userinfo.last_reset_time <= currenttime <= timediff):
                        resetmail_func(request.data['user_id'],userinfo.raw_password,branch_name.region,subject,to_user_li,cc_user_li)
                    else:
                        # datas = User.objects.filter(email = userinfo)
                        # # .update(first_login = True, password = request.data['password'],last_reset_time = currenttime)
                        # # print(request.data['password'],"============",datas)
                        # # breakpoint()
                        usersname = User.objects.filter(email=userinfo).values('username','locationcode').first()
                        location_obj=User.objects.filter(user_type__iexact="BRANCH USER",locationcode=usersname['locationcode']).last()
                        userinfo.raw_password = password
                        userinfo.first_login = True
                        userinfo.password = request.data['password']
                        userinfo.last_reset_time = currenttime
                        userinfo.save()
                        resetmail_func(request.data['user_id'],userinfo.raw_password,branch_name.region,subject,to_user_li,cc_user_li)
                
                else:
                    admin_type = userinfo.user_type if userinfo.user_type else "ADMIN/HO"
                    if timediff and (userinfo.last_reset_time <= currenttime <= timediff):
                        datas = User.objects.filter(email = userinfo).update(first_login = True, password = request.data['password'],last_reset_time = currenttime)
                        usersname = User.objects.filter(email=userinfo).values('username','locationcode').first()
                        # location_obj=User.objects.filter(user_type__iexact="BRANCH USER",locationcode=usersname['locationcode']).last()
                        resetmail_func(request.data['user_id'],userinfo.raw_password,admin_type,subject,to_user_li,cc_user_li)
                    else:
                        userinfo.raw_password = password
                        userinfo.first_login = True
                        userinfo.password = request.data['password']
                        userinfo.last_reset_time = currenttime
                        userinfo.save()
                        
                        resetmail_func(request.data['user_id'],password,branch_name,subject,to_user_li,cc_user_li)
                
                    
                # print(branch_name,'fff',admin_type)
                # branch_name = branch_name.region if branch_name else admin_type
                # # print(type(timediff),'vvvvv')
                # if timediff and (userinfo.last_reset_time <= currenttime <= timediff):
                #     resetmail_func(request.data['user_id'],userinfo.raw_password,branch_name)
                    
                # else:
                #     userinfo.raw_password = password
                #     userinfo.last_reset_time = currenttime
                #     userinfo.save()
                    
                #     resetmail_func(request.data['user_id'],password,branch_name)
                
                # subject = reset_pass_sub
                # html_message = '<h3>Your New Password:</h3>'
                # html_message += '<p> Username <b>: '+str(request.data['user_id'])+'</b> </p>'
                # html_message += '<p>Your New Password : <b>' +password+ '</b> </p>'
                # html_message += '<p>Your Branch is : <b>' +str(branch_name.region)+ '</b> </p>'
                # email_from = settings.EMAIL_HOST_USER
                # #cc_email = ['kamalkantu@triazinesoft.com']
                # cc_email = reset_pass_cc_list
                # # recipient_list = ["rasmis@triazinesoft.com"].append(location_obj.email)
                # recipient_list = reset_pass_to_email
                # reset_email = EmailMessage(
                #             subject = subject,
                #             body = html_message,
                #             from_email = email_from,
                #             to = recipient_list,
                #             cc = cc_email,
                #             reply_to = cc_email,
                #             )
                # reset_email.content_subtype = "html"
                # reset_email.send(fail_silently=True)
                # SendMailToUserForgotPasswordThread(record_data).start()
                

                if resetmail_func:
                    dict = {'massage': 'An email has been sent to reset your password', 'status': True}
                    return Response(dict, status=status.HTTP_200_OK)
                else:
                    dict = {'massage': 'data not found', 'status': False}
                    return Response(dict, status=status.HTTP_200_OK)
            else:
                dict = {'massage': 'Please enter correct user id.', 'status': False,'code':'400'}
                return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)



from wd import utils
class Profile(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            print(request.session,"=========================")
            # now = utils.now_date
            now = datetime.datetime.now()   
            user_type = request.user.user_type
            #  this is for take a constant time===================
            till_date = datetime.datetime(2009, 10, 5, 15, 00, 00)

            week_1st = [datetime.datetime(now.date().year, now.date().month, 8).date(),datetime.datetime(now.date().year, now.date().month,10).date()]
            week_2st = [datetime.datetime(now.date().year, now.date().month, 15).date(),datetime.datetime(now.date().year, now.date().month, 17).date()]
            week_3st = [datetime.datetime(now.date().year, now.date().month, 22).date(),datetime.datetime(now.date().year, now.date().month, 24).date()]
            last_date_month = datetime.datetime(now.date().year, now.date().month, calendar.monthrange(now.date().year,now.date().month)[1]).date()
            week_4st = [datetime.datetime(now.date().year, now.date().month, 1).date(),datetime.datetime(now.date().year, now.date().month, 3).date()]
            
            dddd = datetime.datetime.combine(week_1st[0], till_date.time())

            # date tuple for open weekly checkbox Instant ==============
            weekend_dates = (
                datetime.datetime(now.date().year, now.date().month, 7).date(), #0
                datetime.datetime(now.date().year, now.date().month, 8).date(), #1
                
                datetime.datetime(now.date().year, now.date().month, 14).date(), #2
                datetime.datetime(now.date().year, now.date().month, 15).date(), #3
                
                datetime.datetime(now.date().year, now.date().month, 21).date(), #4
                datetime.datetime(now.date().year, now.date().month, 22).date(), #5
                
                last_date_month, #6
                datetime.datetime(now.date().year, now.date().month, 1).date(), #7
                
                datetime.datetime(now.date().year, now.date().month, 1).date() -relativedelta(days=1), #8
                # for test============
                # datetime.datetime(now.date().year, now.date().month, 10).date(), #9
            )
            # print()
            week_details = week_sele_before_date(request.user.user_type)
            # print(weekend_dates[6],weekend_dates[7],"=====till_date======//",weekend_dates,week_details[2][1],week_details[2][0])
            wd_weekly = ""
            if now.date() in weekend_dates and user_type == "WD":
                week_details = week_checkbox_wd(request.user.user_type)
                if now.date() == weekend_dates[0] or now.date() == weekend_dates[1]:
                    sale_data_check = SalesData.objects.filter(Q(sales_date_time = week_details[2][0])|Q(sales_date_time = week_details[2][1]),transaction_type = "Week1" ,wd_id = request.user.user_id)
                    if sale_data_check:
                        wd_weekly= "Week1"

                elif now.date() == weekend_dates[2] or now.date() == weekend_dates[3]:
                    sale_data_check = SalesData.objects.filter((Q(sales_date_time = week_details[2][0])|Q(sales_date_time = week_details[2][1])),transaction_type = "Week2" ,wd_id = request.user.user_id)
                    print(weekend_dates[2],"==99=====",weekend_dates[3],sale_data_check)
                    # |Q(sales_date_time = weekend_dates[3])
                    if sale_data_check:
                        wd_weekly= "Week2"
                    # return sale_data_check

                elif now.date() == weekend_dates[4] or now.date() == weekend_dates[5]:
                    print(weekend_dates[5],"====ee===",weekend_dates[4])
                    sale_data_check = SalesData.objects.filter(Q(sales_date_time = week_details[2][0])|Q(sales_date_time = week_details[2][1]),transaction_type = "Week3" ,wd_id = request.user.user_id)
                    # sale_data_check = SalesData.objects.filter(sales_date_time__month = weekend_dates[4].month,sales_date_time__year = weekend_dates[5].year,transaction_type = "Week3" ,wd_id = request.user.user_id)
                    
                    # |Q(sales_date_time = weekend_dates[4])
                    # return sale_data_check
                    if sale_data_check:
                        print(sale_data_check,"====ee2===")
                        wd_weekly= "Week3"

                elif now.date() == weekend_dates[6] or now.date() == weekend_dates[7]:
                    sale_data_check = SalesData.objects.filter(Q(sales_date_time = week_details[2][0])|Q(sales_date_time = week_details[2][0]-datetime.timedelta(days=1)),transaction_type = "Week4" ,wd_id = request.user.user_id)
                    if sale_data_check:
                        wd_weekly= "Week4"

                # pass
            
            print(wd_weekly,"====last_date_month===")
            
            

            # print(datetime.datetime.combine(week_2st[0], till_date.time()) <= now and now.date() <= week_2st[1])
            if datetime.datetime.combine(week_1st[0], till_date.time()) <= now and now.date() <= week_1st[1] :
                print("hhhh1")
                weekly = "Week1"
            elif datetime.datetime.combine(week_2st[0], till_date.time()) <= now and now.date() <= week_2st[1] :
                print("hhhh2")
                weekly = "Week2"
            elif datetime.datetime.combine(week_3st[0], till_date.time()) <= now and now.date() <= week_3st[1] :
                print("hhhh3")
                weekly = "Week3"
            elif datetime.datetime.combine(week_4st[0], till_date.time()) <= now and now.date() <= week_4st[1] :
                print("hhhh4")
                weekly = "Week4"
            else:
                print("hhhh7777")
                weekly = ""
            
            # sale_data_check = SalesData.objects.filter(transaction_type =  ,sales_date_time = now.date(), wd_id = request.user.user_id)
            if request.user.user_type == "BRANCH USER":
                print(request.user.user_type)
                print(request.user.user_id)
                
                userid = BranchMaster.objects.filter(branch_code = request.user.locationcode).last()
                print(userid)
                if userid:
                    serializer = BranchMasterSerializer(userid)
                    dat = serializer.data
                    # dat['week']=weekly
                    dat['week']= ""
                    print(dat,"=====>>")
                    dict = {'user_data':[dat],'massage': 'Succesful', 'status': True}
                    return Response(dict, status=status.HTTP_200_OK)
                else:
                    dict = {'massage': 'Invalid User', 'status': False}
                    return Response(dict, status=status.HTTP_200_OK)

            elif request.user.user_type == "WD":
                # print(week_details[2],"=======>>")
                week_details = week_checkbox_wd(request.user.user_type)
                week_details_dt = week_details[2][1] if week_details[2] else None
                week_details_week = week_details[1] if week_details[1] and week_details[1] else None
                # print(week_details, )
                sale_data_check = SalesData.objects.filter(transaction_type = week_details_week ,sales_date_time = week_details_dt, wd_id = request.user.user_id)
                userid = WDmaster.objects.filter(wd_ids = request.user.user_id).last()
                if userid:
                    serializer = WDmastersSerializers(userid)
                    dat = serializer.data
                    dat['week']=week_details[1] if sale_data_check else ""
                    print(dat,"=====>>")
                    dict = {'user_data':[dat],'massage': 'Succesful', 'status': True}

                    return Response(dict, status=status.HTTP_200_OK)
                else:
                    dict = {'massage': 'Invalid User', 'status': False}
                    return Response(dict, status=status.HTTP_200_OK)
                
                
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            elif request.user.user_type == "ADMIN":
                userid = User.objects.filter(user_id=request.user.user_id).last()
                print(userid)
                if userid:
                    serializer = AdminUserSerializer(userid)
                    dat = serializer.data
                    # dat['week']=weekly
                    dat['week']= ""
                    print(dat,"=====>>")
                    dict = {'user_data':[dat],'massage': 'Succesful', 'status': True}
                    return Response(dict, status=status.HTTP_200_OK)
                else:
                    dict = {'massage': 'Invalid User', 'status': False}
                    return Response(dict, status=status.HTTP_200_OK)
            
                
                
                
                
            else:
                dict = {'massage': 'Invalid User', 'status': False}
                return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)



# Logout API===============================
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view


from rest_framework import generics, status, views, permissions
# class LogoutAPIView(generics.GenericAPIView):
class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            print(request.data["refresh"])
            refresh_token = request.data["refresh"]
            # token = RefreshToken(refresh_token)
            # token.blacklist()
            try:
                payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
            except jwt.ExpiredSignatureError as e:
                raise serializers.ValidationError({'error': 'Expired refresh token, please login again.'}) from e
            
            User.objects.filter(id = payload.get('user_id')).update(is_logedin = False, token = None)
            # print(payload.get('user_id'),"================>>>>>>>========")
            
            context = {"status": True, 'message':'Logout Successfully.'}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            context = {'status': False,'message':'Something Went Wrong'}
            return Response(context, status=status.HTTP_200_OK)
        
        
        
class Concurrent_login(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        # try:
            wd_id = request.data['wd_id']
            password = request.data['password']
            
            base64_bytes = wd_id.encode("ascii")
            sample_string_bytes = base64.b64decode(base64_bytes)
            sample_string = sample_string_bytes.decode("ascii")
            wd_id = sample_string.split("_")[0]
            
            base64_bytes = password.encode("ascii")
            sample_string_bytes = base64.b64decode(base64_bytes)
            sample_string = sample_string_bytes.decode("ascii")
            password = sample_string.split("_")[0]
            
            # User.objects.filter(user_id = wd_id).update(is_logedin = False, token = None)
            
            
            user = User.objects.filter(user_id=wd_id).last()
            
            # print(wd_id,"==================??=",user)
            if user:
                user_data = check_password(password, user.password)
            if user and user_data:
                
                
                ### Blacklist Old User.
               
                token=RefreshToken(user.token)
                # print(token,"=============")
                token.blacklist()
                access_token = generate_access_token(user.id)
                refresh_token = generate_refresh_token(user.id)
                if user.user_type == "WD":
                    # userdata1=User.objects.filter(user_id = user.id).values_list()
                    # print(userdata1,"ddddddddddddd")
                    
                    userdata=WDmaster.objects.filter(wd_ids = user.user_id).last()
                    serializer = WDmastersSerializers(userdata)
                    
                    
                if user.user_type == "BRANCH USER":
                
                    userdata=BranchMaster.objects.filter(branch_code = user.locationcode).last()
                    serializer = BranchMasterSerializer(userdata)
                    
                if user.user_type in ["ADMIN", "HO"]:
                                   
            
                    print(user,"user--------------")
                     
                    userdata=User.objects.filter(user_id = user.user_id).last()
                    print(userdata,'////////////////')
                    serializer = AdminUserSerializer(userdata)
                   
                # wd_id=self.request.user.id
                print(wd_id)
                user_update = User.objects.get(user_id=wd_id)
                # print("SSSSSSSSSSSSSS",user_update)
                user_update.token = (str(refresh_token)).strip("b'")
                user_update.is_logedin = True
                user_update.save()
                login_success_reset_invalid_attempt(user.id)
                attendence_count(wd_id,user.user_type) #attendance ---------------
                context = {"access": access_token,"refresh": refresh_token, "userdata":[serializer.data], 'status': True, 'massage': 'Login Successfully',}
                return Response(context, status=status.HTTP_200_OK)
            else:
                if user:
                    wrong_attempt(user.id)
                dict = {'massage': 'Incorrect login credentials. Please try again.', 'status': False}
                return Response(dict, status=status.HTTP_200_OK)
        # except Exception as e:
        #     error = getattr(e, 'message', repr(e))
        #     logger.error(error)
        #     context = {'status': False,'message':'Something Went Wrong'}
        #     return Response(context, status=status.HTTP_200_OK)

