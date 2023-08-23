import datetime
from django.db.models import fields
from rest_framework.relations import ManyRelatedField
from base.models import *
from base.serializers import UserSerializers
from master.models import Archived_SalesData, SKU_Master_Product, Sales_Hierarchy_Master, SalesData, WdSkuCatagory
from rest_framework import serializers

from master.serializers import SKU_Master_ProductSerializers



class Archived_SalesData_Serializer(serializers.ModelSerializer):
    class Meta:
        model =  Archived_SalesData
        fields = "__all__"

class SKU_Master_ProductSerializer(serializers.ModelSerializer):
    # sales = serializers.SerializerMethodField()
    class Meta:
        model =  SKU_Master_Product
        fields = ['sku_id','sku_code','sku_short_name','sku_name','category_code','category_name','weight_uom_code','status']

    # def get_sales(self, obj):


class WdSkuCatagorySerializer(serializers.ModelSerializer):
    sku_productcts = serializers.SerializerMethodField()
    class Meta:
        model =  WdSkuCatagory
        fields = ['sku_code', 'sku_id','wd_town_id','status','sku_productcts']

    def get_sku_productcts(self, obj):
        master_data = SKU_Master_Product.objects.filter(sku_code = obj.sku_code).distinct()
        return SKU_Master_ProductSerializer(master_data, many = True).data




class WDmasterSerializer(serializers.ModelSerializer):
    wd_profile = serializers.SerializerMethodField()
    class Meta:
        # model =  WDmaster
        fields = ['wd_id','wd_name','wd_city','wd_postal_code','wd_state','wd_profile']
    def get_wd_profile(self, obj):
        wduser_data = User.objects.filter(email = obj.wd_id)
        return UserSerializers(wduser_data, many = True).data

class User_serializer(serializers.Serializer):
    wduser = serializers.SerializerMethodField()
    class Meta:
        model =  User
        fields = ['id','username', 'email',"user_type",'first_login','lock_unlock','wduser']

    def get_wduser(self, obj):
        wduser_details = WDmaster.objects.filter(wd_id = obj.id)
        return WDmasterSerializer(wduser_details, many = True).data

class Sales_Hierarchy_MasterSerializer(serializers.ModelSerializer):
    wduser_details = serializers.SerializerMethodField()
    
    class Meta:
        model =  Sales_Hierarchy_Master
        fields = ['wd_id','region_code','wd_town_id','region','town','wduser_details']
    def get_wduser_details(self, obj):
        wduser_data = User.objects.filter(username = obj.region)
        return User_serializer(wduser_data, many = True).data


