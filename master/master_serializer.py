from django.db.models import Q
import json
import pandas as pd
from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from django.contrib.auth.hashers import make_password,check_password
from base.models import *
from master.models import *
import re

### user master upload=================================================
class MasterUserCSVFileUploadFieldagentSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[FileExtensionValidator( ['CSV',] ) ])
    error_msg = serializers.ListField(read_only=True)
    
    class Meta:
        ref_name = 'masteruser_upload'

    def validate(self, data):
        # role_id = self.context.get('request').user
        file = data.get('file')
        csv_record = pd.read_csv(file,dtype=object) 
        # Validation of csv format with column name==================start===>
        list_of_column_names = list(csv_record.columns)
        print("file_list","====fl",csv_record)
        wrong_columns = 0
        

        
        # print(data.get('role'),"====================",role_id)
        
        column = ['USER_ID','NAME','LOCATION','USER_TYPE']
        for columns in list_of_column_names:
            if columns not in column:
                wrong_columns = wrong_columns + 1
        if len(column) != len(list_of_column_names) or wrong_columns > 0:
            raise serializers.ValidationError({'error' : ('CSV File format is wrong.Please check and correct.')})
        
        

        row_count = len(csv_record)
        file_list = csv_record.values.tolist()
        exist_user = []
        with_remark = []
        user_detail = None
        user = None
        df_2_json = csv_record.to_json(orient='records')
        df_2_json = json.loads(df_2_json)
        if not df_2_json:
            raise serializers.ValidationError({'error' : ('There is no data in this CSV.')})
        for row in df_2_json:
            print(str(row['LOCATION']),"=========>>===",file)
            # breakpoint()
            validlocationcode = row['LOCATION'] if len(str(row['LOCATION']))==2 else None
         
                
                
                
            wd_bu_user = User.objects.filter(user_id = row['USER_ID'])
            if not wd_bu_user and validlocationcode and  row['NAME'] and row['LOCATION'] and row['USER_TYPE']:
                if str(row['USER_TYPE']).upper() == 'W':
                    create_user = User()
                    create_user.password = make_password("wpassword@123")
                    create_user.user_id = str(row['USER_ID'])
                    create_user.email = str(row['USER_ID'])+"@ssgpi.com"
                    create_user.user_type = "WD" if str(row['USER_TYPE']).upper() == 'W' else None
                    create_user.username = row['USER_ID']
                    create_user.locationcode = str(row['LOCATION'])
                    create_user.first_name = row['NAME']
                    create_user.save()
                    row['Remasks'] = "Create Success as WD."
                elif str(row['USER_TYPE']).upper() == 'B':
                    create_user = User()
                    create_user.password = make_password("bpassword@123")
                    create_user.user_id = str(row['USER_ID'])
                    create_user.email = str(row['USER_ID'])+"@ssgpi.com"
                    create_user.user_type = "BRANCH USER" if str(row['USER_TYPE']).upper() == 'B' else None
                    create_user.username = row['USER_ID']
                    create_user.locationcode = str(row['LOCATION'])
                    create_user.first_name = row['NAME']
                    create_user.save()
                    row['Remasks'] = "Create Success as BRANCH USER."
            elif wd_bu_user:
                row['Remasks'] = "User already exist."
            elif not validlocationcode:
                row['Remasks'] = "Please enter valid location code"

            elif not row['NAME'] or row['LOCATION'] or row['LOCATION'] or row['USER_TYPE']:
                row['Remasks'] = "'USER_ID','USER_TYPE','LOCATION','USER_TYPE',This fields are should be mandatory."

            with_remark.append(row)
        data['error_msg'] = with_remark
        return data


class WdMasterCSVFileUploadFieldagentSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[FileExtensionValidator( ['CSV',] ) ])
    error_msg = serializers.ListField(read_only=True)
    
    class Meta:
        ref_name = 'wdmaster_uplod'

    def validate(self, data):
        # role_id = self.context.get('request').user
        file = data.get('file')
        # csv_record = pd.read_csv(file, dtype=object) 
        csv_record = pd.read_csv(file, dtype=object) 
        
        # Validation of csv format with column name==================start===>
        list_of_column_names = list(csv_record.columns)
        wrong_columns = 0
        # password  = "Password@123" ### common password every user
        
        
        # print(data.get('role'),"====================",role_id)
        
        column = ['WD_ID','WD_NAME','WD_ADDRESS1','WD_ADDRESS2','TOWN','WD_POSTAL_CODE','WD_STATE','WD_COUNTRY_ID','WD_TYPE']
        for columns in list_of_column_names:
            if columns not in column:
                wrong_columns = wrong_columns + 1
        if len(column) != len(list_of_column_names) or wrong_columns > 0:
            raise serializers.ValidationError({'error' : ('CSV File format is wrong.Please check and correct.')})
        

        row_count = len(csv_record)
        file_list = csv_record.values.tolist()
        exist_user = []
        with_remark = []
        user_detail = None
        user = None
        df_2_json = csv_record.to_json(orient='records')
        df_2_json = json.loads(df_2_json)
        if not df_2_json:
            raise serializers.ValidationError({'error' : ('There is no data in this CSV.')})
        
        for row in df_2_json:
            wd_master = User.objects.filter(user_id = str(row['WD_ID']))
            user_master = WDmaster.objects.filter(wd_ids = str(row['WD_ID']),wd_postal_code = str(row['TOWN']))
            if wd_master and not user_master and row['WD_ID'] and row['WD_NAME'] and row['WD_ADDRESS1'] and row['TOWN'] and row['WD_POSTAL_CODE'] and row['WD_STATE'] and row['WD_COUNTRY_ID'] and row['WD_TYPE']:
                print("===========")
                # breakpoint()
                create_wd_master = WDmaster()
                create_wd_master.wd_ids = row['WD_ID']
                create_wd_master.wd_name = row['WD_NAME']
                create_wd_master.wd_address1 = row['WD_ADDRESS1']
                create_wd_master.wd_address2 = row['WD_ADDRESS2']
                create_wd_master.wd_address3 = row['WD_ADDRESS1']
                create_wd_master.wd_address4 = row['WD_ADDRESS2']
                create_wd_master.wd_postal_code = row['TOWN']
                create_wd_master.wd_state = row['WD_STATE']
                create_wd_master.wd_city = row['WD_POSTAL_CODE']
                create_wd_master.wd_country = row['WD_COUNTRY_ID']
                create_wd_master.wd_type = row['WD_TYPE']
                
                create_wd_master.save()
                row['Remasks'] = "Create Success."
            elif user_master:
                row['Remasks'] = "Already exists."
            elif not wd_master:
                row['Remasks'] = "User not exist in user master."
            elif (not row['WD_ID']) or (not row['WD_NAME']) or (not row['WD_ADDRESS1']) or (not row['WD_ADDRESS2']) or (not row['TOWN']) or (not row['WD_POSTAL_CODE']) or (not row['WD_STATE']) or (not row['WD_COUNTRY_ID']) or (not row['WD_TYPE']) :
                row['Remasks'] = "Please try to fill all fields."

            with_remark.append(row)
        data['error_msg'] = with_remark
        return data

