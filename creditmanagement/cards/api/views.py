from rest_framework import generics
from rest_framework.response import Response
from usercredit.models import *
from cards.api.serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from usercredit.decode import get_object
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime


###### CARD LIST ONLY ADMIN CAN VIEW #########


class GetCardList(APIView):
    permission_classes = [IsAuthenticated&IsAdminUser]

    def get(self, request):
        admin = get_object(request)
        request.data["user_id"] = admin.id
        get_admin = User.objects.get(id = admin.id)
        if get_admin:
            card_id = request.GET.get("card_id")
            if card_id != None or 0:
                try:
                    card_obj = Card.objects.get(card_id=card_id)
                    serializer = AllCardSerializer(card_obj)
                    return Response({"Status": True, "Message": "Card !!!", "data": serializer.data})
                except:
                    return Response({"Status": False, "Message": "No card found !!!"})
            else:
                cards_objs = Card.objects.all()
                
                if cards_objs:
                    serializer = AllCardSerializer(cards_objs, many=True)
                    return Response({"Status": True, "Message": "Cards List !!!", "data": serializer.data})
                else:
                    return Response({"Status": False, "Message": "No Cards found !!!"})  
        else:
            return Response({"Status": False, "Message":"No Admin Found !!!"})



###### CREDIT CARDS LIST, CREATE ,UPDATE AND DELETE #########

class UserCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object(request)
        
        request.data["user_id"] = user.id   
        get_user = User.objects.get(id = user.id)
        if get_user:
            card_id = request.GET.get("card_id")
            if card_id != None or 0:
                try:
                    card_obj = Card.objects.get(card_id=card_id, user_id=user)
                    serializer = CardSerializer(card_obj)
                    return Response({"Status": True, "Message": "Your Card !!!", "data": serializer.data})
                except:
                    return Response({"Status": False, "Message": "No card found !!!"})
            else:
                card_objs = Card.objects.filter(user_id=user)
                if card_objs:
                    serializer = CardSerializer(card_objs, many=True)
                    return Response({"Status": True, "Message": "Your Cards !!!", "data": serializer.data})
                else:
                    return Response({"Status": False, "Message": "No cards found !!!"})
        else:
            return Response({"Status": False, "Message":"No User Found !!!"})


    def post(self, request):
        user = get_object(request)
        request.data["user_id"] = user.id
        user_obj = User.objects.get(id=user.id)
        if user_obj:
            data = request.data
            serializer = CardSerializer(data=data)
            if serializer.is_valid():
                serializer.save( created_by=self.request.user)
                getCard = Card.objects.get(card_id=serializer.data["card_id"])
                due_amount = getCard.due_amount
                commission = getCard.commission
                getCard.commission_total_amount = due_amount * commission/100
                getCard.save()
                return Response({'Status': True, "Message": "Card Added Successfully"})
        return Response({'Status': False, "Message": "something went wrong", "errors": serializer.errors})

        
    def put(self, request):
        now = datetime.now()
        user = get_object(request)
        request.data["user_id"] = user.id
        get_user = User.objects.get(id = user.id)
        if get_user:
            try:
                card_id = request.data["card_id"]
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

                card_obj.modified_at = now

                card_obj.save()
                return Response({"Status":True, "Message":"Card Updated succesfully !!!"})
            except:
                return Response({'Status': False, "Message": "Card doesn't exists"})
        else:
                return Response({'Status': False, "Message": "No user found !!!"})

    def delete(self, request):
        user = get_object(request)
        request.data["user_id"] = user.id
        get_user = User.objects.get(id = user.id)
        if get_user:
            try:
                card_id = request.GET.get("card_id")
                card_obj = Card.objects.get(card_id=card_id, user_id=user.id)
                if card_obj is not None:
                    card_obj.delete()
                    return Response({"Status": True, "Message": "Card deleted successfully !!!"})
            except Exception as e:
                print(e)
                return Response({"Status": False, "Message": "Card doesn't exists"})
        else:
            return Response({'Status': False, "Message": "No user found !!!"})


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



