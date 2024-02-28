from django.db import models
from admin_panel.models import *
# Create your models here.

class Free_consult_detail(models.Model):
    phone_number = models.CharField(max_length=15,verbose_name="Phone number")
    service = models.CharField(max_length=15,blank=True,verbose_name="Service")
    
    
class userdata(models.Model):
    name = models.CharField(max_length=255,verbose_name="Name",blank = True)
    phone_number = models.CharField(max_length=15,verbose_name="Phone number",unique=True,blank = True)
    email = models.EmailField(verbose_name="Email",blank = True)
    status = models.CharField(max_length=255,verbose_name="Status",blank = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
        # return f'{self.email} - {self.phone_number}'
    
    
class user_service_details(models.Model):
    user_id = models.ForeignKey(CustomUser,on_delete = models.CASCADE,verbose_name = "user_id")
    service = models.ForeignKey(srvc, verbose_name="Service", on_delete=models.CASCADE)
    payment = models.BooleanField(verbose_name="Payment",default=False,blank=True)
    msg = models.TextField(verbose_name="user Query",blank=True)
    documents = models.JSONField(verbose_name="Documents",blank=True, default='')
    taken_by = models.CharField(max_length=255,verbose_name="Taken",blank=True)
    status = models.CharField(max_length=255,verbose_name="Status",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.service.svname
        # return f'{self.user_id.name} - {self.service}'
    
    
class user_notification(models.Model):
    recepient= models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    service=models.ForeignKey(srvc,on_delete=models.CASCADE,default='')
    # sender = models.ForeignKey(Staff,on_delete=models.DO_NOTHING)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)