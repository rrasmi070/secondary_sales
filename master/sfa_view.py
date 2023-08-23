import datetime
from master.models import SalesData, Temp_Total_sku_sales
from master.serializers import SalesDataSerializer


# def first_sale_create_update(self, li_arg):
#     try:
#         print("--------------------st")
#         print(li_arg,"+++++++1111111111111")
#         for fts in li_arg:
#             retive_cre_update = SalesData.objects.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
#             # retive_cre_update = sales_data.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
#             if not retive_cre_update:
#                 # SaleData_create(fts).sale_create()
                
                
                
#                 # commented for create sale thread=============
                
#                 sales_data_serializer = SalesDataSerializer(data = fts, many = False)
#                 if sales_data_serializer.is_valid():
#                     sales_data_serializer.save()
#                     print(sales_data_serializer.data,"=========ccrr")
#                 else:
#                     print(sales_data_serializer.errors)
#             else:
#                 # SaleData_update(retive_cre_update,fts).sale_update()
                
#                 # commented for update sale thread=============
#                 sales_data_serializer = SalesDataSerializer(retive_cre_update,data = fts, partial = True)
#                 if sales_data_serializer.is_valid():
#                     sales_data_serializer.save()
#                     print(sales_data_serializer.data,"=========upup")
                    
#                 else:
#                     print(sales_data_serializer.errors)
#         return "Success"
#     except Exception as e:
#         pass
    
    
def recent_day_sale():
            
    try:
        today_date = datetime.datetime.now().date()- datetime.timedelta(days=1)
        from_temp_sale = Temp_Total_sku_sales.objects.filter(sales_date_time = today_date).values('brand_category','sku_id','wd_id','town_id','sales_date_time',
                                                                'local_sales_retail','local_sales_dealer','local_sales_modern_trade','local_sales_hawker','total_local_sales',
                                                                'outstation_sales_reatil','outstation_sales_dealer','outstation_sales_modern_trade','outstation_sales_hawker','total_outstation_sales',
                                                                'other_sales_retail','other_sales_dealer','other_sales_modern_trade','total_other_sales',
                                                                'other_issues_damage','other_issues_return','other_issues_other','total_issue',
                                                                'grand_total','created_by','last_updated','transaction_source','created_date','last_updated_date',
                                                                'status','freeze_status','transaction_type','company','unit_price','region','cnf_id','value',
                                                                'wd_name','wd_type','sku_code','sku_short_name','town_name','town_code','distrcode',
                                                            )
        print(len(from_temp_sale))
        for fts in from_temp_sale:
            retive_cre_update = SalesData.objects.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
            # retive_cre_update = sales_data.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
            if not retive_cre_update:
                # SaleData_create(fts).sale_create()
                
                
                
                # commented for create sale thread=============
                
                sales_data_serializer = SalesDataSerializer(data = fts, many = False)
                if sales_data_serializer.is_valid():
                    sales_data_serializer.save()
                    print('sales_data_serializer.data',"=========11111")
                else:
                    print(sales_data_serializer.errors)
            else:
                # SaleData_update(retive_cre_update,fts).sale_update()
                
                # commenli_argted for update sale thread=============
                sales_data_serializer = SalesDataSerializer(retive_cre_update,data = fts, partial = True)
                if sales_data_serializer.is_valid():
                    sales_data_serializer.save()
                    print('sales_data_serializer.data',"=========11111")
                    
                else:
                    print(sales_data_serializer.errors)
        return "Success"
        
    except Exception as e:
        pass
    
def roolover_day_sale():
            
    try:
        today_date = datetime.datetime.now().date()- datetime.timedelta(days=1)
        from_temp_sale = Temp_Total_sku_sales.objects.filter(sales_date_time__lt = today_date).values('brand_category','sku_id','wd_id','town_id','sales_date_time',
                                                                'local_sales_retail','local_sales_dealer','local_sales_modern_trade','local_sales_hawker','total_local_sales',
                                                                'outstation_sales_reatil','outstation_sales_dealer','outstation_sales_modern_trade','outstation_sales_hawker','total_outstation_sales',
                                                                'other_sales_retail','other_sales_dealer','other_sales_modern_trade','total_other_sales',
                                                                'other_issues_damage','other_issues_return','other_issues_other','total_issue',
                                                                'grand_total','created_by','last_updated','transaction_source','created_date','last_updated_date',
                                                                'status','freeze_status','transaction_type','company','unit_price','region','cnf_id','value',
                                                                'wd_name','wd_type','sku_code','sku_short_name','town_name','town_code','distrcode',
                                                            )
        print(len(from_temp_sale))
        for fts in from_temp_sale:
            retive_cre_update = SalesData.objects.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
            # retive_cre_update = sales_data.filter(wd_id = fts['wd_id'],sku_id = fts['sku_id'],sales_date_time=fts['sales_date_time'],transaction_type = 'DAILY',town_id = fts['town_id'],town_code = fts['town_code']).last()
            if not retive_cre_update:
                # SaleData_create(fts).sale_create()
                
                
                
                # commented for create sale thread=============
                
                sales_data_serializer = SalesDataSerializer(data = fts, many = False)
                if sales_data_serializer.is_valid():
                    sales_data_serializer.save()
                    print('sales_data_serializer.data',"=========22222222222")
                else:
                    print(sales_data_serializer.errors)
            else:
                # SaleData_update(retive_cre_update,fts).sale_update()
                
                # commenli_argted for update sale thread=============
                sales_data_serializer = SalesDataSerializer(retive_cre_update,data = fts, partial = True)
                if sales_data_serializer.is_valid():
                    sales_data_serializer.save()
                    print('sales_data_serializer.data',"=========2222222222222")
                    
                else:
                    print(sales_data_serializer.errors)
        return "Success"
        
    except Exception as e:
        pass