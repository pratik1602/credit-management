from django.contrib import admin
from django.urls import  path

from .views import *

urlpatterns = [

    ###### USER ######

    path('user-register/', RegisterUser.as_view()),
    path('verify-user-otp/', VerifyOTP.as_view()),
    path('resend-otp/', ResendOTP.as_view()),
    path ('register-admin/', RegisterAdmin.as_view()),

    ##### USER #####

    path ('user-profile/', UserProfileView.as_view()),
    path ('edit-profile/', UserProfileView.as_view()),
    path ('delete-profile/', UserProfileView.as_view()),

    ##### ADMIN #####

    path ('admin-profile/', AdminProfileView.as_view()),
    path ('admin-edit-profile/', AdminProfileView.as_view()),
    path ('admin-delete-profile/', AdminProfileView.as_view()),

    ###### LOGIN ######

    path('login-user/', LoginAPIView.as_view()),
    path('login-admin/', LoginAPIView.as_view()),
    
    ###### ADMIN ######

    path ('user-list/', UserListGeneric.as_view()),
    path('verify-admin/', VerifyAdminOTP.as_view()),
    path ('admin-delete-user/', DeleteUserView.as_view()),

    ###### CHANGE PASSWORD ######

    path ('change-password/', UserChangePasswordView.as_view()),

    ###### RESET PASSWORD ###### 
       
    path('reset-password-email/', SendResetPasswordEmail.as_view()),
    path('verify-Reset-pass-OTP/', VerifyResetPasswordOTPView.as_view()),
    path('reset-password/', PasswordResetView.as_view()),

]