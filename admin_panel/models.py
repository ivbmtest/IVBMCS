from django.db import models
from django.contrib.auth.models import User,UserManager
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from django.contrib.auth.models import AbstractUser,BaseUserManager, Permission, Group
from django.contrib.auth.hashers import make_password
from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

# User = get_user_model()

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE = ((1, "Admin"), (2, "Staff"), (3, "Agent"), (4, "User"))
    GENDER = [("M", "Male"), ("F", "Female")]
    
    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField(upload_to='images/')
    address = models.TextField()
    fcm_token = models.TextField(default="")  # For firebase notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Set to an empty list since 'username' is not used
    objects = CustomUserManager()

    def __str__(self):
        return self.first_name
        # return f"{self.last_name}, {self.first_name}"

 # Add or change related_name to avoid clashes
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
   
class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class Agent(models.Model):
    agent_id=models.TextField(default='')
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=' ')

    def __str__(self):
        # return self.admin.id
        return self.admin.last_name + ", " + self.admin.first_name
    
class ctgry(models.Model):
    ctid = models.AutoField(primary_key=True, db_column='tdid',verbose_name='Id')
    ctname = models.CharField(max_length=50,verbose_name='Name')
    ctcode = models.CharField(max_length=50,verbose_name='Code')
    ctdescription = models.TextField(verbose_name='Description')
    ctimg = models.ImageField(upload_to='images/',verbose_name='Image')
    ctstatus = models.IntegerField(verbose_name='Status')
    usrid = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
    dtupdatd = models.DateTimeField(auto_now_add=True,verbose_name='Created On')
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"
        db_table = 'ctgry'
        
    def __str__(self):
        return self.ctname
    
    
class Staff(models.Model):
    category = models.ForeignKey(ctgry, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name

class Users(models.Model):
    # course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name
    
    

class txmst(models.Model):
    txid = models.AutoField(primary_key=True, db_column='txid',verbose_name='Tax Id')
    txname=models.CharField(max_length=255,verbose_name='Tax Name',unique=True)
    txdescription = models.CharField(max_length=255,verbose_name='Tax Description')
    txisgst = models.BooleanField(default=True,verbose_name='GST')
    txstatus = models.IntegerField(verbose_name='Status')
    usrid = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
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
    tdstatus = models.IntegerField(verbose_name='Status')
    usrid = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
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
    frstatus = models.IntegerField(verbose_name='Status')
    usrid = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
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
    crstatus = models.IntegerField(verbose_name='Status')
    usrid = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, 
                              null=True, editable=False,verbose_name="Created By")
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
    cnstatus = models.IntegerField(verbose_name='Status')
    usrid = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
    dtupdatd = models.DateTimeField(auto_now_add=True,verbose_name='Created On')
    
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Country"
        db_table = 'cntry'
    
    def __str__(self):
        return self.cnname
    


    
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

    svdoccolltime =  models.DecimalField(max_digits=5, decimal_places=2,verbose_name="Doc Collection Time(hrs)",null=True,blank=False)
    svproctime =  models.DecimalField(max_digits=5, decimal_places=2,verbose_name="Process request Time(hrs)",null=True,blank=False)
    svprovtime =  models.DecimalField(max_digits=5, decimal_places=2,verbose_name="Service provider Time(hrs)",null=True,blank=False)
    svstatus = models.IntegerField(verbose_name='Status')
    usrid = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
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
    Status = models.IntegerField(verbose_name='Status')
    CreatedBy = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
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

class states(models.Model):
    stid  = models.AutoField(primary_key=True, db_column='stid',verbose_name='State Id')
    stname  = models.CharField(max_length=255,verbose_name="State/Province Name",unique=True)
    stdescription  = models.CharField(max_length=255,verbose_name="Description")
    stcnid  = models.ForeignKey(cntry, on_delete=models.CASCADE,verbose_name='Country')
    sttxcode  = models.CharField(max_length=255,verbose_name="Tax Code")
    usrid = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
    dtupdatd  = models.DateTimeField(auto_now_add=True)
    cnstatus  = models.IntegerField(verbose_name='Status')

    def __str__(self):
        return self.stname


