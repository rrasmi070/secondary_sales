from django.db import models
from base.models import *
from master.models import *
from rest_framework import serializers


        
class TownSerializer(serializers.ModelSerializer):
    # brand_catagory = serializers.SerializerMethodField()
    class Meta:
        model =  Sales_Hierarchy_Master
        fields = ['wd_town_id','town_code','town','country']
        


class UserSerializer(serializers.ModelSerializer):
    town_id = serializers.SerializerMethodField()
    class Meta:
        model =  User
        fields = ['user_type','town_id']
    
    def get_town_id(self, obj):
        data = Sales_Hierarchy_Master.objects.filter(wd_id=obj.username)
        return TownSerializer(data, many=True).data

class Sku_remarksSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Sku_remarks
        fields = '__all__'

class wd_searchSerializer(serializers.ModelSerializer):
    wd_id = serializers.CharField(source='user_id')
    wd_name = serializers.CharField(source='first_name')
    wd_source = serializers.SerializerMethodField()
    class Meta:
        model =  User
        fields = ['id','wd_id','wd_name','wd_source']
    def get_wd_source(self, obj):
        data = WDmaster.objects.filter(wd_ids=obj.user_id).last()
        if data:
            return data.wd_type
        return ""

class Total_sku_sales_serializer(serializers.ModelSerializer):
    class Meta:
        model =  Total_sku_sales
        fields = '__all__'
        
class SalesDataCreateWeekSerializer(serializers.ModelSerializer):
     class Meta:
        model =  SalesData
        fields = '__all__'
    