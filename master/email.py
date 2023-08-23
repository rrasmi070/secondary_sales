import calendar
from email.mime.application import MIMEApplication
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
# from master.serializers import SalesDataSerializer, Integration_log_summary
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import (AllowAny,IsAuthenticated)
# from django.conf import settings
# import os
# import datetime
# from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
# from django.contrib.auth.hashers import make_password ,check_password
# from django.db.models import Q
# from base.tests import generate_access_token, generate_refresh_token
# import jwt
# import logging
# import string
# import random
from urllib.parse import urlparse, urljoin
import random
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import get_template
# from django.template import Context
# from dateutil.relativedelta import relativedelta
# from base.serializers import AdminUserSerializer
# Archived_SalesData_Serializer, BranchMasterSerializers, User_serializer, UserssSerializer
from wd.helper import week_sele_before_date
# from base.permissions import IsWD
# logger = logging.getLogger(__name__)
# from rest_framework_simplejwt.tokens import RefreshToken
from secondary_sales.settings import *
from django.db import transaction
from django.db.models import F,Count,Sum
import logging
logger = logging.getLogger(__name__)
import requests
import base64
from random import randrange
import secrets
# from rest_framework import generics
# from dateutil.parser import parse
import math
from django.http import JsonResponse



    # subject = "reset_pass_sub"
    # html_message = '<h3>Your New Password:</h3>'
    # html_message += '<p> Username <b>: '+str(record)+'</b> </p>'
    # html_message += '<p>Your New Password : <b>' +"hello"+ '</b> </p>'
    # html_message += '<p>Your Branch is : <b>' +"str(hello)"+ '</b> </p>'
    # email_from = settings.EMAIL_HOST_USER
    # cc_email = ['kamalkantu@triazinesoft.com']
    # # cc_email = reset_pass_cc_list
    # # recipient_list = ["rasmis@triazinesoft.com"].append(location_obj.email)
    # recipient_list = cc_email
    # reset_email = EmailMessage(
    #             # subject = "subject",
    #             body = html_message,
    #             from_email = email_from,
    #             to = recipient_list,
    #             cc = cc_email,
    #             reply_to = cc_email,
    #             )
    # reset_email.content_subtype = "html"
    # reset_email.send(fail_silently=True)
    # return True
    
    
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from master.email_sub import *
# mail_content = '''Hello,
# This is a test mail.
# In this mail we are sending some attachments.
# The mail is sent using Python SMTP library.
# Thank You
# '''


def mail_func(pass_cc_email,pass_to_email,subject,body,*argument):
    mail_list=pass_cc_email
    subject=subject
    html_message=body
    #The mail addresses and password
    sender_address =EMAIL_HOST_USER
    sender_pass = EMAIL_HOST_PASSWORD
    # mail_list =[ "kamalkantu@triazinesoft.com,suryas@triazinesoft.com,rasmis@triazinesoft.com"]
    cc=""
    cc_id = mail_list
    for i in cc_id:
        cc+=i+","
    print(cc,'@@@@@@@@@@@@@@@@@@@@')
    receiver_address = ''  #"suryas@triazinesoft.com"
    print('set up MIME')
    rec_id = pass_to_email
    for i in rec_id:
        receiver_address+=i+","
    # receiver_address ="suryas@triazinesoft.com"
    #Setup the MIME
   
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message["Cc"] = cc   
    message['Subject'] = subject
    
    print(message)
    # breakpoint()
    #The subject line
    #The body and the attachments for the mail
    # message.attach(MIMEText(mail_content, 'xlsx'))
    #>>>>>>>>>>>>>>>>>new script>>>>>>>
    body = MIMEText(html_message, 'html', 'utf-8')  
    message.attach(body)  # add message body (text or html)
    for f in argument:
     # add files to the message
        filename=os.path.basename(f)     
        file_path = os.path.join(f)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition','attachment', filename=f)
        message.attach(attachment)       
    #>>>>   END
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password 
    text = message.as_string()
    session.sendmail(message["From"], message["To"].split(",") + str(message["Cc"]).split(","), text)
    # session.sendmail(sender_address,receiver_address,text)
    session.quit()
    print('Mail Sent')
    
def weekly_save_notification_mail(subject,recipient_list,cc_email,html_message):
    # print(subject,"===========",recipient_list,cc_email,html_message)
    
    email_from = EMAIL_HOST_USER
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