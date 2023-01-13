from django.contrib import admin
from django.urls import path

from usercredit.cards.views import *

urlpatterns = [
   
    path ('cards-list/', cardListGenerics.as_view()),

    path ('card-view/', UserCardAPIView.as_view()),
    path ('add-card/', UserCardAPIView.as_view()),
    path ('edit-card/<int:card_id>/', UserCardAPIView.as_view()),
    path ('delete-card/<int:card_id>/', UserCardAPIView.as_view()),

    path ('card-payment/<int:card_id>/', PaymentAPI.as_view()),

    path('add-commission/<int:card_id>/', AddcommissionAPIView.as_view()),

]