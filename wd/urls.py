from django.db import router
from django.urls import include, path
from wd.views import *

urlpatterns = [
    path('api/v1/wd/wd_town/',WDtown.as_view(),name='wd_town'),
    path('api/v1/wd/brand_catagory/',BrandCategory.as_view(),name='brand_catagory'),
    path('api/v1/wd/wd_add_sales/',WDAddSales.as_view(),name='wd_add_sales'),
    path('api/v1/wd/wd_add_sales_new/',WDAddSales_New.as_view(),name='wd_add_sales_new'),
    path('api/v1/wd/add_total_sales/',WD_Total_Sales.as_view(),name='add_total_sales'),
    path('api/v1/wd/Sku_remarks/',Sku_remarks_views.as_view(),name='Sku_remarks'),
    path('api/v1/wd/wd_search/',wd_search.as_view(),name='wd_search'),

]