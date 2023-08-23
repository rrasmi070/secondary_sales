# from base.models import User
# from rest_framework import permissions
# from django.contrib.auth.models import Group
# permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

# class IsWD(permissions.BasePermission):
#     def has_permission(self, request, view):
#         try:
#             roles = User.objects.get(username_type='WD')
#         except User.DoesNotExist:
#             roles = User.objects.create(username_type='WD')

#         if request.user.roles.username_type == 'WD':
#             return request.user


# class IsManager(permissions.BasePermission):
#     def has_permission(self, request, view):
#         try:
#             roles = User.objects.get(username_type='MANAGER')
#         except User.DoesNotExist:
#             roles = User.objects.create(username_type='MANAGER')

#         if request.user.roles.username_type == 'MANAGER':
#             return request.user




class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # ajay.

    def __call__(self, request):
        response = self.get_response(request)
        # response.__setitem__('Server', 'sdggfkklk')
        del response['Server']
        response.headers['Server'] = ""
        response.headers['X-Frame-Options'] = ""
        # response.headers['Content-Length'] = ""
        response.headers['X-Content-Type-Options'] = ""
        response.headers['Date'] = ""
        response.headers['Vary'] = ""
        response.headers['Referrer-Policy'] = ""
        return response

class SimpleMiddlewareA:
    def __init__(self, get_response):
        self.get_response = get_response
        # ajay.

    def __call__(self, request):
        response = self.get_response(request)
        response.__setitem__('Allow', '')
        del response['Allow']
        return response



#gfgkjhljkljhkm




