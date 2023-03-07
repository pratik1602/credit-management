from django.contrib import admin
from django.urls import  path

from usercredit.api.views import *

urlpatterns = [

    ###### USER ######

    path('user-register', RegisterUser.as_view(), name= "RegisterUser"),
    path('verify-user-otp', VerifyOTP.as_view(), name="VerifyOTP"),
    path('resend-otp', ResendOTP.as_view(), name="ResendOTP"),
    path ('register-admin', RegisterAdmin.as_view(), name="RegisterAdmin"),

    ##### USER #####

    path ('user-profile', UserProfileView.as_view(), name="UserProfileView"),
    path ('edit-profile', UserProfileView.as_view(), name="UserProfileView"),
    path ('delete-profile', UserProfileView.as_view(), name="UserProfileView"),

    ##### ADMIN #####

    path ('admin-profile', AdminProfileView.as_view(), name="AdminProfileView"),
    path ('admin-edit-profile', AdminProfileView.as_view(), name="AdminProfileView"),
    path ('admin-delete-profile', AdminProfileView.as_view(), name="AdminProfileView"),

    ###### LOGIN ######

    path('login-user', LoginAPIView.as_view(), name="LoginAPIView"),
    path('login-admin', LoginAPIView.as_view(), name="LoginAPIView"),
    
    ###### ADMIN ACCESSES ######

    path ('user-list', GetUserList.as_view(), name="GetUserList"),
    path ('admin-delete-user', DeleteUserView.as_view(), name="DeleteUserView"),

    ###### VERIFY ADMIN WITH OTP ######

    path('verify-admin', VerifyAdminOTP.as_view(), name="VerifyAdminOTP"),

    ###### CHANGE PASSWORD ######

    path ('change-password', UserChangePasswordView.as_view(), name="UserChangePasswordView"),

    ###### RESET PASSWORD ###### 
       
    path('reset-password-email', SendResetPasswordEmail.as_view(), name="SendResetPasswordEmail"),
    path('verify-Reset-pass-OTP', VerifyResetPasswordOTPView.as_view(), name="VerifyResetPasswordOTPView"),
    path('reset-password', PasswordResetView.as_view(), name="PasswordResetView"),

]