from rest_framework import serializers
from base.models import Access_log, Attendence, BranchMaster
from master.models import *


class SalesDataSerialize(serializers.ModelSerializer):
    total_retail = serializers.SerializerMethodField()
    toatal_Dealer = serializers.SerializerMethodField()
    total_Howker = serializers.SerializerMethodField()
    total_Modern_Trade_Sales = serializers.SerializerMethodField()
    
    class Meta:
        model =  SalesData
        fields = [
                    'region','town_name','wd_name','wd_id','brand_category','sku_code','sku_short_name','sales_date_time',
                    'local_sales_retail','local_sales_dealer','local_sales_modern_trade','local_sales_hawker',
                    'outstation_sales_reatil','outstation_sales_dealer','outstation_sales_modern_trade','outstation_sales_hawker',
                    'other_sales_retail','other_sales_dealer','other_sales_modern_trade',
                                        
                    'total_retail','toatal_Dealer','total_Modern_Trade_Sales','total_Howker',
                    'total_local_sales','total_outstation_sales','grand_total',
                    'other_issues_damage','other_issues_return','other_issues_other','total_issue','wd_type'
                ]
    def get_total_retail(self, obj):
        # print(obj['wd_type'],"=================")
        total_retail = float(obj['local_sales_retail'])+float(obj['outstation_sales_reatil'])+float(obj['other_sales_retail'])
        return total_retail
    
    def get_toatal_Dealer(self, obj):
        total_retail = float(obj['local_sales_dealer'])+float(obj['outstation_sales_dealer'])+float(obj['other_sales_dealer'])
        return total_retail
    
    def get_total_Howker(self, obj):
        total_retail = float(obj['local_sales_hawker'])+float(obj['outstation_sales_hawker'])
        return total_retail
    
    def get_total_Modern_Trade_Sales(self, obj):
        total_retail = float(obj['local_sales_modern_trade'])+float(obj['other_sales_modern_trade'])+float(obj['outstation_sales_modern_trade'])
        return total_retail


class SalesDataSerialize_WD(serializers.ModelSerializer):
    total_retail = serializers.SerializerMethodField()
    toatal_Dealer = serializers.SerializerMethodField()
    total_Howker = serializers.SerializerMethodField()
    total_Modern_Trade_Sales = serializers.SerializerMethodField()
    
    class Meta:
        model =  SalesData
        fields = [
                    # 'wd_name','wd_type','town_id'
                    'region','statename','town_name','wd_name',
                    # 'wd_type',
                    'wd_id',
                    # 'town_id',
                    'brand_category','sku_code','sku_short_name','sales_date_time',
                    'local_sales_retail','local_sales_dealer','local_sales_modern_trade','local_sales_hawker',
                    'outstation_sales_reatil','outstation_sales_dealer','outstation_sales_modern_trade','outstation_sales_hawker',
                    'other_sales_retail','other_sales_dealer','other_sales_modern_trade',
                                        
                    'total_retail','toatal_Dealer','total_Modern_Trade_Sales','total_Howker',
                    'total_local_sales','total_outstation_sales',
                    # 'total_other_sales'
                    'grand_total',
                    'other_issues_damage','other_issues_return','other_issues_other','total_issue','wd_type'
                    
                ]
    def get_total_retail(self, obj):
        # print(obj['wd_type'],"=========['total_other_sales']===================")
        total_retail = round((float(obj['local_sales_retail'])+float(obj['outstation_sales_reatil'])+float(obj['other_sales_retail'])),2)
        return total_retail
    
    def get_toatal_Dealer(self, obj):
        total_retail = round((float(obj['local_sales_dealer'])+float(obj['outstation_sales_dealer'])+float(obj['other_sales_dealer'])),2)
        return total_retail
    
    def get_total_Howker(self, obj):
        total_retail = round((float(obj['local_sales_hawker'])+float(obj['outstation_sales_hawker'])),2)
        return total_retail
    
    def get_total_Modern_Trade_Sales(self, obj):
        total_retail = round((float(obj['local_sales_modern_trade'])+float(obj['other_sales_modern_trade'])+float(obj['outstation_sales_modern_trade'])),2)
        return total_retail





# WD_SalesDataSerialize for WD================================================

