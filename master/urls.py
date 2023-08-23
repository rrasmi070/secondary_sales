from django.db import router
from django.urls import include, path
from master.views import *
from master.master_view import *

urlpatterns = [
    # url(r'^hhh', schema_view),
    path('api/v1/master_user_upload/',MasteruserCSVFileUploadGenerics.as_view(),name='master_user_upload'),
    path('api/v1/wd_master_upload/',WDMasterCSVFileUploadGenerics.as_view(),name='wd_master_upload'),
    path('api/v1/heirarchy_master_upload/',HeirarchymasterMasterCSVFileUploadFieldagentGenerics.as_view(),name='heirarchy_master_upload'),
    path('api/v1/masterwdskucategoryupload/',MasterWdSkuCategory.as_view(),name='masterwdskucategoryupload'),
    path('api/v1/masterwdskucategoryupload_update/',MasterWdSkuCategoryUpdate.as_view(),name='masterwdskucategoryupload_update'),
    path('api/v1/skumasterproduct/',Skumasterproduct.as_view(),name='skumasterproduct'),
    path('api/v1/masterwdskucategoryupload_update_town_id/',MasterWdSkuCategoryUpdate_Town_id.as_view(),name='masterwdskucategoryupload_update_town_id'),
    
    
    path('api/v1/User_upload/',User_upload.as_view(),name='User_upload'),
    path('api/v1/BranchMaster_upload/',BranchMaster_upload.as_view(),name='BranchMaster_upload'),
    path('api/v1/SKU_Master_Productupload/',SKU_Master_Productupload.as_view(),name='SKU_Master_Productupload'),
    path('api/v1/WDmaster_upload/',WDmaster_upload.as_view(),name='WDmaster_upload'),
    path('api/v1/WdSkuCatagoryupload/',WdSkuCatagoryupload.as_view(),name='WdSkuCatagoryupload'),
    path('api/v1/Sales_Hierarchy/',Sales_Hierarchy_Master_upload.as_view(),name='Sales_Hierarchy'),
    path('api/v1/master_candy_gms_upload/',Candy_Gms.as_view(),name='Candy_Gms'),
    

    path('api/v1/WD_sku_type_upload/',WD_sku_type_upload.as_view(),name='WD_sku_type_upload'),

    path('api/v1/SFA_API_validate/',SFA_API_valid.as_view(),name='SFA_API_valid'), #by Rasmi======
    path('api/v1/SFA_API_read_json_file/',SFA_API_read_json_file.as_view(),name='SFA_API_read_json_file'), #by Rasmi======
    path('api/v2/SFA_API_validate_v2/',SFA_API_valid_V2.as_view(),name='SFA_API_validate_v2'), #by Rasmi======

    path('api/v1/surya_api/',Schedule_Surya.as_view(),name='Surya_API'),
    
    # path('api/v1/surya_api_json_read/',Surya_API_json.as_view(),name='Suryua_API'),
    path('api/v1/wdupdate/',wdupdate.as_view(),name='wdupdate'),
    path('api/v1/unique_log/',unique_log.as_view(),name='unique_log'),
    path('api/v1/test_email/',Test_Sch.as_view(),name='test_email'),    
    
    
    path('api/v1/sfa_email/',Sfa_email.as_view(),name='sfa_email'),
    path('api/v1/surya_api_email/',Surya_API_email.as_view(),name='surya_api_email'),       
    path('api/v1/sales_upload/',SalesUpload.as_view(),name='sales_upload'),

]