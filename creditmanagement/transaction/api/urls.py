from django.urls import path
from transaction.api.views import *

urlpatterns = [

    path("all-record", RecordList.as_view(), name="RecordList"),

    path("add-record", PaymentRecord.as_view(), name="AddPaymentRecord"),

]