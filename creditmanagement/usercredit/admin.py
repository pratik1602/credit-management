from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from datetime import datetime
from django.contrib.auth.models import Group

# Register your models here.

User  = get_user_model()
admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['id','email', 'is_verified', 'is_admin','under_by'] #'aadhar_status','pan_status','cheque_status', 'commission_status', 
    list_filter = ['role',]
    list_editable = ['is_verified'] #'aadhar_status','pan_status','cheque_status',
    list_per_page = 10
    fieldsets = (
        ('User Credentials', {'fields': ('email','password')}),
        ('Personal info', {'fields': ('under_by','first_name', 'last_name', 'phone_no', 'aadhar','aadhar_status','pan','pan_status','cheque','cheque_status','otp' ,'refer_code','referred_by','tc', 'commission_status','created_by','user_created_at','modified_by', 'user_modified_at')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff', 'is_verified', 'role')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','first_name', 'last_name', 'phone_no', 'aadhar','pan','cheque','tc','role','is_admin', 'is_active', 'is_staff','commission_status',)}
        ),
    )
    readonly_fields = ('user_created_at','user_modified_at',)
    search_fields = ['email']
    ordering = ['id']
    filter_horizontal = ()


    def save_model(self, request, obj, form, change):
        time_date = datetime.now()
        if change:
            obj.modified_by = request.user
            obj.user_modified_at = time_date

        else:                    
            obj.created_by = request.user

        obj.save()                         
        return super(UserAdmin, self).save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)

########## CARDS ADMIN #########

class CardsAdmin(admin.ModelAdmin):
    list_display = ['card_id', 'card_holder_name','card_type','due_date', 'due_amount', 'commission','commission_total_amount', 'paid_by','card_status']
    list_filter = ('card_status', 'card_type' )
    search_fields = ('card_holder_name','card_id',)
    list_editable = ['commission', 'card_status']
    readonly_fields = ('created_at','modified_at',)
    ordering = ('card_id',)
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        
        if change:
            obj.updated_by = request.user
            obj.commission_total_amount = obj.due_amount * obj.commission/100
            obj.paid_by = request.user
            obj.card_status = True
        else:                    
            obj.created_by = request.user
            obj.commission_total_amount = obj.due_amount * obj.commission/100
        obj.save()            
        return super(CardsAdmin, self).save_model(request, obj, form, change)

admin.site.register(Card, CardsAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'card', 'amount_paid','commission', 'profit_amount']

    def save_model(self, request, obj, form, change):

        if change:
            obj.profit_amount = obj.amount_paid * obj.commission/100
            obj.paid_at = datetime.now()
        else:                    
            obj.profit_amount = obj.amount_paid * obj.commission/100
        obj.save()            
        return super(TransactionAdmin, self).save_model(request, obj, form, change)

admin.site.register(Transaction, TransactionAdmin)
