import threading
from master.models import SalesData

from master.serializers import SalesDataSerializer


class SaleData_create(threading.Thread):
    def __init__(self, json):
        self.json = json
        threading.Thread.__init__(self)
        
    def sale_create(self):
        try:
            sales_data_serializer = SalesDataSerializer(data = self.json, many = False)
            if sales_data_serializer.is_valid():
                sales_data_serializer.save()
                print(sales_data_serializer.data,"=========ccrr")
            else:
                print(sales_data_serializer.errors)
        except Exception as e:
            pass
        
        
        
class SaleData_update(threading.Thread):
    def __init__(self,update_obj, json):
        self.json = json
        self.update_obj = update_obj
        threading.Thread.__init__(self)
        
    def sale_update(self):
        try:
            sales_data_serializer = SalesDataSerializer(self.update_obj,data = self.json, partial = True)
            if sales_data_serializer.is_valid():
                sales_data_serializer.save()
                print(sales_data_serializer.data,"=========upup")
                
            else:
                print(sales_data_serializer.errors)
        except Exception as e:
            pass
        
        
def first_sale_create_update(self, li_arg):
    try:
        print(self.li_arg,"+++++++1111111111111")
        for fts in li_arg:
            retive_cre_update = SalesData.objects.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
            # retive_cre_update = sales_data.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
            if not retive_cre_update:
                # SaleData_create(fts).sale_create()
                
                
                
                # commented for create sale thread=============
                
                sales_data_serializer = SalesDataSerializer(data = fts, many = False)
                if sales_data_serializer.is_valid():
                    sales_data_serializer.save()
                    print(sales_data_serializer.data,"=========ccrr")
                else:
                    print(sales_data_serializer.errors)
            else:
                # SaleData_update(retive_cre_update,fts).sale_update()
                
                # commented for update sale thread=============
                sales_data_serializer = SalesDataSerializer(retive_cre_update,data = fts, partial = True)
                if sales_data_serializer.is_valid():
                    sales_data_serializer.save()
                    print(sales_data_serializer.data,"=========upup")
                    
                else:
                    print(sales_data_serializer.errors)
    except Exception as e:
        pass
    
    
class SaleData_create_and_update_1(threading.Thread):
    def __init__(self,from_temp_sale):
        # print(from_temp_sale,"======init--------")
        # self.json = json
        self.from_temp_sale = from_temp_sale
        threading.Thread.__init__(self)
        
        
    def run(self):
        print(len(self.from_temp_sale),"==========start thread")
        for fts in self.from_temp_sale:        
            print('------------------11111')               
            retive_cre_update = SalesData.objects.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
            # retive_cre_update = sales_data.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
            if not retive_cre_update:
                # SaleData_create(fts).sale_create()
                
                
                
                # commented for create sale thread=============
                
                sales_data_serializer = SalesDataSerializer(data = fts, many = False)
                if sales_data_serializer.is_valid():
                    sales_data_serializer.save()
                    # print(sales_data_serializer.data,"=========ccrr")
                else:
                    print(sales_data_serializer.errors)
            else:
                # SaleData_update(retive_cre_update,fts).sale_update()
                
                # commented for update sale thread=============
                sales_data_serializer = SalesDataSerializer(retive_cre_update,data = fts, partial = True)
                if sales_data_serializer.is_valid():
                    sales_data_serializer.save()
                    # print(sales_data_serializer.data,"=========upup")
                    
                else:
                    print(sales_data_serializer.errors)
                    
                    
class SaleData_create_and_update_2(threading.Thread):
    def __init__(self,from_temp_sale):
        # print(from_temp_sale,"======init--------")
        # self.json = json
        self.from_temp_sale = from_temp_sale
        threading.Thread.__init__(self)
        
    def run(self):
        print(len(self.from_temp_sale),"==========start thread")
        
        for fts in self.from_temp_sale:         
            print('------------------22222')               
                          
            retive_cre_update = SalesData.objects.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
            # retive_cre_update = sales_data.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
            if not retive_cre_update:
                # SaleData_create(fts).sale_create()
                
                
                
                # commented for create sale thread=============
                
                sales_data_serializer = SalesDataSerializer(data = fts, many = False)
                if sales_data_serializer.is_valid():
                    sales_data_serializer.save()
                    # print(sales_data_serializer.data,"=========ccrr")
                else:
                    print(sales_data_serializer.errors)
            else:
                # SaleData_update(retive_cre_update,fts).sale_update()
                
                # commented for update sale thread=============
                sales_data_serializer = SalesDataSerializer(retive_cre_update,data = fts, partial = True)
                if sales_data_serializer.is_valid():
                    sales_data_serializer.save()
                    # print(sales_data_serializer.data,"=========upup")
                    
                else:
                    print(sales_data_serializer.errors)
                    
                    
                    
class SaleData_create_and_update_3(threading.Thread):
    def __init__(self,from_temp_sale):
        # print(from_temp_sale,"======init--------")
        # self.json = json
        self.from_temp_sale = from_temp_sale
        threading.Thread.__init__(self)
    def run(self):
        print(len(self.from_temp_sale),"==========start thread")
        
        for fts in self.from_temp_sale:                 
            print('------------------3333')               
                  
            retive_cre_update = SalesData.objects.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
            # retive_cre_update = sales_data.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
            if not retive_cre_update:
                # SaleData_create(fts).sale_create()
                
                
                
                # commented for create sale thread=============
                
                sales_data_serializer = SalesDataSerializer(data = fts, many = False)
                if sales_data_serializer.is_valid():
                    sales_data_serializer.save()
                    # print(sales_data_serializer.data,"=========ccrr")
                else:
                    print(sales_data_serializer.errors)
            else:
                # SaleData_update(retive_cre_update,fts).sale_update()
                
                # commented for update sale thread=============
                sales_data_serializer = SalesDataSerializer(retive_cre_update,data = fts, partial = True)
                if sales_data_serializer.is_valid():
                    sales_data_serializer.save()
                    # print(sales_data_serializer.data,"=========upup")
                    
                else:
                    print(sales_data_serializer.errors)
                    
                    
class SaleData_create_and_update_4(threading.Thread):
    def __init__(self,from_temp_sale):
        # print(from_temp_sale,"======init--------")
        # self.json = json
        self.from_temp_sale = from_temp_sale
        threading.Thread.__init__(self)
        
    def run(self):
        print(len(self.from_temp_sale),"==========start thread")
        
        for fts in self.from_temp_sale:                       
            print('------------------44444')               
            
            retive_cre_update = SalesData.objects.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
            # retive_cre_update = sales_data.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
            if not retive_cre_update:
                # SaleData_create(fts).sale_create()
                
                
                
                # commented for create sale thread=============
                
                sales_data_serializer = SalesDataSerializer(data = fts, many = False)
                if sales_data_serializer.is_valid():
                    sales_data_serializer.save()
                    # print(sales_data_serializer.data,"=========ccrr")
                else:
                    print(sales_data_serializer.errors)
            else:
                # SaleData_update(retive_cre_update,fts).sale_update()
                
                # commented for update sale thread=============
                sales_data_serializer = SalesDataSerializer(retive_cre_update,data = fts, partial = True)
                if sales_data_serializer.is_valid():
                    sales_data_serializer.save()
                    # print(sales_data_serializer.data,"=========upup")
                    
                else:
                    print(sales_data_serializer.errors)