class HeirarchymasterMasterCSVFileUploadFieldagentSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[FileExtensionValidator( ['CSV',] ) ])
    error_msg = serializers.ListField(read_only=True)
    
    class Meta:
        ref_name = 'heirarchy_master_upload'

    def validate(self, data):
        file = data.get('file')
        csv_record = pd.read_csv(file,dtype=object)
        # Validation of csv format with column name==================start===>
        list_of_column_names = list(csv_record.columns)
        wrong_columns = 0
        
        column = ['WD_ID','WD_TOWN_ID','REGION_CODE','REGION','TOWN','TOWN_CODE','SKU_CATEGORY_CODE','WD_TOWN_CODE']
        for columns in list_of_column_names:
            print("=====",columns)
            if columns not in column:
                wrong_columns = wrong_columns + 1
        if len(column) != len(list_of_column_names) or wrong_columns > 0:
            raise serializers.ValidationError({'error' : ('CSV File format is wrong.Please check and correct.')})
        
        
        
        row_count = len(csv_record)
        file_list = csv_record.values.tolist()
        exist_user = []
        with_remark = []
        user_detail = None
        user = None
        df_2_json = csv_record.to_json(orient='records')
        df_2_json = json.loads(df_2_json)
        if not df_2_json:
            raise serializers.ValidationError({'error' : ('There is no data in this CSV.')})
        
        for row in df_2_json:
            print(row,df_2_json,'pppppp')
            town_data=str(row['TOWN'])
            town_len=town_data.split('-')
            valid_town = True if len(town_len) == 2 else None
            wd_check=None
            splitted_code=[]
            # print('aaa=====================================',splitted_code,town_len[1],valid_town,str(row['TOWN_CODE']))
            
            if valid_town and town_len[1]==str(row['TOWN_CODE']):
                wd_check=WDmaster.objects.filter(wd_ids=str(row['WD_ID']),wd_postal_code__icontains=town_len[1])
                splitted_code=[town_len[1],re.sub('\W+','',town_len[1]),str(town_len[1]),str(town_len[1])[1:],'0'+str(town_len[1])]
                
            print(splitted_code,wd_check,'gggggggggggg')
            user = User.objects.filter(user_id = str(row['WD_ID']))
            wd_master = WDmaster.objects.filter(wd_ids = str(row['WD_ID']))
            heirarchy_master = Sales_Hierarchy_Master.objects.filter(wd_id = str(row['WD_ID']),town_code = str(row['TOWN_CODE']),town = str(row['TOWN']), wd_town_id = str(row['WD_TOWN_ID']))
            check_town_exist = Sales_Hierarchy_Master.objects.filter(wd_id = str(row['WD_ID']),town_code__in = splitted_code,town = str(row['TOWN']))
            town_id_list=check_town_exist.values_list('wd_town_id',flat=True)
            check_town_exist=check_town_exist.last()
            town_id_list_check=row['WD_TOWN_ID'] if row['WD_TOWN_ID'] not in town_id_list else None
            # check_town_ids = check_town_exist.filter(town = str(row['TOWN']))
            # check_town_exist = check_town_exist.last()
            print(heirarchy_master,'ddddddddddd','check_town_ids',wd_master,'llllll',check_town_exist)
            
            if wd_master and user  and (not heirarchy_master) and (not check_town_exist) and town_id_list_check and row['WD_ID'] and valid_town and wd_check and row['WD_TOWN_ID'] and row['REGION_CODE'] and row['REGION'] and row['TOWN'] and row['TOWN_CODE'] and row['SKU_CATEGORY_CODE']:
                # print("==========>>>=")
                print('>>>>>>>>>>>>>>>>666666666666666666>>>>>>>>>>>>>>>>>>>>>>>>>')

                heirarchy_master = Sales_Hierarchy_Master()
                heirarchy_master.wd_id = str(row['WD_ID'])
                heirarchy_master.town_code = str(row['TOWN_CODE'])
                heirarchy_master.wd_town_id = str(row['WD_TOWN_ID'])
                heirarchy_master.town = str(row['TOWN'])
                heirarchy_master.region = str(row['REGION'])
                heirarchy_master.region_code = str(row['REGION_CODE'])
                heirarchy_master.sku_category_code = str(row['SKU_CATEGORY_CODE'])
                heirarchy_master.wd_town_code = str(row['WD_TOWN_CODE'])
                heirarchy_master.save()
                row['Remasks'] = "Create Success."
                print("========1==remark")
            # elif wd_master and user  and (not heirarchy_master and not check_town_ids) and check_town_exist and row['WD_ID'] and valid_town and wd_check and row['WD_TOWN_ID'] and row['REGION_CODE'] and row['REGION'] and row['TOWN'] and row['TOWN_CODE'] and row['SKU_CATEGORY_CODE']:
            elif wd_master and user  and (not heirarchy_master) and  check_town_exist and row['WD_ID'] and valid_town and wd_check and row['WD_TOWN_ID'] and row['REGION_CODE'] and row['REGION'] and row['TOWN'] and row['TOWN_CODE'] and row['SKU_CATEGORY_CODE']:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                # print(heirarchy_master,'ddddddddddd',check_town_ids)
                heirarchy_master_up = Sales_Hierarchy_Master()
                heirarchy_master_up.wd_id = str(row['WD_ID'])
                heirarchy_master_up.town_code = check_town_exist.town_code if check_town_exist else str(row['TOWN_CODE'])
                heirarchy_master_up.wd_town_id = str(row['WD_TOWN_ID'])
                heirarchy_master_up.town = str(row['TOWN'])
                heirarchy_master_up.region = str(row['REGION'])
                heirarchy_master_up.region_code = str(row['REGION_CODE'])
                heirarchy_master_up.sku_category_code = str(row['SKU_CATEGORY_CODE'])
                heirarchy_master_up.wd_town_code = str(row['WD_TOWN_CODE'])
                heirarchy_master_up.save()
                row['Remasks'] = "Create Success."
                print("=======2===remark")
                # breakpoint()
                
            elif heirarchy_master:
                row['Remasks'] = "Already exist."
            # elif check_town_ids:
            #     print(check_town_ids,'uuuuu')
            #     row['Remasks'] = "Already exist.222"
            elif not valid_town:
                row['Remasks']="Not Valid Town"
            elif not wd_check:
                row['Remasks']="Given town should be same with WD Master Town"
            elif not user:
                row['Remasks'] = "This user not exist user master."
            elif not wd_master:
                row['Remasks'] = "WdMaster not exist."
            elif (not row['WD_ID']) or (not row['WD_TOWN_ID']) or (not row['REGION_CODE']) or (not row['REGION']) or (not row['TOWN']) or (not row['TOWN_CODE']) or (not row['SKU_CATEGORY_CODE']) or (not row['SKU_CATEGORY_CODE']):
                row['Remasks'] = "Please try to fill all fields."

            with_remark.append(row)
        data['error_msg'] = with_remark
        return data
    
    
class MasterWdSkuCategoryCSVFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[FileExtensionValidator( ['CSV',] ) ])
    error_msg = serializers.ListField(read_only=True)
    class Meta:
            ref_name = 'heirarchy_master_WDskuCategory_upload'
            
    def validate(self,data):
        file = data.get('file')
        csv_record = pd.read_csv(file,dtype=object)
        # Validation of csv format with column name==================start===>
        list_of_column_names = list(csv_record.columns)
        wrong_columns = 0
        
        column=['SKU_CODE','WD_TOWN_ID','SKU_ID','ACTIVE_FLAG','MAX(B.UNIT_PRICE)','CNF_NAME','CNF_ID','WD_ID','TOWN','REGION']
        for columns in list_of_column_names: 

            print(columns,"=======")
            if columns not in column:
                wrong_columns+=1
        if len(column) != len(list_of_column_names) or wrong_columns > 0:
            raise serializers.ValidationError({'error' : ('CSV File format is wrong.Please check and correct.')})
        
        row_count = len(csv_record)
        file_list = csv_record.values.tolist()
        exist_user = []
        with_remark = []
        user_detail = None
        df_2_json = csv_record.to_json(orient='records')
        df_2_json = json.loads(df_2_json)
        
        if not df_2_json:
            raise serializers.ValidationError({'error' : ('There is no data in this CSV.')})
        
        for row in df_2_json: 
            user = User.objects.filter(user_id = str(row['WD_ID']))           
            wd_master = WDmaster.objects.filter(wd_ids = str(row['WD_ID']))
            heirarchy_master = Sales_Hierarchy_Master.objects.filter(wd_id = str(row['WD_ID']),wd_town_id = str(row['WD_TOWN_ID']))
            skumappingmaster = WdSkuCatagory.objects.filter(sku_code=str(row['SKU_CODE']),wd_town_id=str(row['WD_TOWN_ID']),sku_id=str(row['SKU_ID']))

            skucode=str(row['SKU_CODE'])
            skuid=str(row['SKU_ID'])
            data_check=SKU_Master_Product.objects.filter(sku_id=skuid,sku_code=skucode) 
            if wd_master and user  and  heirarchy_master and (not skumappingmaster)  and row['WD_TOWN_ID'] and row['SKU_CODE'] and row['SKU_ID'] and row['CNF_ID'] and row['ACTIVE_FLAG'] and row['MAX(B.UNIT_PRICE)']:
                skumappingmaster=WdSkuCatagory()
                # skumappingmaster.wd_id = str(row['WD_ID'])
            
                skumappingmaster.sku_code=str(row['SKU_CODE'])
                skumappingmaster.wd_town_id=str(row['WD_TOWN_ID'])
                skumappingmaster.sku_id=str(row['SKU_ID'])
                skumappingmaster.cnf_id=str(row['CNF_ID'])
                skumappingmaster.active_flag=str(row['ACTIVE_FLAG'])
                skumappingmaster.last_price=str(row['MAX(B.UNIT_PRICE)'])
                skumappingmaster.save()
                
                if data_check:
                    row['Remarks'] = "Create Success."
                elif not data_check:
                    row['Remarks'] = "This sku id or sku code not exists in Sku Master, please provide with same sku id and code."
                    
                    
            elif not heirarchy_master:
                row['Remarks'] = "Heirarchy Master not exist with this town id."
            elif not user:
                row['Remarks'] = "This user not exist user master."
            elif not wd_master:
                row['Remarks'] = " Wd master not exist."
            elif skumappingmaster:
                skumappingmaster.update(status=1)
                row['Remarks'] = "skumappingmaster already exist."
            elif (not row['WD_ID']) or (not row['WD_TOWN_ID']) or (not row['REGION_CODE']) or (not row['REGION']) or (not row['TOWN']) :
                row['Remasks'] = "Please try to fill all fields."

            with_remark.append(row)
          
        data['error_msg'] = with_remark
        return data
    
              
                
class MasterWdSkuCategoryUpdateCSVFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[FileExtensionValidator( ['CSV',] ) ])
    error_msg = serializers.ListField(read_only=True)
    class Meta:
            ref_name = 'heirarchy_master_WDskuCategory_upload'
            
    def validate(self,data):
        file = data.get('file')
        csv_record = pd.read_csv(file,dtype=object)
        # Validation of csv format with column name==================start===>
        list_of_column_names = list(csv_record.columns)
        wrong_columns = 0
        
        column=['SKU_CODE','WD_TOWN_ID','SKU_ID','ACTIVE_FLAG','MAX(B.UNIT_PRICE)','CNF_NAME','CNF_ID','WD_ID','TOWN','REGION']
        for columns in list_of_column_names: 

            print(columns,"=======")
            if columns not in column:
                wrong_columns+=1
        if len(column) != len(list_of_column_names) or wrong_columns > 0:
            raise serializers.ValidationError({'error' : ('CSV File format is wrong.Please check and correct.')})
        
        row_count = len(csv_record)
        file_list = csv_record.values.tolist()
        exist_user = []
        with_remark = []
        user_detail = None
        df_2_json = csv_record.to_json(orient='records')
        df_2_json = json.loads(df_2_json)
        
        if not df_2_json:
            raise serializers.ValidationError({'error' : ('There is no data in this CSV.')})
        
        for row in df_2_json: 
            user = User.objects.filter(user_id = str(row['WD_ID']))           
            wd_master = WDmaster.objects.filter(wd_ids = str(row['WD_ID']))
            heirarchy_master = Sales_Hierarchy_Master.objects.filter(wd_id = str(row['WD_ID']),wd_town_id = str(row['WD_TOWN_ID']))
            skumappingmaster = WdSkuCatagory.objects.filter(sku_code=str(row['SKU_CODE']),wd_town_id=str(row['WD_TOWN_ID']),sku_id=str(row['SKU_ID']))

            skucode=str(row['SKU_CODE'])
            skuid=str(row['SKU_ID'])
            data_check=SKU_Master_Product.objects.filter(sku_id=skuid,sku_code=skucode) 
            if wd_master and user  and  heirarchy_master and skumappingmaster  and row['WD_TOWN_ID'] and row['SKU_CODE'] and row['SKU_ID'] and row['CNF_ID'] and row['ACTIVE_FLAG'] and row['MAX(B.UNIT_PRICE)']:
                skumappingmaster_update=skumappingmaster.last()
                # skumappingmaster.wd_id = str(row['WD_ID'])
            
                skumappingmaster_update.status=0
                # skumappingmaster_update.wd_town_id=str(row['WD_TOWN_ID'])
                # skumappingmaster_update.sku_id=str(row['SKU_ID'])
                # skumappingmaster_update.cnf_id=str(row['CNF_ID'])
                # skumappingmaster_update.active_flag=str(row['ACTIVE_FLAG'])
                # skumappingmaster_update.last_price=str(row['MAX(B.UNIT_PRICE)'])
                skumappingmaster_update.save()
                row['Remarks'] = "Deactivate Successfully."
                
                # if data_check:
                #     row['Remarks'] = "Create Success."
                # elif not data_check:
                #     row['Remarks'] = "This sku id or sku code not exists in Sku Master, please provide with same sku id and code."
                    
                    
            elif not skumappingmaster:
                row['Remarks'] = "Not Exist."
            elif not heirarchy_master:
                row['Remarks'] = "Heirarchy Master not exist with this town id."
            elif not user:
                row['Remarks'] = "This user not exist user master."
            elif not wd_master:
                row['Remarks'] = " Wd master not exist."
            elif skumappingmaster:
                row['Remarks'] = "skumappingmaster already exist."
            elif (not row['WD_ID']) or (not row['WD_TOWN_ID']) or (not row['REGION_CODE']) or (not row['REGION']) or (not row['TOWN']) :
                row['Remasks'] = "Please try to fill all fields."

            with_remark.append(row)
          
        data['error_msg'] = with_remark
        return data      
                
                
class SkumasterproductUploadSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[FileExtensionValidator( ['CSV',] ) ])
    error_msg = serializers.ListField(read_only=True)
    class Meta:
        
        model=SKU_Master_Product
        
    def validate(self,data):
        file = data.get('file')
        csv_record = pd.read_csv(file,dtype=object)
        # Validation of csv format with column name==================start===>
        list_of_column_names = list(csv_record.columns)
        wrong_columns = 0
        
        column=['SKU_ID','SKU_CODE','SKU_SHORT_NAME','SKU_NAME','ACTIVE_FLAG','PRIMARY_UOM_CODE','EFFECTIVE_FROM','CATEGORY_CODE','CATEGORY_NAME','COMPANY']
        for columns in list_of_column_names: 

            print(columns,"=======")
            if columns not in column:
                wrong_columns+=1
        if len(column) != len(list_of_column_names) or wrong_columns > 0:
            raise serializers.ValidationError({'error' : ('CSV File format is wrong.Please check and correct.')})
        
        
        row_count = len(csv_record)
        file_list = csv_record.values.tolist()
        exist_user = []
        with_remark = []
        user_detail = None
        df_2_json = csv_record.to_json(orient='records')
        df_2_json = json.loads(df_2_json)
        
        if not df_2_json:
            raise serializers.ValidationError({'error' : ('There is no data in this CSV.')})
        
        for row in df_2_json:
            skuid=SKU_Master_Product.objects.filter(sku_id=str(row['SKU_ID']))
            skucode=SKU_Master_Product.objects.filter(sku_code=str(row['SKU_CODE']))
            try:
                date_check = datetime.datetime.strptime(str(row['EFFECTIVE_FROM']), '%Y-%m-%d')
                if date_check:
                    datecheck = date_check
                else:
                    datecheck = None
            except ValueError:
                datecheck = None
            
            
            if not ( skuid and skucode) and row['SKU_ID'] and row['SKU_CODE'] and row['SKU_SHORT_NAME'] and row['SKU_NAME'] and row['ACTIVE_FLAG'] and row['PRIMARY_UOM_CODE'] and datecheck and row['CATEGORY_CODE'] and row['CATEGORY_NAME'] and row['COMPANY']:
                skudata=SKU_Master_Product()
                skudata.sku_id=str(row['SKU_ID'])
                skudata.sku_code=str(row['SKU_CODE'])
                skudata.sku_short_name=str(row['SKU_SHORT_NAME'])
                skudata.sku_name=str(row['SKU_NAME'])
                skudata.active_flag=str(row['ACTIVE_FLAG'])
               
                skudata.primary_uom_code = str(row['PRIMARY_UOM_CODE'])
                skudata.effective_from = datecheck
                skudata.category_code = str(row['CATEGORY_CODE'])
                skudata.category_name = str(row['CATEGORY_NAME'])
                skudata.company = str(row['COMPANY'])
                skudata.save()
                
                row['Remarks'] = "Create Success."
            elif  skuid:
                row['Remarks'] = "Sku id already exists."
                
            elif  skucode:
                row['Remarks'] = "Sku code already exists."
            elif not datecheck:
                row['Remarks'] = "Invalid date format or date cannot be blank."
                   
            elif not row['SKU_ID'] or not row['SKU_CODE'] or not row['SKU_SHORT_NAME'] or not row['SKU_NAME'] or not row['ACTIVE_FLAG'] or not row['PRIMARY_UOM_CODE'] or not date_check or not row['CATEGORY_CODE'] or not row['CATEGORY_NAME'] or not row['COMPANY']:
                row['Remarks'] = "Please try to fill all fields"
    
                
            with_remark.append(row)
          
        data['error_msg'] = with_remark
        return data
                
                
                
                
