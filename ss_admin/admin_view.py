from base.models import BranchMaster, User, WDmaster
# from base.serializers import BranchMasterSerializer
from master.models import SKU_Master_Product
from rest_framework import generics
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from ss_admin.paginator import Page25pagination
from ss_admin.serializers import *
from rest_framework.permissions import (AllowAny,IsAuthenticated)
from rest_framework.parsers import FormParser, MultiPartParser
from django.http import HttpResponse
import pandas as pd

from rest_framework.views import APIView


class DatauploadCSVFileDownload(generics.GenericAPIView):
    def get(self,request,type):
        type=str(type)
        try:
            if type=="MasterProduct":
                base_url = f"{request.scheme}://" +f"{request.get_host()}/media/master_format/Sku_master_product.xlsx"
                context = {'status': True,'message': 'File record is downloading.','data':base_url}
            
            
            if type=="MasterUser":
                base_url = f"{request.scheme}://" +f"{request.get_host()}/media/master_format/Masteruser.xlsx"
                context = {'status': True,'message': 'File record is downloading.','data':base_url}
                
            
            if type=="WDuser":
                base_url = f"{request.scheme}://" +f"{request.get_host()}/media/master_format/Wdmaster.xlsx"
                context = {'status': True,'message': 'File record is downloading.','data':base_url}
                
            
            if type=="HirMaster":
                base_url = f"{request.scheme}://" +f"{request.get_host()}/media/master_format/hir_master.xlsx"
                context = {'status': True,'message': 'File record is downloading.','data':base_url}
                
            
            if type=="Skumapping":
                base_url = f"{request.scheme}://" +f"{request.get_host()}/media/master_format/skumapping.xlsx"
                context = {'status': True,'message': 'File record is downloading.','data':base_url}
            
            
            
            
            return Response(context, status=status.HTTP_200_OK) 
        except Exception as e:
            # logger.error(f'FailedCSVExcelReportUser:error => {str(e)}')
            context = {'status': False, 'error': {'message': ['Something Went Wrong']}}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
        


class SkuMasterlist(generics.ListAPIView):
    pagination_class=Page25pagination
    serializer_class=Sku_master_serializer
    # permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        try:           
            data = SKU_Master_Product.objects.all()
            return data
        except Exception as e:  
            context = {'status': False, 'message': {"error": str(e)}}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    

class SkuMasterDownload(generics.GenericAPIView):
    serializer_class=Sku_master_serializer
    # permission_classes = (IsAuthenticated,)
    def get(self,request):
        try:           
            data = SKU_Master_Product.objects.filter(status = True).all()
            serializers=self.serializer_class(data,many=True)
            context = {'status': True, 'message': "Data found Successfully","data":serializers.data}
            
            return Response(context, status=status.HTTP_200_OK)  
        except Exception as e:  
            context = {'status': False, 'message': {"error": str(e)}}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    
class WDMasterUserList(generics.ListAPIView):
    serializer_class=WDMasterSerializer
    pagination_class=Page25pagination
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        try:           
            data = WDmaster.objects.filter().all()
            return data
        except Exception as e:  
            context = {'status': False, 'message': {"error": str(e)}}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class SkuActiveInactive(APIView):
    def post(self,request):
        try:
            check = request.GET.get("id",None)
            skstatus=SKU_Master_Product.objects.filter(id=check).last()
            if skstatus.status==1:
                skstatus.status=0
                skstatus.save()
                # skustatus=SKU_Master_Product.objects.update(sku_code=check,status=0)
                context = {'status': True,'message': "InActive successfully"}
            elif skstatus.status==0:
                skstatus.status=1
                skstatus.save()
                # skustatus=SKU_Master_Product.objects.update(sku_code=check,status=1)
                context = {'status': True,'message': "Active successfully"}
                
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:  
            context = {'status': False, 'message': {"error": str(e)}}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
            

class WDActiveInactive(APIView):
    def post(self,request):
        try:
            check = request.data["id"]
           
            skstatus=User.objects.filter(id=check).last()
            if skstatus.status==1:
                skstatus.status=0
                skstatus.save()
                context = {'status': True,'message': "InActive successfully"}
            elif skstatus.status==0:
                
                skstatus.status=1
                skstatus.save()
                context = {'status': True,'message': "Active successfully"}
                
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:  
            context = {'status': False, 'message': {"error": str(e)}}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
            
            
                    
            
            
                        
    