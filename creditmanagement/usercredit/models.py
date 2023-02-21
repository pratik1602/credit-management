from django.db import models
from django.contrib.auth.models import  AbstractBaseUser
from usercredit.cards.validate import *
from usercredit.manager import *
from django.core.validators import MaxValueValidator, MinValueValidator
percentage_validators=[MinValueValidator(0.9), MaxValueValidator(100)]
from django.conf import settings
from usercredit.utils import *
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):

    ADMIN = 1
    USER = 2

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (USER, 'User'),
    )   

    username = None
    profile_pic =  models.ImageField(upload_to='',default="")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=12)
    aadhar = models.ImageField(upload_to='',default="")
    aadhar_status = models.BooleanField(default=False)
    pan = models.ImageField(upload_to='',default="")
    pan_status = models.BooleanField(default=False)
    cheque = models.ImageField(upload_to='',default="")
    cheque_status = models.BooleanField(default=False)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=2)
    is_verified = models.BooleanField(default=False)
    is_active =  models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_admin = models.BooleanField(default=False)
    tc = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    refer_code = models.CharField(max_length=8, blank=True, null=True)
    referred_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='usercredit_User_referred_by')
    commission_status = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='usercredit_User_created_by')
    modified_by =  models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='usercredit_User_modified_by')
    user_created_at = models.DateTimeField(default=datetime.now)
    user_modified_at = models.DateTimeField(default=datetime.now)
    
    USERNAME_FIELD =  'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_no', ]

    objects = UserManager()


    def has_perm(self, perm, obj=None):
        return self.is_admin

    def  has_module_perms(self, app_label):
        return self.is_admin

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.refer_code == "":
            refer_code = generate_ref_code()
            self.refer_code = refer_code
        super().save(*args, **kwargs)


class Card(models.Model):  

    card_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    CARD_CHOICE = (("business", "BUSINESS"),
                ("personal", "PERSONAL"),)
    card_bank_name = models.CharField(max_length=100)
    card_type = models.CharField(max_length=15, choices=CARD_CHOICE)
    card_number = models.PositiveBigIntegerField( unique=True) #validators=[validate_card_number],
    card_holder_name= models.CharField(max_length=100)
    card_photo = models.CharField(max_length=100)   
    card_exp_date = models.DateField() #validators=[is_expired]
    card_cvv = models.IntegerField() #validators=[validate_cvv]
    due_date = models.DateField() #validators=[has_expired]
    commission = models.FloatField(validators=percentage_validators, blank=True, null=True)
    due_amount = models.FloatField(default=0)
    card_status = models.BooleanField(default=False)
    updated_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_by_user', on_delete=models.SET_NULL,  null=True, blank=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_by_user',on_delete=models.SET_NULL,  null=True, blank=True)
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='paid_by_user', on_delete=models.SET_NULL, null=True, blank=True) 
    commission_total_amount = models.FloatField(null=True,blank=True)
    commission_paid_through = models.CharField(max_length=100)
    created_at = models.DateTimeField(default= datetime.now)
    modified_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.card_bank_name      