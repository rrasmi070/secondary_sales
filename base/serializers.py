import os
from urllib.parse import urljoin, urlparse
import jwt
from pymysql import NULL
from rest_framework import serializers
from base.tests import generate_access_token

from secondary_sales import settings
from .models import *
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as validators
import logging
logger = logging.getLogger(__name__)

"""
Build the image URL
"""
def get_image_url(url,path):

    filename = os.path.basename(urlparse(url).path)

    return urljoin(url, path+"/" + filename)

class UserRefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=255,error_messages={'blank': 'Please enter refresh_token'})
    access = serializers.CharField(read_only=True)
    status = serializers.BooleanField(default=False)

    ref_name ='UserRefreshToken'

    def validate(self, attrs):
        try:
            refresh_token = attrs.get('refresh')
            try:
                payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
            except jwt.ExpiredSignatureError as e:
                raise serializers.ValidationError({'error': 'Expired refresh token, please login again.'}) from e
            
            user = User.objects.filter(id=payload.get('user_id')).first()
            print(user.id,"=================", user.token)
            if user and user.token:
                print("========================//===================")
                print(refresh_token)
                print(user.token)
                if str(refresh_token) == user.token:
                    access_token = generate_access_token(user.id)
                    attrs['access'] = access_token
                    attrs['status'] = True
                    return super().validate(attrs)
                # else:
                raise serializers.ValidationError({'error' : 'Token Expaired'})
                    
            if user is None:
                raise serializers.ValidationError({'error' : 'User not found'})
        except Exception as e:
            error = getattr(e, 'message', repr(e))
            logger.error(error)
            
            
            

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ['user_type','lock_unlock',]


class WDmastersSerializers(serializers.ModelSerializer):
    first_login = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()
    user_lock_unlock = serializers.SerializerMethodField()
    wduser_id = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    wd_id = serializers.SerializerMethodField()
    wd_source = serializers.SerializerMethodField()
    
    class Meta:
        model =  WDmaster
        fields = ['wd_ids','wd_id','wduser_id','wd_name','wd_address1','wd_address2','wd_postal_code','wd_city','wd_state','wd_country','first_login', 'user_type','user_lock_unlock','profile_pic','wd_source']
    
    def get_first_login(self, obj):
        print(obj)
        first_login = User.objects.filter(user_id = obj.wd_ids, user_type = "WD").last()
        return first_login.first_login

    def get_user_type(self, obj):
        # print(obj.wd_ids)
        first_login = User.objects.filter(user_id = obj.wd_ids, user_type = "WD").last()
        return first_login.user_type

    def get_user_lock_unlock(self, obj):
        # print(obj.wd_ids)
        first_login = User.objects.filter(user_id = obj.wd_ids, user_type = "WD").last()
        return first_login.lock_unlock

    def get_wduser_id(self, obj):
        # print(obj.wd_ids)
        first_login = User.objects.filter(user_id = obj.wd_ids, user_type = "WD").last()
        return first_login.username

    def get_wd_id(self, obj):
        # print(obj.wd_ids)
        first_login = User.objects.filter(user_id = obj.wd_ids).last()
        return first_login.user_id

    def get_profile_pic(self, obj):
        first_login = User.objects.filter(user_id = obj.wd_ids).last()
        if first_login.profile_pic:
            print(first_login.profile_pic.url)
            # img = get_image_url(first_login.profile_pic.url,"profile_pic/")
            return first_login.profile_pic.url
        else:
            return ""
    def get_wd_source(self, obj):
        if obj.wd_type:
            return obj.wd_type
        else:
            return ""
        
        

class BranchMasterSerializer(serializers.ModelSerializer):

    first_login = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()
    user_lock_unlock = serializers.SerializerMethodField()
    branch_user = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    branch_id = serializers.SerializerMethodField()
   
    
    class Meta:
        model =  BranchMaster
        fields = ['branch_id','branch_user','branch_name','branch_address1','branch_address2','branch_code','region','branch_state','branch_city',
        'branch_postal_code', 'branch_country', 'branch_country_code','first_login','user_type','user_lock_unlock','profile_pic']


   
    def get_branch_id(self, obj):
        first_login = User.objects.filter(locationcode = obj.branch_code, user_type = "BRANCH USER").last()
        return first_login.user_id

    def get_first_login(self, obj):
        first_login = User.objects.filter(locationcode = obj.branch_code, user_type = "BRANCH USER").last()
        return first_login.first_login

    def get_user_type(self, obj):
        print(obj.branch_code,"==========>>>>>>>>>>>>>========")
        first_login = User.objects.filter(locationcode = obj.branch_code, user_type = "BRANCH USER").last()
        return first_login.user_type

    def get_user_lock_unlock(self, obj):
        first_login = User.objects.filter(locationcode = obj.branch_code, user_type = "BRANCH USER").last()
        return first_login.lock_unlock

    def get_branch_user(self, obj):
        first_login = User.objects.filter(locationcode = obj.branch_code, user_type = "BRANCH USER").last()
        if first_login.username:
            return first_login.username
        else:
            return ""
        # return first_login.username

    def get_profile_pic(self, obj):
        # print(obj.wd_id)
        first_login = User.objects.filter(locationcode = obj.branch_code).last()
        if first_login.profile_pic:
            return first_login.profile_pic.url
        else:
            return ""

class User_uoloadSerializers(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = '__all__'


class User_serializ(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = '__all__'


        
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields ='__all__'
    