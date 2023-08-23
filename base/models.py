from django.db import models
from django.contrib.auth.models import  AbstractUser

class User(AbstractUser):
    user_id = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(max_length=100,null=True, blank=True)
    user_type = models.CharField(max_length=20,null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    created_by = models.CharField(max_length=100,null=True,blank=True)
    last_modified_on = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    last_modified_by = models.CharField(max_length=101,null=True, blank=True)
    first_login = models.BooleanField(default=False)
    lock_unlock = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    profile_pic = models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    locationcode = models.CharField(max_length=100,null=True, blank=True)
    
    is_logedin = models.BooleanField(default=False)
    token = models.CharField(max_length=255,null=True, blank=True)
    is_reset_password = models.BooleanField(default=False)
    reset_password_date = models.DateTimeField(null=True, blank=True)
    
    invalid_login = models.PositiveIntegerField(default=0)
    last_acive_time = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    first_attempt = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    last_attempt = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    raw_password = models.CharField(max_length=50,null=True, blank=True)
    last_reset_time = models.DateTimeField(blank=True,null=True)
    
    

    def __str__(self):
        return "{}" .format(self.email)
    class Meta:
        db_table = "master_user"
        
# from rest_framework import permissions      
# class BlackListedToken(models.Model):
#     token = models.CharField(max_length=500)
#     user = models.ForeignKey(User, related_name="token_user", on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ("token", "user")

# class IsTokenValid(permissions.BasePermission):
#     def has_permission(self, request, view):
#         user_id = request.user.id            
#         is_allowed_user = True
#         token = request.auth.decode("utf-8")
#         try:
#             is_blackListed = BlackListedToken.objects.get(user=user_id, token=token)
#             if is_blackListed:
#                 is_allowed_user = False
#         except BlackListedToken.DoesNotExist:
#             is_allowed_user = True
#         return is_allowed_user        
        

        
class Password_History(models.Model):
    user_id = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=20, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = "user_password_histrory"
    

class WDmaster(models.Model):
    # wd_id = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    wd_ids = models.CharField(max_length=100, blank=True, null=True)
    wd_name = models.CharField(max_length=100, blank=True, null=True)
    wd_address1 = models.CharField(max_length=150, blank=True, null=True)
    wd_address2 = models.CharField(max_length=150, blank=True, null=True)
    wd_address3 = models.CharField(max_length=150, blank=True, null=True)
    wd_address4 = models.CharField(max_length=150, blank=True, null=True)
    wd_postal_code = models.CharField(max_length=100, blank=True, null=True)
    wd_city = models.CharField(max_length=100, blank=True, null=True)
    wd_state = models.CharField(max_length=100, blank=True, null=True)
    wd_country = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True,)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    last_updated_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.CharField(max_length=100,blank=True, null=True)
    status = models.BooleanField(default=True)
    wd_type = models.CharField(max_length=20,null=True,blank=True)

    class Meta:
        db_table = "master_wdmaster"


class BranchMaster(models.Model):
    branch_id = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    branch_address1 = models.CharField(max_length=150, blank=True, null=True)
    branch_address2	= models.CharField(max_length=150, blank=True, null=True)
    branch_address3 = models.CharField(max_length=150, blank=True, null=True)
    branch_city	= models.CharField(max_length=100, blank=True, null=True)
    branch_postal_code = models.CharField(max_length=100, blank=True, null=True)	
    branch_country_code	= models.CharField(max_length=100, blank=True, null=True)
    branch_country	= models.CharField(max_length=100, blank=True, null=True)
    branch_state = models.CharField(max_length=100, blank=True, null=True)
    branch_code	= models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    created_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    last_updated = models.CharField(max_length=101, unique=True,null=True, blank=True)
    status = models.BooleanField(default=True)
    branch_ids = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "master_branchmaster"
    

class Attendence(models.Model):
    user_id=models.CharField(max_length=25,null=True,blank=True)
    user_type=models.CharField(max_length=30,null=True,blank=True)
    added_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(blank=True, null=True)
    login_count=models.IntegerField(default=1)
    zone =  models.CharField(null=True,blank=True,max_length=150)
    statename =  models.CharField(null=True,blank=True,max_length=150)
    gpi_state =  models.CharField(null=True,blank=True,max_length=150)
    town = models.CharField(null=True,blank=True,max_length=150)
    wd_name = models.CharField(null=True,blank=True,max_length=150)

    class Meta:
        db_table = "master_user_attendance"
        
        
class Access_log(models.Model):
    user_id=models.CharField(max_length=100,null=True,blank=True)
    user_type=models.CharField(max_length=100,null=True,blank=True)
    sales_save_date=models.DateField(max_length=100,null=True,blank=True)
    town_code=models.CharField(max_length=20,null=True,blank=True)
    created_at=models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=20,null=True,blank=True)
    updated_on=models.DateTimeField(blank=True, null=True)
    updated_by=models.CharField(max_length=20,null=True,blank=True)
    count=models.IntegerField(default=1)
    town = models.CharField(null=True,blank=True,max_length=150)
    wd_name = models.CharField(null=True,blank=True,max_length=150)
    zone =  models.CharField(null=True,blank=True,max_length=150)
    statename =  models.CharField(null=True,blank=True,max_length=150)
    gpi_state =  models.CharField(null=True,blank=True,max_length=150)
    


    class Meta:
        db_table="access_log"
        
        
class Weeklysales_update_log(models.Model):
    wd_id = models.CharField(max_length=100,blank=True,null=True)
    sku_id = models.CharField(max_length=100,blank=True,null=True)
    wd_town_id = models.CharField(max_length=100,blank=True,null=True)
    branch_id = models.CharField(max_length=100,blank=True,null=True)
    previous_quantity= models.FloatField(max_length=100,blank=True,null=True)
    new_quantity = models.FloatField(max_length=100,blank=True,null=True)
    sales_type = models.CharField(max_length=100,blank=True,null=True)
    month = models.CharField(max_length=100,blank=True,null=True)
    week = models.CharField(max_length=100,blank=True,null=True)
    year= models.CharField(max_length=100,blank=True,null=True)
    transaction_type= models.CharField(max_length=100,blank=True,null=True)
    brand_category= models.CharField(max_length=100,blank=True,null=True)
    sku_name = models.CharField(max_length=200,blank=True,null=True)
    sku_code = models.CharField(max_length=100,blank=True,null=True)
    updated_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    is_sent = models.BooleanField(default=False)
    class Meta:
        db_table="weekly_update_log"