class WD_SalesDataSerialize(serializers.ModelSerializer):
    total_retail = serializers.SerializerMethodField()
    toatal_Dealer = serializers.SerializerMethodField()
    total_Howker = serializers.SerializerMethodField()
    total_Modern_Trade_Sales = serializers.SerializerMethodField()
    
    class Meta:
        model =  SalesData
        fields = [
                    # 'wd_name','wd_type','town_id'
                    # 'wd_name','wd_id',
                    'town_name','statename','wd_name','wd_id','brand_category','sku_code','sku_short_name','sales_date_time',
                    'local_sales_retail','local_sales_dealer','local_sales_modern_trade','local_sales_hawker',
                    'outstation_sales_reatil','outstation_sales_dealer','outstation_sales_modern_trade','outstation_sales_hawker',
                    'other_sales_retail','other_sales_dealer','other_sales_modern_trade',
                    
                    'total_retail','toatal_Dealer','total_Modern_Trade_Sales','total_Howker',
                    'total_local_sales','total_outstation_sales',
                    # 'total_other_sales'
                    'grand_total',
                    'other_issues_damage','other_issues_return','other_issues_other','total_issue',
                    'wd_type'
                ]
    def get_total_retail(self, obj):
        # print(obj,"=========['total_other_sales']===================")
        total_retail = float(obj['local_sales_retail'])+float(obj['outstation_sales_reatil'])+float(obj['other_sales_retail'])
        return total_retail
    
    def get_toatal_Dealer(self, obj):
        total_retail = float(obj['local_sales_dealer'])+float(obj['outstation_sales_dealer'])+float(obj['other_sales_dealer'])
        return total_retail
    
    def get_total_Howker(self, obj):
        total_retail = float(obj['local_sales_hawker'])+float(obj['outstation_sales_hawker'])
        return total_retail
    
    def get_total_Modern_Trade_Sales(self, obj):
        total_retail = float(obj['local_sales_modern_trade'])+float(obj['other_sales_modern_trade'])+float(obj['outstation_sales_modern_trade'])
        return total_retail
    
    
    
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> WEEKLYREPORT

class WeeklyDataSerialize(serializers.ModelSerializer):
    total_retail = serializers.SerializerMethodField()
    toatal_Dealer = serializers.SerializerMethodField()
    total_Howker = serializers.SerializerMethodField()
    total_Modern_Trade_Sales = serializers.SerializerMethodField()
    sales_date_time = serializers.SerializerMethodField()
    
    class Meta:
        model =  SalesData
        fields = [
                    'region','statename','town_name','wd_name','wd_id','brand_category','sku_code','sku_short_name','sales_date_time','transaction_type',
                    'local_sales_retail','local_sales_dealer','local_sales_modern_trade','local_sales_hawker',
                    'outstation_sales_reatil','outstation_sales_dealer','outstation_sales_modern_trade','outstation_sales_hawker',
                    'other_sales_retail','other_sales_dealer','other_sales_modern_trade',
                                        
                    'total_retail','toatal_Dealer','total_Modern_Trade_Sales','total_Howker',
                    'total_local_sales','total_outstation_sales','grand_total',
                    'other_issues_damage','other_issues_return','other_issues_other','total_issue','wd_type','town_name','town_code','sales_date_time'
                ]
        
    def get_total_retail(self, obj):
        # print(obj['wd_type'],"=================")
        total_retail = float(obj['local_sales_retail'])+float(obj['outstation_sales_reatil'])+float(obj['other_sales_retail'])
        return total_retail
    
    def get_toatal_Dealer(self, obj):
        total_retail = float(obj['local_sales_dealer'])+float(obj['outstation_sales_dealer'])+float(obj['other_sales_dealer'])
        return total_retail
    
    def get_total_Howker(self, obj):
        total_retail = float(obj['local_sales_hawker'])+float(obj['outstation_sales_hawker'])
        return total_retail
    
    def get_total_Modern_Trade_Sales(self, obj):
        # print(obj.transaction_type)
        
        total_retail = float(obj['local_sales_modern_trade'])+float(obj['other_sales_modern_trade'])+float(obj['outstation_sales_modern_trade'])
        return total_retail


    def get_sales_date_time(self,obj):
        if obj['transaction_type'] == "Week4" :
            print(obj ['transaction_type'],'jjjjjjjjjjjjjjjjjjjjjjjj')
            data=(obj['sales_date_time'])
            d=str(data)
            print(data,'aaaaaa')

            
            datee = datetime.datetime.strptime(d, "%Y-%m-%d")
            daa=str(datee.year)+"-"+str(datee.month)+"-"+"28"
            return daa
        
        else:
            return (obj['sales_date_time'])
            
            

#>>>>>>>>>>>>WD weekly report serializer



