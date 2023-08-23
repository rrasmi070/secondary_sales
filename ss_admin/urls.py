from django.db import router
from django.urls import include, path
from ss_admin.admin_view import  DatauploadCSVFileDownload, SkuActiveInactive, SkuMasterDownload, SkuMasterlist, WDActiveInactive, WDMasterUserList
from ss_admin.views import *

urlpatterns = [
    path('api/v1/test/',Test.as_view(),name='test'),
    path('api/v1/branchlist/',BranchList.as_view(),name='branchlist'),
    path('api/v1/wdtownlist/',WDTownlist.as_view(),name='wdtownlist'),
    path('api/v1/wdlist/',WDlist.as_view(),name='wdlist'),
    path('api/v1/masteruploadformat/<str:type>',DatauploadCSVFileDownload.as_view(),name='DatauploadCSVFileDownload'),
    path('api/v1/skumasterlist/',SkuMasterlist.as_view(),name='skumasterlist'),
    path('api/v1/skumasterdownload/',SkuMasterDownload.as_view(),name='skumasterdownload'),
    path('api/v1/wduserlist/',WDMasterUserList.as_view(),name='wduserlist'),
    path('api/v1/skuactiveinactive/',SkuActiveInactive.as_view(),name='skuactiveinactive'),
    path('api/v1/wdactiveinactive/',WDActiveInactive.as_view(),name='wdactiveinactive'),
    
    

    
    
    
    
    
    
    
    # path('api/v1/wdbranchlist/',GetWDLBranchist.as_view(),name='wdbranchlist'),
    # path('api/v1/adminreport/',Admin_HO_Report_get.as_view(),name='adminreport'),
    
    
    
    
    

]