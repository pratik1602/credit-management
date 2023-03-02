from usercredit.models import *
from rest_framework import generics
from rest_framework.response import Response
from transaction.api.serializers import *
from usercredit.emails import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth import authenticate
from usercredit.decode import get_object
from django_filters.rest_framework import DjangoFilterBackend
from usercredit.utils import *
from datetime import datetime
from django.contrib.auth.hashers import check_password


###### ADD PAYMENT RECORD ######

class RecordList(generics.ListAPIView):
    permission_classes = [IsAuthenticated&IsAdminUser]
    queryset = Transaction.objects.all()
    serializer_class = RecordSerializer
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['transaction_id',]

##### RECORD CRUD ######

class PaymentRecord(APIView):
    permission_classes = [IsAuthenticated&IsAdminUser]

    def post(self, request):
        admin = get_object(request)
        request.data["user_id"] = admin
        get_admin = User.objects.get(id = admin.id)
        if get_admin:
            data = request.data
            try:
                get_card_id = data["card_object_id"]
                get_card = Card.objects.get(card_id = get_card_id)
            except:
                return Response({"Status":False, "Message":"Card not found !!!"})
            serializer = RecordSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                get_record = Transaction.objects.get(transaction_id = serializer.data["transaction_id"])
                Total_profit_amount =  get_record.amount_paid * get_record.commission/100 
                get_record.profit_amount = "%.2f" % float(Total_profit_amount)
                get_record.card = get_card
                get_record.admin = get_admin
                get_record.save()
                return Response({"Status":True, "Message":"Record Added Successfully !!!"})
            else:
                return Response({"Status":False, "Data":serializer.errors})
        else:
            return Response({"Status":False, "Message":"Admin not found !!!"})
        
    
        
