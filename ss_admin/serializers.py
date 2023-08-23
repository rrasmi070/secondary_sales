# from dataclasses import field
import json
from django.db import models
from base.models import *
from master.models import *
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from django.core.validators import FileExtensionValidator
import pandas as pd



class BranchListSerializer(serializers.ModelSerializer):
    From = SerializerMethodField('from')

    class Meta:
        model =  User
        fields = ['wd_name','region','branch_code','user_id','user_type']

# class WDListSerializer(serializers.ModelSerializer):
    
#     wd_name = SerializerMethodField('first_name')
#     wd_id = SerializerMethodField('user_id')
    
#     class Meta:
#         model=User


class Wmaster_wd_towns(serializers.ModelSerializer):
    town = serializers.SerializerMethodField()
    town_code = serializers.SerializerMethodField()
    class Meta:
        model =  WDmaster
        fields = ['town','town_code']
        
    def get_town(self, obj):
        # print(obj['wd_postal_code'],"=======serializer======")
        return obj['wd_postal_code']

    def get_town_code(self, obj):
        # print(str(obj.wd_postal_code),"=================serializer======")
        # a = str(obj.wd_postal_code).split('-')[1]
        # if len(str(obj['wd_postal_code']).split('-'))>1 :
        #     return str(obj['wd_postal_code']).split('-')[1]
        # else:
        #     return ""
        town_code = Sales_Hierarchy_Master.objects.filter(town__iexact = obj['wd_postal_code']).last()
        if town_code:
            return town_code.town_code
        else:
            return ""
        
        
class Sku_master_serializer(serializers.ModelSerializer):
    class Meta:
        model=SKU_Master_Product
        fields="__all__"
        
class WDMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=WDmaster
        fields="__all__"
 