class BranchMasterSerializers(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField()
    class Meta:
        model =  BranchMaster
        fields = ['branch_id','branch_name','branch_city','region','branch_code','branch']

    def get_branch(self, obj):
        region_name = Sales_Hierarchy_Master.objects.filter(region = obj.region).distinct()
        return Sales_Hierarchy_MasterSerializer(region_name, many = True).data


class Sales_Hierarchy_MasterSerializers(serializers.ModelSerializer):
    wd_name = serializers.SerializerMethodField()
    lock_unlock = serializers.SerializerMethodField()
    region_code = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    town = serializers.SerializerMethodField()
    town_code = serializers.SerializerMethodField()
    class Meta:
        model =  Sales_Hierarchy_Master
        fields = ['id','wd_id','region_code','region','town_code','town','wd_name','lock_unlock']
    # def get_wd_name(self, obj):
    #     wd_name=WDmaster.objects.filter(wd_ids=obj['wd_id']).last()
    #     if wd_name:
    #         return wd_name.wd_name
    #     return ''
    def get_lock_unlock(self, obj):
        wd = User.objects.filter( user_id= obj['wd_id']).last()
        if wd:
            return wd.lock_unlock
        return ''
    def get_region_code(self, obj):
        reg_obj=Sales_Hierarchy_Master.objects.filter(wd_id=obj['wd_id']).last()
        if reg_obj:
            return reg_obj.region_code
        return ''
    def get_region(self, obj):
        reg_obj=Sales_Hierarchy_Master.objects.filter(wd_id=obj['wd_id']).last()
        if reg_obj:
            return reg_obj.region
        return ''

    def get_town(self, obj):
        reg_obj=Sales_Hierarchy_Master.objects.filter(wd_id=obj['wd_id']).last()
        if reg_obj:
            return reg_obj.town
        return ''

    def get_town_code(self, obj):
        reg_obj=Sales_Hierarchy_Master.objects.filter(wd_id=obj['wd_id']).last()
        if reg_obj:
            return reg_obj.town_code
        return ''


class SKU_Master_ProductsSerializer(serializers.ModelSerializer):
    # sales = serializers.SerializerMethodField()
    class Meta:
        model =  SKU_Master_Product
        fields = ['id','sku_id','sku_code','sku_short_name','sku_name']


class UserssSerializer(serializers.ModelSerializer):
    # sales = serializers.SerializerMethodField()
    class Meta:
        model =  User
        fields = ['profile_pic']


class UserSerialize_getWDMaster(serializers.ModelSerializer):
    wd_name = serializers.SerializerMethodField()
    wd_id = serializers.SerializerMethodField()
    lock_unlock = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    wd_source = serializers.SerializerMethodField()
    sm_state = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    locationcode = serializers.SerializerMethodField()
    town = serializers.SerializerMethodField()
     
    class Meta:
        model =  WDmaster
        fields = ['wd_name','wd_ids','wd_id','first_name','user_id','locationcode','lock_unlock','region','town','wd_source','sm_state', 'wd_type']

    def get_locationcode(self, obj):
        data = User.objects.filter(user_id = obj.wd_ids).last()
        return data.locationcode
    def get_region(self, obj):
        data = User.objects.filter(user_id = obj.wd_ids).last()
        return data.locationcode
    def get_town(self, obj):
       
        return obj.wd_postal_code
    
    def get_wd_id(self, obj):
        # data = User.objects.filter(user_id = obj.wd_id).last()
        return obj.wd_ids
    
    def get_wd_name(self, obj):
        data = User.objects.filter(user_id = obj.wd_ids).last()
        return data.first_name

    def get_user_id(self, obj):
        data = User.objects.filter(user_id = obj.wd_ids).last()
        return data.user_id

    def get_lock_unlock(self, obj):
        wd = User.objects.filter( user_id= obj.wd_ids).last()
        if wd:
            return wd.lock_unlock
        return ''
    def get_first_name(self, obj):
        data = User.objects.filter(user_id = obj.wd_ids).last()
        return data.first_name
    
    def get_wd_source(self, obj):
        # wd = WDmaster.objects.filter( wd_ids__iexact= obj.wd_id).last()
        # if wd:
        #     return wd.wd_type
        return obj.wd_type
    
    def get_sm_state(self, obj):
        # wd = WDmaster.objects.filter( wd_ids= obj.wd_id).last()
        # if wd:
        # return ''
        return obj.wd_state


class UserSerialize_getWD(serializers.ModelSerializer):
    wd_name = serializers.SerializerMethodField()
    wd_id = serializers.SerializerMethodField()
    lock_unlock = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    town = serializers.SerializerMethodField()
    wd_source = serializers.SerializerMethodField()
    sm_state = serializers.SerializerMethodField()
    
    class Meta:
        model =  User
        fields = ['wd_name','wd_id','first_name','user_id','locationcode','lock_unlock','region','town','wd_source','sm_state']

    def get_wd_name(self, obj):
        data = User.objects.filter(user_id = obj['user_id']).last()
        return data.first_name

    def get_wd_id(self, obj):
        data = User.objects.filter(user_id = obj['user_id']).last()
        return data.user_id

    def get_lock_unlock(self, obj):
        wd = User.objects.filter( user_id= obj['user_id']).last()
        if wd:
            return wd.lock_unlock
        return ''
    
    def get_region(self, obj):
        wd = Sales_Hierarchy_Master.objects.filter( wd_id= obj['user_id'], region_code= obj['locationcode']).last()
        if wd:
            return wd.region
        return ''

    def get_town(self, obj):
        wd = Sales_Hierarchy_Master.objects.filter( wd_id= obj['user_id'],region_code= obj['locationcode']).last()
        if wd:
            return wd.town
        return "No town"

    def get_wd_source(self, obj):
        wd = WDmaster.objects.filter( wd_ids__iexact= obj['user_id']).last()
        if wd:
            return wd.wd_type
        return ''

    def get_sm_state(self, obj):
        wd = WDmaster.objects.filter( wd_ids= obj['user_id']).last()
        if wd:
            return wd.wd_state
        return ''

class UserSerializeID_Name(serializers.ModelSerializer):
    wd_name = serializers.SerializerMethodField()
    wd_id = serializers.SerializerMethodField()
    
    class Meta:
        model =  User
        fields = ['wd_name','wd_id','first_name']

    def get_wd_name(self, obj):
        data = User.objects.filter(user_id = obj['user_id']).last()
        return data.first_name

    def get_wd_id(self, obj):
        data = User.objects.filter(user_id = obj['user_id']).last()
        return data.user_id

class Usrer_serializer_town(serializers.ModelSerializer):
    town = serializers.SerializerMethodField()
    class Meta:
        model =  User
        fields = ['first_name','user_id','town']

    def get_town(sell,obj):
        print(obj,"-----------")
        # for i in obj:
        # print(i,"=====i======")
        wd_list_data = Sales_Hierarchy_Master.objects.filter(wd_id = obj['user_id']).last()
        if wd_list_data:
            return wd_list_data.town
            # return None

class WDmaster_wd_town(serializers.ModelSerializer):
    town = serializers.SerializerMethodField()
    town_code = serializers.SerializerMethodField()
    class Meta:
        model =  WDmaster
        fields = ['town','town_code']

    def get_town(self, obj):
        return obj.wd_postal_code

    def get_town_code(self, obj):
        print(obj.wd_postal_code,"=======serializer======")
        town_code = Sales_Hierarchy_Master.objects.filter(town = obj.wd_postal_code).last()
        if town_code:
            return town_code.town_code
        else:
            return ""
        # print(str(obj.wd_postal_code),"=================serializer======")
        # # a = str(obj.wd_postal_code).split('-')[1]
        # if len(str(obj.wd_postal_code).split('-'))>1 :
        #     return (str(obj.wd_postal_code)).split('-')[1]
        # else:
        #     return ""
        
        
        
class WDmaster_wd_towns(serializers.ModelSerializer):
    town = serializers.SerializerMethodField()
    town_code = serializers.SerializerMethodField()
    class Meta:
        model =  WDmaster
        fields = ['town','town_code']

    def get_town(self, obj):
        # print(obj['wd_postal_code'],"=======serializer======")
        return obj['wd_postal_code']

    def get_town_code(self, obj):
        town_code = Sales_Hierarchy_Master.objects.filter(town__iexact = obj['wd_postal_code']).last()
        if town_code:
            return town_code.town_code
        else:
            return ""
        # breakpoint()
        # print(str(obj.wd_postal_code),"=================serializer======")
        # a = str(obj.wd_postal_code).split('-')[1]
        # if len(str(obj['wd_postal_code']).split('-'))>1 :
        #     return str(obj['wd_postal_code']).split('-')[1]
        # else:
        #     return ""
        
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields ='__all__'
    
    
class SalesSerializer(serializers.ModelSerializer):
    SalesData = serializers.SerializerMethodField()
    class Meta:
        model= SKU_Master_Product 
        fields = ['sku_id','sku_code','sku_short_name','sku_name','SalesData']
    
    def get_SalesData(self, obj):
        sales_objects = self.context.get('sales_objects')
        town_id_list = self.context.get('town_id_list')
        print(sales_objects,"================sales_objects--------serializ")
        
        try:
            start = datetime.datetime.now()
            sale_obj = sales_objects.filter(sku_id = obj['sku_id'],town_id__in = town_id_list).values()
            ex_time = (datetime.datetime.now()-start)
            print(ex_time,"========ex_time------serializer")
            if sale_obj:
                return sale_obj
            else:
                return [{}]
        except:
            return [{}]
        

class SaleSaveUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model= SalesData
        fields = '__all__'