# from types import ClassMethodDescriptorType
from django.db.models import fields
from rest_framework import serializers
from master.models import *
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as validators
from base.models import *


class Candy_JAR_GMSSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Candy_JAR_GMS
        fields = "__all__"


class SalesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SalesData
        fields = "__all__"
class SalesData_7daysSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SalesData_7days
        fields = "__all__"

class Temp_Total_sku_salesSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Temp_Total_sku_sales
        fields = "__all__"



class SalesDataSerializers(serializers.ModelSerializer):
    total_local_sales = serializers.SerializerMethodField()
    total_outstation_sale = serializers.SerializerMethodField()
    total_other_sales = serializers.SerializerMethodField()
    total_sales = serializers.SerializerMethodField()
    total_other_issue = serializers.SerializerMethodField()
    class Meta:
        model =  SalesData
        fields = ['sku_id','wd_id','town_id','sale_date_time','local_sales_retail','local_sales_dealer',
        'local_sales_modern_trade','local_sales_hawker','outstation_sales_reatil','outstation_sales_dealer',
        'outstation_sales_modern_trade','outstation_sales_hawker','other_sales_reatil','other_sales_dealer',
        'other_sales_modern_trade','other_issues_damage','other_issues_return','other_issues_other','last_updated_date',
        'created_by','updated_by','source','created_on','created_by','updated_on','updated_by','total_local_sales',
        'total_outstation_sale','total_other_sales','total_sales','total_other_issue']

    def get_total_local_sales(self, obj):
        print('++++++++++++++++++++')
        total_local_sales = int(obj.local_sales_retail) +int(obj.local_sales_dealer) +int(obj.local_sales_modern_trade) +int(obj.local_sales_hawker)
        return total_local_sales

    def get_total_outstation_sale(self, obj):
        total_outstation_sale = int(obj.outstation_sales_reatil) +int(obj.outstation_sales_dealer) +int(obj.outstation_sales_modern_trade) +int(obj.outstation_sales_hawker)
        return total_outstation_sale

    def get_total_other_sales(self, obj):
        total_other_sales = int(obj.other_sales_reatil) +int(obj.other_sales_dealer) +int(obj.other_sales_modern_trade)
        return total_other_sales

    def get_total_other_issue(self, obj):
        total_other_issue = int(obj.other_issues_return) +int(obj.other_issues_damage) +int(obj.other_issues_other)
        return total_other_issue

    def get_total_sales(self, obj):
        total_local_sales = int(obj.local_sales_retail) +int(obj.local_sales_dealer) +int(obj.local_sales_modern_trade) +int(obj.local_sales_hawker)

        total_outstation_sale = int(obj.outstation_sales_reatil) +int(obj.outstation_sales_dealer) +int(obj.outstation_sales_modern_trade) +int(obj.outstation_sales_hawker)

        total_other_sales = int(obj.other_sales_reatil) +int(obj.other_sales_dealer) +int(obj.other_sales_modern_trade)

        total_sales = total_local_sales+total_outstation_sale+total_other_sales

        return total_sales

# class GPIWeeklySalesSerializers(serializers.ModelSerializer):
#     class Meta:
#         model =  GPIWeeklySales
#         fields = '__all__'

class SKU_Master_ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model =  SKU_Master_Product
        fields = '__all__'

class WdSkuCatagorySerializers(serializers.ModelSerializer):
    class Meta:
        model =  WdSkuCatagory
        fields = '__all__'        

class SKUListSerializers(serializers.ModelSerializer):
    class Meta:
        model =  WdSkuCatagory
        fields = [
            'wd_id','wd_town_id','zone_code','zone','zone_code'
        ]

class Saless_Hierarchy_MasterSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Sales_Hierarchy_Master
        fields = '__all__' 

class WDmasterSerializers(serializers.ModelSerializer):
    class Meta:
        model =  WDmaster
        fields = '__all__' 

class BranchMasterSerializers(serializers.ModelSerializer):
    class Meta:
        model =  BranchMaster
        fields = '__all__'

class Integration_log_summarySerializers(serializers.ModelSerializer):
    class Meta:
        model =  Integration_log_summary
        fields = '__all__'                    


class Integration_log_detailsSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Integration_log_details
        fields = '__all__'                    
class Repeat_countSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Repeat_count
        fields = '__all__'
        
        
class Invalid_log_dataSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Invalid_log_data
        fields = '__all__'