class MasterWdSkuCategoryUpdate_town_id_CSVFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[FileExtensionValidator( ['CSV',] ) ])
    error_msg = serializers.ListField(read_only=True)
    class Meta:
        ref_name = 'heirarchy_master_WDskuCategory_upload'
            
    def validate(self,data):
        file = data.get('file')
        csv_record = pd.read_csv(file,dtype=object)
        # Validation of csv format with column name==================start===>
        list_of_column_names = list(csv_record.columns)
        wrong_columns = 0
        column=['sku_code','category','wd_id','town_id','correct_town_id','sku_id','cnf_id','active_flag']
        for columns in list_of_column_names: 

            print(columns,"=======")
            if columns not in column:
                wrong_columns+=1
        if len(column) != len(list_of_column_names) or wrong_columns > 0:
            raise serializers.ValidationError({'error' : ('CSV File format is wrong.Please check and correct.')})
        
        row_count = len(csv_record)
        file_list = csv_record.values.tolist()
        exist_user = []
        with_remark = []
        user_detail = None
        df_2_json = csv_record.to_json(orient='records')
        df_2_json = json.loads(df_2_json)
        
        if not df_2_json:
            raise serializers.ValidationError({'error' : ('There is no data in this CSV.')})
        
        for row in df_2_json: 
            
            skumappingmaster = WdSkuCatagory.objects.filter(sku_code=str(row['sku_code']),wd_town_id=str(row['town_id']),sku_id=str(row['sku_id']))

            skucode=str(row['sku_code'])
            skuid=str(row['sku_id'])
            data_check=SKU_Master_Product.objects.filter(sku_id=skuid,sku_code=skucode) 
            if skumappingmaster  and row['town_id'] and row['correct_town_id'] and row['sku_code'] and row['sku_id']:
                skumappingmaster_update=skumappingmaster.last()
            
                skumappingmaster_update.wd_town_id=str(row['correct_town_id'])
                skumappingmaster_update.last_updated_date = datetime.datetime.now()
                skumappingmaster_update.save()
                row['Remarks'] = "Update Successfully."
                                    
            elif not skumappingmaster:
                row['Remarks'] = "Not Exist."
           
            elif (not row['wd_id']) or (not row['town_id']) or (not row['correct_town_id']) or (not row['sku_id']) or (not row['sku_code']) :
                row['Remasks'] = "Please try to fill all fields."
            else:
                row['Remasks'] = "Something went wrong."

            with_remark.append(row)
          
        data['error_msg'] = with_remark
        return data      