class WD_WeeklyDataSerialize(serializers.ModelSerializer):
    total_retail = serializers.SerializerMethodField()
    toatal_Dealer = serializers.SerializerMethodField()
    total_Howker = serializers.SerializerMethodField()
    total_Modern_Trade_Sales = serializers.SerializerMethodField()
    
    class Meta:
        model =  SalesData
        fields = [
                    # 'wd_name','wd_type','town_id'
                    # 'wd_name','wd_id',
                    'region','statename','town_name','wd_name','wd_id','brand_category','sku_code','sku_short_name','sales_date_time',
                    'local_sales_retail','local_sales_dealer','local_sales_modern_trade','local_sales_hawker',
                    'outstation_sales_reatil','outstation_sales_dealer','outstation_sales_modern_trade','outstation_sales_hawker',
                    'other_sales_retail','other_sales_dealer','other_sales_modern_trade',
                    
                    'total_retail','toatal_Dealer','total_Modern_Trade_Sales','total_Howker',
                    'total_local_sales','total_outstation_sales',
                    # 'total_other_sales'
                    'grand_total',
                    'other_issues_damage','other_issues_return','other_issues_other','total_issue',
                    'wd_type','town_code','transaction_type'
                ]
    def get_total_retail(self, obj):
        # print(obj,"=========['total_other_sales']===================")
        total_retail = float(obj['local_sales_retail'])+float(obj['outstation_sales_reatil'])+float(obj['other_sales_retail'])
        return total_retail
    
    def get_toatal_Dealer(self, obj):
        total_retail = float(obj['local_sales_dealer'])+float(obj['outstation_sales_dealer'])+float(obj['other_sales_dealer'])
        return total_retail
    
    def get_total_Howker(self, obj):
        total_retail = float(obj['local_sales_hawker'])+float(obj['outstation_sales_hawker'])
        return total_retail
    
    def get_total_Modern_Trade_Sales(self, obj):
        total_retail = float(obj['local_sales_modern_trade'])+float(obj['other_sales_modern_trade'])+float(obj['outstation_sales_modern_trade'])
        return total_retail




class AttendenceSerializer(serializers.ModelSerializer):
    wd_id=serializers.SerializerMethodField()
    wd_name=serializers.SerializerMethodField()
    branch_name=serializers.SerializerMethodField()
    town_code=serializers.SerializerMethodField()
    town_name=serializers.SerializerMethodField()
    login_date=serializers.SerializerMethodField()


    class Meta:
        # model =  SalesData
        model=Attendence
        fields=['wd_id','wd_name','statename','branch_name','town_code',"town_name",'login_date']



    def get_wd_id(self,obj):
        return obj.user_id

    def get_wd_name(self,obj):
        wd_name=User.objects.filter(user_id=obj.user_id).last()
        return wd_name.first_name
      
    def get_branch_name(self,obj):
        user=User.objects.filter(user_id=obj.user_id).last()
        branch=BranchMaster.objects.filter(branch_code=user.locationcode).last()
        return branch.branch_name + " - "+(branch.region)

    def get_town_code(self,obj):
        town_data=Sales_Hierarchy_Master.objects.filter(wd_id=obj.user_id).last()
        return town_data.town_code
    
    def get_town_name(self,obj):
        town_data=Sales_Hierarchy_Master.objects.filter(wd_id=obj.user_id).last()
        return town_data.town

    def get_login_date(self,obj):
        return obj.added_on.strftime("%d-%m-%Y %I:%M %p")
    

class AccessSerializer(serializers.ModelSerializer):
    wd_id=serializers.SerializerMethodField()
    wd_name=serializers.SerializerMethodField()
    branch_name=serializers.SerializerMethodField()
    town_code=serializers.SerializerMethodField()
    town_name=serializers.SerializerMethodField()
    sales_save_date=serializers.SerializerMethodField()
    date_time = serializers.SerializerMethodField()

    class Meta:
        # model =  SalesData
        model=Access_log
        fields=['wd_id','wd_name','statename','branch_name','town_code',"town_name",'sales_save_date','date_time']



    def get_wd_id(self,obj):
        return obj.user_id

    def get_wd_name(self,obj):
        wd_name=User.objects.filter(user_id=obj.user_id).last()
        return wd_name.first_name
      
    def get_branch_name(self,obj):
        user=User.objects.filter(user_id=obj.user_id).last()
        branch=BranchMaster.objects.filter(branch_code=user.locationcode).last()
        return branch.branch_name + " - "+(branch.region)

    def get_town_code(self,obj):
        town_data=Sales_Hierarchy_Master.objects.filter(wd_id=obj.user_id).last()
        return town_data.town_code
    
    def get_town_name(self,obj):
        town_data=Sales_Hierarchy_Master.objects.filter(wd_id=obj.user_id).last()
        return town_data.town

    def get_sales_save_date(self,obj):
        return obj.sales_save_date.strftime("%d-%m-%Y")
    
    def get_date_time(self, obj):
        if obj and obj.updated_on:
            return obj.updated_on.strftime("%d-%m-%Y %I:%M %p")
        else:
            return obj.created_at.strftime("%d-%m-%Y %I:%M %p")