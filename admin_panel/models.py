from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
# Create your models here.


class txmst(models.Model):
    txid = models.AutoField(primary_key=True, db_column='txid',verbose_name='Tax Id')
    txname=models.CharField(max_length=255,verbose_name='Tax Name',unique=True)
    txdescription = models.CharField(max_length=255,verbose_name='Tax Description')
    txisgst = models.BooleanField(default=True,verbose_name='GST')
    txstatus = models.BooleanField(default=True,verbose_name='Status')
    usrid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
    dtupdatd = models.DateTimeField(auto_now_add=True,verbose_name='Created On')
       
    class Meta:
        verbose_name = "Tax Master"
        verbose_name_plural = "Tax Master"
        db_table = 'txmst'
        
    def __str__(self):
        return self.txname
    
    
class txdet(models.Model):
    tdid = models.AutoField(primary_key=True, db_column='tdid',verbose_name='Tax Detais Id')
    tdtxid = models.ForeignKey(txmst,on_delete=models.CASCADE,verbose_name='Tax Id')
    tdname = models.CharField(max_length=255,verbose_name='Tax Details Name')
    tddescription = models.CharField(max_length=255,verbose_name='Tax Details Description')
    tdcgst = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='CGST Rate')
    tdsgst = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='SGST Rate')
    tdigst = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='IGST Rate')
    tdvat = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='VAT Rate')
    tdcess = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='CESS Rate')
    tdstatus = models.BooleanField(default=True, verbose_name='Status')
    usrid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
    dtupdatd = models.DateTimeField(auto_now_add=True,verbose_name='Created On')
    
    
    class Meta:
        verbose_name = "Tax Details"
        verbose_name_plural = "Tax Details"
        db_table = 'txdet'
        
    def __str__(self):
        return self.tdname
        
        
class formt(models.Model):
    frid = models.AutoField(primary_key=True, db_column='tdid',verbose_name='Id')
    frname = models.CharField(max_length=255,verbose_name='Name',unique=True)
    frdescription = models.CharField(max_length=255,verbose_name='Description')
    frfltr = models.CharField(max_length=255,verbose_name='Format Filter')
    frstatus = models.BooleanField(default=True, verbose_name='Status')
    usrid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
    dtupdatd = models.DateTimeField(auto_now_add=True,verbose_name='Created On')
    
    class Meta:
        verbose_name = "File Format Details"
        verbose_name_plural = "File Format Details"
        db_table = 'formt'
        
    def __str__(self):
        return self.frname
        
    
class crnc(models.Model):
    crid = models.AutoField(primary_key=True, db_column='tdid',verbose_name='Id')
    crname = models.CharField(max_length=100,verbose_name='Name')
    crsymbol = models.CharField(max_length=10,verbose_name='Symbol')
    crdescription = models.TextField(verbose_name='Description')
    crstatus = models.BooleanField(default=True,verbose_name='Status')
    usrid = models.ForeignKey(User,  on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
    dtupdatd = models.DateTimeField(auto_now_add=True,verbose_name='Created On')
    
    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currency"
        db_table = 'crnc'
    
    def __str__(self):
        return self.crname
    

class cntry(models.Model):
    cnid = models.AutoField(primary_key=True, db_column='tdid',verbose_name='Id')
    cnname = models.CharField(max_length=100,verbose_name='Name')
    cndescription = models.TextField(verbose_name='Description')
    cncrid =models.ForeignKey(crnc,  on_delete=models.CASCADE,verbose_name='Currency')
    cntxid = models.ForeignKey(txmst, on_delete=models.CASCADE,verbose_name='Tax')
    # Tax = models.TextField()
    cnstatus = models.BooleanField(default=True,verbose_name='Status')
    usrid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
    dtupdatd = models.DateTimeField(auto_now_add=True,verbose_name='Created On')
    
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Country"
        db_table = 'cntry'
    
    def __str__(self):
        return self.cnname
    

class ctgry(models.Model):
    ctid = models.AutoField(primary_key=True, db_column='tdid',verbose_name='Id')
    ctname = models.CharField(max_length=50,verbose_name='Name')
    ctcode = models.CharField(max_length=50,verbose_name='Code')
    ctdescription = models.TextField(verbose_name='Description')
    ctimg = models.ImageField(upload_to='images/',verbose_name='Image')
    ctstatus = models.BooleanField(default=True,verbose_name='Status')
    usrid = models.ForeignKey(User,  on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
    dtupdatd = models.DateTimeField(auto_now_add=True,verbose_name='Created On')
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"
        db_table = 'ctgry'
        
    def __str__(self):
        return self.ctname
    
class srvc(models.Model):
    svid = models.AutoField(primary_key=True, db_column='tdid',verbose_name='Tax Detais Id')
    svcode = models.CharField(max_length=255,unique=True,verbose_name='Code')
    svname = models.CharField(max_length=255,unique=True,verbose_name='Name')
    svdescription = models.CharField(max_length=255,verbose_name='Description')
    svcategory = models.ForeignKey(ctgry, on_delete=models.CASCADE,verbose_name='Category')
    svcountry = models.ForeignKey(cntry, on_delete=models.CASCADE,verbose_name='Country')
    svrate = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Rate')  #Government Rate
    svratesplit = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Rate Split Up") #Rate Splitup of value in svrate column
    svsrvchg = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Service chg") #IVBMCS Service chg
    discrt = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Discount Rate")
    discamt = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Discount Amt")
    disctxt = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Discount Text")
    svagamt = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Agent Amt")
    svagrt = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Agent Rate")
    svtxid = models.ForeignKey(txmst, on_delete=models.CASCADE,verbose_name="Tax")
    svtxrt = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Tax Rate")
    svtxamt = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Tax Amt")
    svnetamt = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Net Amt")
    svstatus = models.BooleanField(default=True,verbose_name='Status')
    usrid = models.ForeignKey(User,  on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
    dtupdatd = models.DateTimeField(auto_now_add=True,verbose_name='Created On')
    
    class Meta:
        verbose_name = "Services"
        verbose_name_plural = "Services"
        db_table = 'srvc'
    
    def __str__(self):
        return self.svname
    
class DocumentsRequired(models.Model):
    tdid = models.AutoField(primary_key=True, db_column='tdid',verbose_name='Tax Detais Id')
    Service = models.ForeignKey(srvc, on_delete=models.CASCADE)
    DocumentName = models.CharField(max_length=50,verbose_name='Document Name')
    Description = models.TextField() 
    Format = models.ForeignKey(formt, on_delete=models.CASCADE)
    MaxFileSize = models.IntegerField(verbose_name= 'Max File Size')
    Status = models.BooleanField(default=True)
    CreatedBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
    CreatedOn = models.DateTimeField(auto_now_add=True,verbose_name='Created On')
    
    
# demo user model

class UserProfile(models.Model):
    name = models.CharField(max_length=255,verbose_name="Name")
    phone_number = models.CharField(max_length=15,verbose_name="Phone number")
    email = models.EmailField(verbose_name="Email")
    service = models.ForeignKey(srvc, on_delete=models.CASCADE,verbose_name="Service")
    document = models.FileField(upload_to='user_documents/',verbose_name="Upload Document(.pdf)")
    image = models.ImageField(upload_to='user_images/',verbose_name="Upload Image(.jpg/.jpeg)")
    payment = models.BooleanField(verbose_name="Payment")
    taken_by = models.CharField(max_length=255,verbose_name="Taken",blank=True)
    status = models.CharField(max_length=255,verbose_name="Status",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    


