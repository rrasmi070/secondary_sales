from django.db import router
from django.urls import include, path
from rest_framework import routers
from branch_user.views import *

from branch_user.reports import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('data',Auto_freez, basename='freez-data')

urlpatterns = [
    path('api/v1/branch_user/skulist/',Skulist.as_view(),name='skulist'),
    path('api/v1/branch_user/get_wd_list/',GetWDList.as_view(),name='get_wd_list'),
    path('api/v1/branch_user/sales_skulist/',SalesSkulist.as_view(),name='sales_skulist'),
    path('api/v1/branch_user/lock_unlock/',LockUnlock_user.as_view(),name='lock_unlock'),
    # path('api/v1/branch_user/Skulistforadd/',Gets.as_view(),name='skulist'),
    path('api/v1/branch_user/report_get/',Report_get.as_view(),name='report_get'),
    path('api/v1/branch_user/weekly_report_get/',WeeklyReport_get.as_view(),name='weekly_report_get'),
    # path('api/v1/branch_user/attendance_report_get/',Attendence_Report_get.as_view(),name='weekly_report_get'),
    path('api/v1/branch_user/attendence_access_Report/',Attendence_access_Report.as_view(),name='Attendence_access_log_report'),
    path('api/v1/branch_user/towm_wise_wd/',Towm_wise_wd.as_view(),name='towm_wise_wd'),

    path('api/v1/branch_user/towns_of_wd/',Towns_of_WD.as_view(),name='towns_of_wd'),


    path('api/v1/branch_user/manualy_crate_weekly/',manualy_crate_weekly.as_view(),name='manualy_crate_weekly'),
    path('api/v1/branch_user/manualy_crate_weekly_new/',Create_Update_Weekly_Sales.as_view(),name='manualy_crate_weekly_new'),
    path('api/v1/branch_user/weekly_update_unfreeze/',Schedule_Week_update_code.as_view(),name='weekly_update_unfreeze'),
    path('api/v1/branch_user/manualy_crate_weekly_by_date/',manualy_crate_weekly_by_date.as_view(),name='manualy_crate_weekly_by_date'),
    
    
    # new==========================
    path('api/v1/branch_user/Skulistforadd/',Gets_sales_new.as_view(),name='get_sales_new'),
    path('api/v1/branch_user/check_timeing/',Check_timeing.as_view(),name='check_timeing'),

]