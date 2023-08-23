from pyexpat import model
from statistics import mode
from timeit import repeat
from django.db import models
import datetime

from base.models import User


class Sales_Hierarchy_Master(models.Model):
    wd_id = models.CharField(max_length=100,null=True,blank=True)
    wd_town_id = models.CharField(max_length=100,null=True,blank=True)
    region_code = models.CharField(max_length=100,null=True,blank=True)
    region = models.CharField(max_length=100,null=True,blank=True)
    town_code = models.CharField(max_length=100,null=True,blank=True)
    town = models.CharField(max_length=100,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    created_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    last_updated = models.CharField(max_length=101, null=True, blank=True)
    status = models.BooleanField(default=True)
    sku_category_code = models.CharField(max_length=100,null=True,blank=True)
    wd_town_code = models.CharField(max_length=100,null=True,blank=True)


    

class SKU_Master_Product(models.Model):
    sku_id = models.CharField(max_length=100,null=True,blank=True)
    sku_code = models.CharField(max_length=100,null=True,blank=True)
    sku_short_name = models.CharField(max_length=100,null=True,blank=True)
    sku_name = models.CharField(max_length=100,null=True,blank=True)
    active_flag = models.CharField(max_length=100,null=True,blank=True)
    cnf_id = models.IntegerField(null=True,blank=True)
    cnf_name = models.CharField(max_length=100,null=True,blank=True)
    weight_uom_code = models.CharField(max_length=100,null=True,blank=True)
    calculated_by = models.FloatField(max_length=100,null=True,blank=True)
    effective_from = models.CharField(max_length=100,null=True,blank=True)
    category_name = models.CharField(max_length=100,null=True,blank=True)
    category_code = models.CharField(max_length=100,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    created_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    last_updated = models.CharField(max_length=101,null=True, blank=True)
    status = models.BooleanField(default=True)
    primary_uom_code = models.CharField(max_length=100,null=True,blank=True)
    company = models.CharField(max_length=60,null=True,blank=True)
    unit_price = models.FloatField(blank=True,null=True,default=0)


class WdSkuCatagory(models.Model):
    # category_code = models.CharField(max_length=100,null=True,blank=True)
    sku_code = models.CharField(max_length=100, blank=True,null=True)
    wd_town_id = models.CharField(max_length=100,blank=True,null=True)
    sku_id = models.CharField(max_length=100,null=True,blank=True)
    cnf_id = models.CharField(max_length=100, blank=True,null=True)
    cnf_code = models.CharField(max_length=50,blank=True,null=True)
    order_month_year = models.CharField(max_length=50,blank=True,null=True)
    last_price = models.FloatField(default=0)
    active_flag = models.CharField(max_length=100, blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    created_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    last_updated = models.CharField(max_length=101,null=True, blank=True)
    status = models.BooleanField(default=True)







class SalesData(models.Model):
    brand_category = models.CharField(max_length=20 , blank=True,null=True)
    sku_id = models.CharField(max_length=100, blank=True,null=True)
    wd_id = models.CharField(max_length=100, blank=True,null=True)
    town_id	= models.CharField(max_length=100, blank=True,null=True)
    sales_date_time = models.DateField(blank=True,null=True)


    local_sales_retail = models.FloatField(blank=True,null=True,default=0)
    local_sales_dealer = models.FloatField(blank=True,null=True,default=0)
    local_sales_modern_trade = models.FloatField(blank=True,null=True,default=0)
    local_sales_hawker = models.FloatField(blank=True,null=True,default=0)
    total_local_sales = models.FloatField(blank=True,null=True,default=0)

    outstation_sales_reatil	= models.FloatField(blank=True,null=True,default=0)
    outstation_sales_dealer = models.FloatField(blank=True,null=True,default=0)
    outstation_sales_modern_trade = models.FloatField(blank=True,null=True,default=0)
    outstation_sales_hawker = models.FloatField(blank=True,null=True,default=0)
    total_outstation_sales = models.FloatField(blank=True,null=True,default=0)
    
    other_sales_retail = models.FloatField(blank=True,null=True,default=0)
    other_sales_dealer = models.FloatField(blank=True,null=True,default=0)
    other_sales_modern_trade = models.FloatField(blank=True,null=True,default=0)
    total_other_sales = models.FloatField(blank=True,null=True,default=0)

    
    other_issues_damage = models.FloatField(blank=True,null=True,default=0)
    other_issues_return = models.FloatField(blank=True,null=True,default=0)
    other_issues_other = models.FloatField(blank=True,null=True,default=0)
    total_issue = models.FloatField(blank=True,null=True,default=0)

    grand_total = models.DecimalField(blank=True,null=True,default=0,max_digits=10, decimal_places = 3)
    
    created_by = models.CharField(max_length=100, blank=True,null=True)
    last_updated = models.CharField(max_length=100, blank=True,null=True)
    transaction_source = models.CharField(max_length=50, blank=True,null=True)
    created_date = models.DateTimeField(blank=True,null=True)
    last_updated_date = models.DateTimeField(blank=True,null=True)
    status = models.BooleanField(default=True)
    freeze_status = models.BooleanField(default=False)
    transaction_type = models.CharField(max_length=20, blank=True,null=True)

    company = models.CharField(max_length=60,null=True,blank=True)
    unit_price = models.FloatField(blank=True,null=True,default=0)
    region = models.CharField(max_length=60,null=True,blank=True)
    cnf_id = models.CharField(max_length=60,null=True,blank=True)
    value = models.FloatField(null=True,blank=True,default=0)

    #now field for report
    wd_name = models.CharField(max_length=60,null=True,blank=True)
    wd_type = models.CharField(max_length=60,null=True,blank=True)
    sku_code = models.CharField(max_length=60,null=True,blank=True)
    sku_short_name = models.CharField(max_length=60,null=True,blank=True)
    town_name = models.CharField(null=True,blank=True,max_length=60)
    town_code = models.CharField(null=True,blank=True,max_length=150)
    distrcode = models.CharField(null=True,blank=True,max_length=50)
    zone =  models.CharField(null=True,blank=True,max_length=150)
    statename =  models.CharField(null=True,blank=True,max_length=150)
    gpi_state =  models.CharField(null=True,blank=True,max_length=150)


    # status_3rd_party = models.BooleanField(default=False)
    class Meta:
        db_table = "transaction_salesdata"
             
class SalesData_7days(models.Model):
    brand_category = models.CharField(max_length=20 , blank=True,null=True)
    sku_id = models.CharField(max_length=100, blank=True,null=True)
    wd_id = models.CharField(max_length=100, blank=True,null=True)
    town_id	= models.CharField(max_length=100, blank=True,null=True)
    sales_date_time = models.DateField(blank=True,null=True)


    local_sales_retail = models.FloatField(blank=True,null=True,default=0)
    local_sales_dealer = models.FloatField(blank=True,null=True,default=0)
    local_sales_modern_trade = models.FloatField(blank=True,null=True,default=0)
    local_sales_hawker = models.FloatField(blank=True,null=True,default=0)
    total_local_sales = models.FloatField(blank=True,null=True,default=0)

    outstation_sales_reatil	= models.FloatField(blank=True,null=True,default=0)
    outstation_sales_dealer = models.FloatField(blank=True,null=True,default=0)
    outstation_sales_modern_trade = models.FloatField(blank=True,null=True,default=0)
    outstation_sales_hawker = models.FloatField(blank=True,null=True,default=0)
    total_outstation_sales = models.FloatField(blank=True,null=True,default=0)
    
    other_sales_retail = models.FloatField(blank=True,null=True,default=0)
    other_sales_dealer = models.FloatField(blank=True,null=True,default=0)
    other_sales_modern_trade = models.FloatField(blank=True,null=True,default=0)
    total_other_sales = models.FloatField(blank=True,null=True,default=0)

    
    other_issues_damage = models.FloatField(blank=True,null=True,default=0)
    other_issues_return = models.FloatField(blank=True,null=True,default=0)
    other_issues_other = models.FloatField(blank=True,null=True,default=0)
    total_issue = models.FloatField(blank=True,null=True,default=0)

    grand_total = models.DecimalField(blank=True,null=True,default=0,max_digits=10, decimal_places = 3)
    
    created_by = models.CharField(max_length=100, blank=True,null=True)
    last_updated = models.CharField(max_length=100, blank=True,null=True)
    transaction_source = models.CharField(max_length=50, blank=True,null=True)
    created_date = models.DateTimeField(blank=True,null=True)
    last_updated_date = models.DateTimeField(blank=True,null=True)
    status = models.BooleanField(default=True)
    freeze_status = models.BooleanField(default=False)
    transaction_type = models.CharField(max_length=20, blank=True,null=True)

    company = models.CharField(max_length=60,null=True,blank=True)
    unit_price = models.FloatField(blank=True,null=True,default=0)
    region = models.CharField(max_length=60,null=True,blank=True)
    cnf_id = models.CharField(max_length=60,null=True,blank=True)
    value = models.FloatField(null=True,blank=True,default=0)

    #now field for report
    wd_name = models.CharField(max_length=60,null=True,blank=True)
    wd_type = models.CharField(max_length=60,null=True,blank=True)
    sku_code = models.CharField(max_length=60,null=True,blank=True)
    sku_short_name = models.CharField(max_length=60,null=True,blank=True)
    town_name = models.CharField(null=True,blank=True,max_length=60)
    town_code = models.CharField(null=True,blank=True,max_length=150)
    distrcode = models.CharField(null=True,blank=True,max_length=50)
    zone =  models.CharField(null=True,blank=True,max_length=150)
    statename =  models.CharField(null=True,blank=True,max_length=150)
    gpi_state =  models.CharField(null=True,blank=True,max_length=150)


    # status_3rd_party = models.BooleanField(default=False)
    class Meta:
        db_table = "transaction_salesdata_last7days"


class Total_sku_sales(models.Model):
    sale_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=25,null=True,blank=True)
    town_id =  models.CharField(max_length=25,null=True,blank=True)
    wd_id =  models.CharField(max_length=25,null=True,blank=True)
    transaction_type =  models.CharField(max_length=25,null=True,blank=True) #which type of transaction (daily/weekly)======

    local_retail_total = models.FloatField(default=0, null=True,blank=True)
    local_dealer_total = models.FloatField(default=0, null=True,blank=True)
    local_hawker_total = models.FloatField(default=0, null=True,blank=True)
    local_m_total = models.FloatField(default=0, null=True,blank=True)
    total_local = models.FloatField(default=0, null=True,blank=True)

    outstation_retail_total = models.FloatField(default=0, null=True,blank=True)
    outstation_dealer_total = models.FloatField(default=0, null=True,blank=True)
    outstation_hawker_total = models.FloatField(default=0, null=True,blank=True)
    outstation_m_total = models.FloatField(default=0, null=True,blank=True)
    outstation_total = models.FloatField(default=0, null=True,blank=True)

    other_retail_total = models.FloatField(default=0, null=True,blank=True)
    other_dealer_total = models.FloatField(default=0, null=True,blank=True)
    other_m_total = models.FloatField(default=0, null=True,blank=True)
    other_total = models.FloatField(default=0, null=True,blank=True)

    total_retail_total = models.FloatField(default=0, null=True,blank=True)
    total_detail_total = models.FloatField(default=0, null=True,blank=True)
    total_hawker_total = models.FloatField(default=0, null=True,blank=True)
    total_m_trade_total = models.FloatField(default=0, null=True,blank=True)
    all_total = models.FloatField(default=0, null=True,blank=True) #till this========================

    other_issued_damage_total = models.FloatField(default=0, null=True,blank=True)
    other_issued_return_total = models.FloatField(default=0, null=True,blank=True)
    other_issued_other_total = models.FloatField(default=0, null=True,blank=True)
    total_issued = models.FloatField(default=0, null=True,blank=True)

    created_date = models.DateTimeField(null=True,blank=True)
    updated_date = models.DateTimeField(null=True,blank=True)

    class Meta:
        db_table = "transaction_total_sku_sales"
        
class Temp_Total_sku_sales(models.Model):
    brand_category = models.CharField(max_length=20 , blank=True,null=True)
    sku_id = models.CharField(max_length=100, blank=True,null=True)
    wd_id = models.CharField(max_length=100, blank=True,null=True)
    town_id	= models.CharField(max_length=100, blank=True,null=True)
    sales_date_time = models.DateField(blank=True,null=True)


    local_sales_retail = models.FloatField(blank=True,null=True,default=0)
    local_sales_dealer = models.FloatField(blank=True,null=True,default=0)
    local_sales_modern_trade = models.FloatField(blank=True,null=True,default=0)
    local_sales_hawker = models.FloatField(blank=True,null=True,default=0)
    total_local_sales = models.FloatField(blank=True,null=True,default=0)

    outstation_sales_reatil	= models.FloatField(blank=True,null=True,default=0)
    outstation_sales_dealer = models.FloatField(blank=True,null=True,default=0)
    outstation_sales_modern_trade = models.FloatField(blank=True,null=True,default=0)
    outstation_sales_hawker = models.FloatField(blank=True,null=True,default=0)
    total_outstation_sales = models.FloatField(blank=True,null=True,default=0)
    
    other_sales_retail = models.FloatField(blank=True,null=True,default=0)
    other_sales_dealer = models.FloatField(blank=True,null=True,default=0)
    other_sales_modern_trade = models.FloatField(blank=True,null=True,default=0)
    total_other_sales = models.FloatField(blank=True,null=True,default=0)

    
    other_issues_damage = models.FloatField(blank=True,null=True,default=0)
    other_issues_return = models.FloatField(blank=True,null=True,default=0)
    other_issues_other = models.FloatField(blank=True,null=True,default=0)
    total_issue = models.FloatField(blank=True,null=True,default=0)

    grand_total = models.FloatField(blank=True,null=True,default=0)
    
    created_by = models.CharField(max_length=100, blank=True,null=True)
    last_updated = models.CharField(max_length=100, blank=True,null=True)
    transaction_source = models.CharField(max_length=50, blank=True,null=True)
    created_date = models.DateTimeField(blank=True,null=True)
    last_updated_date = models.DateTimeField(blank=True,null=True)
    status = models.BooleanField(default=True)
    freeze_status = models.BooleanField(default=False)
    transaction_type = models.CharField(max_length=20, blank=True,null=True)

    company = models.CharField(max_length=60,null=True,blank=True)
    unit_price = models.FloatField(blank=True,null=True,default=0)
    region = models.CharField(max_length=60,null=True,blank=True)
    cnf_id = models.CharField(max_length=60,null=True,blank=True)
    value = models.FloatField(null=True,blank=True,default=0)

    #now field for report
    wd_name = models.CharField(max_length=60,null=True,blank=True)
    wd_type = models.CharField(max_length=60,null=True,blank=True)
    sku_code = models.CharField(max_length=60,null=True,blank=True)
    sku_short_name = models.CharField(max_length=60,null=True,blank=True)
    town_name = models.CharField(null=True,blank=True,max_length=60)
    town_code = models.CharField(null=True,blank=True,max_length=150)
    distrcode = models.CharField(null=True,blank=True,max_length=50)
    zone =  models.CharField(null=True,blank=True,max_length=150)
    statename =  models.CharField(null=True,blank=True,max_length=150)
    gpi_state =  models.CharField(null=True,blank=True,max_length=150)

    # demon = models.CharField(null=True,blank=True,max_length=50)

    class Meta:
        db_table = "temp_transaction_total_sku_sales"


class Archived_SalesData(models.Model):
    brand_category = models.CharField(max_length=20 , blank=True,null=True)
    sku_id = models.CharField(max_length=100, blank=True,null=True)
    wd_id = models.CharField(max_length=100, blank=True,null=True)
    town_id	= models.CharField(max_length=100, blank=True,null=True)
    sales_date_time = models.DateField(blank=True,null=True)


    local_sales_retail = models.FloatField(blank=True,null=True,default=0)
    local_sales_dealer = models.FloatField(blank=True,null=True,default=0)
    local_sales_modern_trade = models.FloatField(blank=True,null=True,default=0)
    local_sales_hawker = models.FloatField(blank=True,null=True,default=0)
    total_local_sales = models.FloatField(blank=True,null=True,default=0)

    outstation_sales_reatil	= models.FloatField(blank=True,null=True,default=0)
    outstation_sales_dealer = models.FloatField(blank=True,null=True,default=0)
    outstation_sales_modern_trade = models.FloatField(blank=True,null=True,default=0)
    outstation_sales_hawker = models.FloatField(blank=True,null=True,default=0)
    total_outstation_sales = models.FloatField(blank=True,null=True,default=0)
    
    other_sales_retail = models.FloatField(blank=True,null=True,default=0)
    other_sales_dealer = models.FloatField(blank=True,null=True,default=0)
    other_sales_modern_trade = models.FloatField(blank=True,null=True,default=0)
    total_other_sales = models.FloatField(blank=True,null=True,default=0)

    
    other_issues_damage = models.FloatField(blank=True,null=True,default=0)
    other_issues_return = models.FloatField(blank=True,null=True,default=0)
    other_issues_other = models.FloatField(blank=True,null=True,default=0)
    total_issue = models.FloatField(blank=True,null=True,default=0)

    grand_total = models.FloatField(blank=True,null=True,default=0)
    
    created_by = models.CharField(max_length=100, blank=True,null=True)
    last_updated = models.CharField(max_length=100, blank=True,null=True)
    transaction_source = models.CharField(max_length=50, blank=True,null=True)
    created_date = models.DateTimeField(blank=True,null=True)
    last_updated_date = models.DateTimeField(blank=True,null=True)

    archived_date = models.DateTimeField(blank=True,null=True)

    status = models.BooleanField(default=True)
    freeze_status = models.BooleanField(default=False)
    transaction_type = models.CharField(max_length=20, blank=True,null=True)

    company = models.CharField(max_length=60,null=True,blank=True)
    unit_price = models.FloatField(blank=True,null=True,default=0)
    region = models.CharField(max_length=60,null=True,blank=True)
    cnf_id = models.CharField(max_length=60,null=True,blank=True)
    value = models.FloatField(null=True,blank=True,default=0)

    #now field for report
    wd_name = models.CharField(max_length=60,null=True,blank=True)
    wd_type = models.CharField(max_length=60,null=True,blank=True)
    sku_code = models.CharField(max_length=60,null=True,blank=True)
    sku_short_name = models.CharField(max_length=60,null=True,blank=True)
    town_name = models.CharField(null=True,blank=True,max_length=60)
    town_code = models.CharField(null=True,blank=True,max_length=100)
    zone =  models.CharField(null=True,blank=True,max_length=150)
    statename =  models.CharField(null=True,blank=True,max_length=150)
    gpi_state =  models.CharField(null=True,blank=True,max_length=150)

    # status_3rd_party = models.BooleanField(default=False)
    class Meta:
        db_table = "transaction_archived_salesdata"


class Sku_remarks(models.Model):
    wd_id = models.CharField(max_length=100, blank=True,null=True)
    sales_date_time = models.DateField(blank=True,null=True)
    remarks_type = models.CharField(max_length=20, blank=True,null=True)

    created_by = models.CharField(max_length=100, blank=True,null=True)
    last_updated = models.CharField(max_length=100, blank=True,null=True)
    created_date = models.DateTimeField(blank=True,null=True)
    last_updated_date = models.DateTimeField(blank=True,null=True)
    remarks = models.TextField(blank=True,null=True)


class SKU_type(models.Model):
    wd_id = models.CharField(max_length=100,null=True,blank=True)
    wd_type = models.CharField(max_length=100,null=True,blank=True)
    created_by = models.CharField(max_length=100, blank=True,null=True)
    last_updated = models.CharField(max_length=100, blank=True,null=True)
    created_date = models.DateTimeField(blank=True,null=True)
    last_updated_date = models.DateTimeField(blank=True,null=True)

class Integration_log_summary(models.Model):
    tranisition_source = models.CharField(max_length=50, blank=True,null=True)
    sale_date = models.DateField(blank=True,null=True)
    total_distributer_sale = models.IntegerField(blank=True,null=True)
    total_insart_sale = models.IntegerField(blank=True,null=True)
    invalid = models.IntegerField(default=0)
    email_status = models.BooleanField(default=False)

    created_by = models.CharField(max_length=100, blank=True,null=True)
    last_updated = models.CharField(max_length=100, blank=True,null=True)
    created_date = models.DateTimeField(auto_now=True)
    last_updated_date = models.DateTimeField(blank=True,null=True)
    class Meta:
        db_table = "integration_log_summary"
        


class Integration_log_details(models.Model):
    sku_id = models.CharField(max_length=100, blank=True,null=True)
    wd_id = models.CharField(max_length=100, blank=True,null=True)
    town_id = models.CharField(max_length=100, blank=True,null=True)
    reason = models.TextField(blank=True,null=True)
    tranisition_source = models.CharField(max_length=50, blank=True,null=True)
    sales_date_time = models.DateTimeField(blank=True,null=True)
    repeat_count = models.IntegerField(blank=True,null=True)

    created_by = models.CharField(max_length=100, blank=True,null=True)
    last_updated = models.CharField(max_length=100, blank=True,null=True)
    created_date = models.DateTimeField(blank=True,null=True)
    last_updated_date = models.DateTimeField(blank=True,null=True)
    class Meta:
        db_table = "integration_log_details"



class Candy_JAR_GMS(models.Model):
    sku_id = models.CharField(max_length = 50 ,null=True, blank=True)
    sku_code = models.CharField(max_length = 50 ,null=True, blank=True)
    sku_name = models.CharField(max_length = 50 ,null=True, blank=True)
    sku_short_name = models.CharField(max_length = 50 ,null=True, blank=True)
    jar_size_gms = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = "candy_conversion_jar_gms"


# third_party API Repeat count table======
class Repeat_count(models.Model):
    wd_id = models.CharField(max_length=50,blank=True,null = True)
    sku_id = models.CharField(max_length=50,blank=True,null = True)
    town_id = models.CharField(max_length=150,blank=True,null = True)
    sale_date_time = models.DateField(max_length=50,blank=True,null = True)
    transaction_source = models.CharField(max_length=50,blank=True,null = True)
    repeat_time = models.IntegerField(default=0,blank=True,null = True)
    
    

class Invalid_log_data(models.Model):
    distrcode = models.CharField(max_length=30,blank=True,null = True)
    dist_id = models.CharField(max_length=30,blank=True,null = True)
    dist_type = models.CharField(max_length=30,blank=True,null = True)
    sale_date = models.CharField(max_length=30,blank=True,null = True)
    region = models.CharField(max_length=30,blank=True,null = True)
    town_code = models.CharField(max_length=30,blank=True,null = True)
    prodcode = models.CharField(max_length=30,blank=True,null = True)
    state = models.CharField(max_length=30,blank=True,null = True)
    duration_start = models.CharField(max_length=30,blank=True,null = True)
    plan_type = models.CharField(max_length=30,blank=True,null = True)
    franchisecode = models.CharField(max_length=30,blank=True,null = True)
    brandcode = models.CharField(max_length=30,blank=True,null = True)
    catcode = models.CharField(max_length=30,blank=True,null = True)
    local_retail = models.CharField(max_length=30,blank=True,null = True)
    local_dealer = models.CharField(max_length=30,blank=True,null = True)
    local_MT = models.CharField(max_length=30,blank=True,null = True)
    local_HA = models.CharField(max_length=30,blank=True,null = True)
    out_retail = models.CharField(max_length=30,blank=True,null = True)
    out_dealer = models.CharField(max_length=30,blank=True,null = True)
    out_MT = models.CharField(max_length=30,blank=True,null = True)
    out_HA = models.CharField(max_length=30,blank=True,null = True)
    other_retail = models.CharField(max_length=30,blank=True,null = True)
    other_dealer = models.CharField(max_length=30,blank=True,null = True)
    other_MT = models.CharField(max_length=30,blank=True,null = True)
    other_issued_damage = models.CharField(max_length=30,blank=True,null = True)
    other_issued_returns = models.CharField(max_length=30,blank=True,null = True)
    transaction_source = models.CharField(max_length=30,blank=True,null = True)
    
    # 3rd party api running status
   
        
    
class Apistatus(models.Model):
    
    running_date = models.DateField(blank=True,null = True)
    status = models.BooleanField(default=False)
    api = models.CharField(max_length=30,blank=True,null = True)
    sfa_bulk_flag = models.BooleanField(default=False)
    
             
class Subject(models.Model):
    use_for=models.CharField(max_length=20,blank=True,null=True)
    name=models.CharField(max_length=250,blank=True,null=True)
    
class Email_users(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,blank=True,null=True)
    email=models.EmailField(max_length=100,blank=True,null=True)
    use_for=models.CharField(max_length=100,blank=True,null=True)
    email_cc=models.BooleanField(default=True)
    email_to=models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)