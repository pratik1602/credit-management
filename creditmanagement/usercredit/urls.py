from django.contrib import admin
from django.urls import  path

from .views import *

urlpatterns = [

    ###### USER ######

    path('user-register/', RegisterUser.as_view()),
    path('verify-user-otp/', VerifyOTP.as_view()),
    path('resend-otp/', ResendOTP.as_view()),
    path ('register-admin/', RegisterAdmin.as_view()),

    path ('user-profile/', UserProfileView.as_view()),
    path ('edit-profile/', UserProfileView.as_view()),
    path ('delete-profile/', UserProfileView.as_view()),

    ###### LOGIN ######

    path('login-user/', LoginAPIView.as_view()),
    
    ###### ADMIN ######

    path ('user-list/', UserListGeneric.as_view()),
    path('verify-admin/', VerifyAdminOTP.as_view()),
    path ('admin-delete-user/', DeleteUserView.as_view()),

    ###### CHANGE PASSWORD ######

    path ('change-password/', UserChangePasswordView.as_view()),
    path('reset-password-email/', SendResetPasswordEmail.as_view()),
    path('reset-password/<uid>/<token>/', PasswordResetView.as_view()),

    # ####### ADD COMMISSION ######

    # path('add-commission/<id>/', CommisionAPI.as_view()),


]