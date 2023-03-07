from django.contrib import admin
from django.urls import path

from cards.api.views import *

urlpatterns = [
   
    path ('cards-list', GetCardList.as_view(), name="GetCardList"),

    path ('card-view', UserCardAPIView.as_view(), name="UserCardAPIView"),
    path ('add-card', UserCardAPIView.as_view(), name="UserCardAPIView"),
    path ('edit-card', UserCardAPIView.as_view(), name="UserCardAPIView"),
    path ('delete-card', UserCardAPIView.as_view(), name="UserCardAPIView"),

    path ('card-payment/<int:card_id>/', PaymentAPI.as_view()),

    path('add-commission/<int:card_id>/', AddcommissionAPIView.as_view()),

]