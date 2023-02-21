from rest_framework import generics
from rest_framework.response import Response
from usercredit.models import *
from usercredit.cards.serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from usercredit.decode import get_object
from django_filters.rest_framework import DjangoFilterBackend


###### CARD LIST ONLY ADMIN CAN VIEW #########

class cardListGenerics(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Card.objects.all()
    serializer_class = AllCardSerializer
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['card_id',]


###### CREDIT CARDS LIST, CREATE ,UPDATE AND DELETE #########

class UserCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object(request)
        
        request.data["user_id"] = user.pk
        card_id = request.GET.get("card_id")
        if card_id != None or 0:
            card_obj = Card.objects.filter(card_id=card_id, user_id=user)
        else:
            card_obj = Card.objects.filter(user_id=user)
        serializer = CardSerializer(card_obj, many=True)
        return Response({"Status": True, "Message": "Card List", "data": serializer.data})

    def post(self, request):
        user = get_object(request)
        request.data["user_id"] = user.pk
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response({'Status': True, "Message": "Card Added Successfully"})
        return Response({'Status': False, "Message": "something went wrong", "errors": serializer.errors})

    def put(self, request, card_id):
        try:
            now = datetime.now()
            user = get_object(request)
            request.data["user_id"] = user.id
            card_obj = Card.objects.get(card_id=card_id, user_id=user.id)

            card_obj.card_bank_name = request.data["card_bank_name"]
            card_obj.card_type = request.data["card_type"]
            card_obj.card_number = request.data["card_number"]
            card_obj.card_holder_name =  request.data["card_holder_name"]
            card_obj.card_photo = request.data["card_photo"]
            card_obj.card_exp_date = request.data["card_exp_date"]
            card_obj.card_cvv = request.data["card_cvv"]
            card_obj.due_date =  request.data["due_date"]
            card_obj.due_amount = request.data["due_amount"]

            due_amount = float(card_obj.due_amount)
            commission = float(card_obj.commission)
            commission_amount = due_amount * commission/100
            card_obj.commission_total_amount = "%.2f" % float(commission_amount)
            card_obj.updated_by = request.user
            card_obj.paid_by = request.user

            card_obj.modified_at = now

            card_obj.save()
            return Response({"Status":True, "Data":request.data, "Message":"Data Updated"})

        except:
            return Response({'Status': False, "Message": "Card doesn't exists"})

    def delete(self, request, card_id):
        try:
            user = get_object(request)
            request.data["user_id"] = user.id
            card = Card.objects.get(card_id=card_id, user_id=user.id)
            if card is not None:
                card.delete()
                return Response({"Status": True, "Message": "Card deleted!"})
        except Exception as e:
            print(e)
            return Response({"Status": False, "Message": "Card doesn't exists"})


###### PAYMENT API #######

class PaymentAPI(APIView):
    def post(self, request, card_id):
        try:
            user = get_object(request)
            request.data["user_id"] = user.id
            card_obj = Card.objects.get(card_id=card_id)

            card_obj.card_bank_name = request.data["card_bank_name"]
            card_obj.due_amount = "%.2f" % request.data["due_amount"]

            due_amount = float(card_obj.due_amount)
            commission = float(card_obj.commission)
            commission_amount = due_amount * commission/100
            card_obj.commission_total_amount = "%.2f" % float(commission_amount)
            card_obj.paid_by = request.user
            card_obj.card_status = True

            card_obj.save()
            return Response({"Status":True, "Data":request.data, "Message":"Payment successful"})

        except:
            return Response({'Status': False, "Message": "Card doesn't exists"})


######## ADD COMMISSION BY ADMIN ##########

class AddcommissionAPIView(APIView):
    permission_classes = [IsAdminUser & IsAuthenticated]

    def post(self, request, card_id):

        try:
            card_obj = Card.objects.get(card_id=card_id)
            card_obj.commission = request.data["commission"]
            due_amount = float(card_obj.due_amount)
            commission = float(card_obj.commission)
            commission_amount = due_amount * commission/100
            card_obj.commission_total_amount = "%.2f" % float(commission_amount)
            card_obj.save()
            
            return Response({"Status":True, "Data":request.data, "Message":"Commission Added"})

        except Exception as e:
            print(e)
            return Response({"Message": "Card Doesn't exists"})