class clnt(models.Model):
    clid = models.AutoField(primary_key=True, db_column='clid',verbose_name='Client Id')
    clcode = models.CharField(max_length=255,verbose_name="Client code",unique=True)
    clname = models.CharField(max_length=255,verbose_name="Client Name")
    clagid = models.IntegerField(verbose_name= 'Agent ID')
    claddress = models.CharField(max_length=255,verbose_name="Client Address")
    clcnid = models.ForeignKey(cntry, on_delete=models.CASCADE,verbose_name='Country')
    clstid =  models.ForeignKey(states, on_delete=models.CASCADE,verbose_name='States')
    clmobno = models.CharField(max_length=255,verbose_name="Mob No: ")
    clmobvrfd = models.IntegerField(verbose_name= 'Mobno verified')
    clmobvrfcode =  models.CharField(max_length=255,verbose_name="Verification Code")
    clemail = models.CharField(max_length=255,verbose_name="Email")
    clemailvrfd = models.IntegerField(verbose_name= 'Email Verified')
    clemailvrfcode = models.CharField(max_length=255,verbose_name="Verification Code")
    usrid = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
    dtupdatd = models.DateTimeField(auto_now_add=True)
    clstatus = models.IntegerField(verbose_name='Status')
    
    

    def __str__(self):
        return self.clname
  

class clsubsdet(models.Model):
    csid  = models.AutoField(primary_key=True, db_column='csid',verbose_name='Client sub ID')
    csclid  = models.ForeignKey(clnt, on_delete=models.CASCADE,verbose_name='Client')
    csslno  = models.IntegerField(verbose_name= 'Sl No')
    cssvid  = models.ForeignKey(srvc, on_delete=models.CASCADE,verbose_name='Service')
    cssubsdate  = models.DateTimeField(verbose_name= 'Sub date')
    csvldprd  = models.IntegerField(verbose_name= 'Sub period')
    csvldprdunt  = models.IntegerField(verbose_name= 'Sub unit')
    cssubsexpdate  = models.DateTimeField(verbose_name='Sub Expiry Date')
    csrate  = models.DecimalField(max_digits=18, decimal_places=3,verbose_name="Govt Rate")
    cssrvchg  = models.DecimalField(max_digits=18, decimal_places=3,verbose_name="IVBMCS Ser Charge")
    csdiscrt  = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Discount Rate")
    csdiscamt  = models.DecimalField(max_digits=18, decimal_places=3,verbose_name="Discount Amt")
    csagrt  = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Agent Rate")
    csagamt  = models.DecimalField(max_digits=18, decimal_places=3,verbose_name="Agent Amt")
    cstxrt  = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Tax Rate")
    cstxamt  = models.DecimalField(max_digits=18, decimal_places=3,verbose_name="Tax Amt")
    csnetamt  = models.DecimalField(max_digits=18, decimal_places=3,verbose_name="Net Rate")
    usrid = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
    dtupdatd  = models.DateTimeField(auto_now_add=True)
    csstatus  = models.IntegerField(verbose_name='Status')

    

# class admcat(models.Model):
#     acid = models.AutoField(primary_key=True, db_column='acid',verbose_name='Admin Cat ID')
#     acname = models.CharField(max_length=255,verbose_name="Admin Cat Name",unique=True)
#     acdescription =  models.CharField(max_length=255,verbose_name="Description")
#     acisadm =  models.IntegerField(verbose_name= 'admin or user') #NA
#     usrid = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
#     dtupdatd = models.DateTimeField(auto_now_add=True)
#     acstatus = models.IntegerField(verbose_name='Status')

#     def __str__(self):
#         return self.acname

# class admroles(models.Model):
#     arid = models.AutoField(primary_key=True, db_column='arid',verbose_name='Admin role ID')
#     aracid = models.ForeignKey(admcat, on_delete=models.CASCADE,verbose_name='Admin Cat')
#     arsvid = models.IntegerField(verbose_name= 'Service Id')
#     usrid = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, null=True, editable=False,verbose_name="Created By")
#     dtupdatd = models.DateTimeField(auto_now_add=True)
#     arstatus = models.IntegerField(verbose_name='Status')


    

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Agent.objects.create(admin=instance)
        if instance.user_type == 4:
            Users.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.agent.save()
    if instance.user_type == 4:
        instance.users.save()
    
    