from django.db.models import Q
import json
import pandas as pd
from rest_framework import serializers
from master.master_serializer import *
from rest_framework import serializers
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from master.email import mail_func

class MasteruserCSVFileUploadGenerics(generics.GenericAPIView):
    # permission_classes = (permissions.IsAuthenticated)
    serializer_class = MasterUserCSVFileUploadFieldagentSerializer
    parser_classes = (FormParser, MultiPartParser)
    
    def post(self, request, *args, **kwargs):
        try:
            request.data['error_msg'] = None
            serializer = self.serializer_class(data=request.data) # , context={'request':request}
            if serializer.is_valid():
                context = {'status': True,'message': "Success","data":serializer.data['error_msg']}
            else:
                context = {'status': False,'message': serializer.errors}
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            context = {'status': False, 'message': {"error": str(e)}}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WDMasterCSVFileUploadGenerics(generics.GenericAPIView):
    serializer_class = WdMasterCSVFileUploadFieldagentSerializer
    parser_classes = (FormParser, MultiPartParser)
    def post(self, request, *args, **kwargs):
        # try:
            request.data['error_msg'] = None
            serializer = self.serializer_class(data=request.data) # , context={'request':request}
            if serializer.is_valid():
                context = {'status': True,'message': "Success","data":serializer.data['error_msg']}
            else:
                context = {'status': False,'message': serializer.errors}
            return Response(context, status=status.HTTP_200_OK)
        # except Exception as e:
        #     context = {'status': False, 'message': {"error": str(e)}}
        #     return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HeirarchymasterMasterCSVFileUploadFieldagentGenerics(generics.GenericAPIView):
    serializer_class = HeirarchymasterMasterCSVFileUploadFieldagentSerializer
    parser_classes = (FormParser, MultiPartParser)
    def post(self, request, *args, **kwargs):
        try:
            request.data['error_msg'] = None
            serializer = self.serializer_class(data=request.data) # , context={'request':request}
            if serializer.is_valid():
                context = {'status': True,'message': "Success","data":serializer.data['error_msg']}
            else:
                context = {'status': False,'message': serializer.errors}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {'status': False, 'message': {"error": str(e)}}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HeirarchymasterMasterCSVFileUploadFieldagentGenerics(generics.GenericAPIView):
    serializer_class = HeirarchymasterMasterCSVFileUploadFieldagentSerializer
    parser_classes = (FormParser, MultiPartParser)
    def post(self, request, *args, **kwargs):
        # try:
            request.data['error_msg'] = None
            serializer = self.serializer_class(data=request.data) # , context={'request':request}
            if serializer.is_valid():
                context = {'status': True,'message': "Success","data":serializer.data['error_msg']}
            else:
                context = {'status': False,'message': serializer.errors}
            return Response(context, status=status.HTTP_200_OK)
        # except Exception as e:
        #     context = {'status': False, 'message': {"error": str(e)}}
        #     return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
class MasterWdSkuCategory(generics.GenericAPIView):
    serializer_class=MasterWdSkuCategoryCSVFileUploadSerializer
    parser_classes=(FormParser, MultiPartParser)
    
    def post(self,request, *args, **kwargs):
        request.data['error_msg']=None
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            context={'status':True,'message':"Success","data":serializer.data['error_msg']}
        else:
            context = {'status': False,'message': serializer.errors}
        return Response(context, status=status.HTTP_200_OK)
        
    

class MasterWdSkuCategoryUpdate(generics.GenericAPIView):
    serializer_class=MasterWdSkuCategoryUpdateCSVFileUploadSerializer
    parser_classes=(FormParser, MultiPartParser)
    
    def post(self,request, *args, **kwargs):
        request.data['error_msg']=None
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            # response = HttpResponse(content_type='text/xlsx')
            # response['Content-Disposition'] = 'attachment; filename="Sku_upload_remark.xlsx"'
            df = pd.DataFrame.from_dict(serializer.data['error_msg'])
            
            # record = df.to_csv (response, index = False)
            df.to_excel(r'media/Sales_hir_master_remarks.xlsx', index=False)
            # aq = df.to_excel( excel_writer, sheet_name='Sheet1', )
            # aq=df.to_excel("Sku_upload_remark.xlsx")
            sheet="media/Sales_hir_master_remarks.xlsx"
            subject="SKU Mapping Remarks Attachment."
            # base_url = f"{request.scheme}://" +f"{request.get_host()}/media/fgileName.xlsx"
            html_message="<p>SKU Mapping Remarks file is  attached below</p>"
            pass_to_email = ['rasmis@triazinesoft.com','kamalkantu@triazinesoft.com'] #,'saurabha@triazinesoft.com']
            
            # df.to_excel('Courses.xlsx')
            mail_func(pass_to_email,subject,html_message,sheet)
            
            if mail_func:
                pass
                
                
            #     dict = {'massage': 'An email has been sent to reset your password', 'status': True}
            #     return Response(dict, status=status.HTTP_200_OK)
            # else:
            #     dict = {'massage': 'data not found', 'status': False}
            #     return Response(dict, status=status.HTTP_200_OK)
            
            
            context={'status':True,'message':"Success","data":serializer.data['error_msg']}
        else:
            context = {'status': False,'message': serializer.errors}
        return Response(context, status=status.HTTP_200_OK)
    

class MasterWdSkuCategoryUpdate(generics.GenericAPIView):
    serializer_class=MasterWdSkuCategoryUpdateCSVFileUploadSerializer
    parser_classes=(FormParser, MultiPartParser)
    
    def post(self,request, *args, **kwargs):
        request.data['error_msg']=None
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            # response = HttpResponse(content_type='text/xlsx')
            # response['Content-Disposition'] = 'attachment; filename="Sku_upload_remark.xlsx"'
            df = pd.DataFrame.from_dict(serializer.data['error_msg'])
            
            # record = df.to_csv (response, index = False)
            df.to_excel(r'media/Sales_hir_master_remarks.xlsx', index=False)
            # aq = df.to_excel( excel_writer, sheet_name='Sheet1', )
            # aq=df.to_excel("Sku_upload_remark.xlsx")
            sheet="media/Sales_hir_master_remarks.xlsx"
            subject="SKU Mapping Remarks Attachment."
            # base_url = f"{request.scheme}://" +f"{request.get_host()}/media/fgileName.xlsx"
            html_message="<p>SKU Mapping Remarks file is  attached below</p>"
            pass_to_email = ['rasmis@triazinesoft.com','kamalkantu@triazinesoft.com'] #,'saurabha@triazinesoft.com']
            
            # df.to_excel('Courses.xlsx')
            # mail_func(pass_to_email,subject,html_message,sheet)
            
            # if mail_func:
            #     pass
                
                
            #     dict = {'massage': 'An email has been sent to reset your password', 'status': True}
            #     return Response(dict, status=status.HTTP_200_OK)
            # else:
            #     dict = {'massage': 'data not found', 'status': False}
            #     return Response(dict, status=status.HTTP_200_OK)
            
            
            context={'status':True,'message':"Success","data":serializer.data['error_msg']}
        else:
            context = {'status': False,'message': serializer.errors}
        return Response(context, status=status.HTTP_200_OK)
    
    
@method_decorator(csrf_exempt, name='dispatch')
class Skumasterproduct(generics.GenericAPIView):
    serializer_class=SkumasterproductUploadSerializer
    parser_classes=(FormParser, MultiPartParser)
    
    def post(self,request, *args, **kwargs):
            request.data['error_msg']=None
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid():
                context={'status':True,'message':"Success","data":serializer.data['error_msg']}
            else:
                context = {'status': False,'message': serializer.errors}
            return Response(context, status=status.HTTP_200_OK)


class MasterWdSkuCategoryUpdate_Town_id(generics.GenericAPIView):
    serializer_class=MasterWdSkuCategoryUpdate_town_id_CSVFileUploadSerializer
    parser_classes=(FormParser, MultiPartParser)
    
    def post(self,request, *args, **kwargs):
        request.data['error_msg']=None
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            
            df = pd.DataFrame.from_dict(serializer.data['error_msg'])
            
            context={'status':True,'message':"Success","data":serializer.data['error_msg']}
        else:
            context = {'status': False,'message': serializer.errors}
        return Response(context, status=status.HTTP_200_OK)