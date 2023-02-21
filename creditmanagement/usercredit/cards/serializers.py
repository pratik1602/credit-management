from rest_framework import serializers
from usercredit.models import *
from usercredit.serializers import *

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "profile_pic"]


class CardSerializer(serializers.ModelSerializer):
    # user_id = serializers.SerializerMethodField()
    # # created_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    # # updated_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    # # commission_total_amount = models.FloatField( blank=True)
    # def get_user_id(obj):
    #     user = User.objects.filter(id=obj.user_id)
    #     user_id = UserSerializer(user)
    #     return user_id.data


    commission = serializers.FloatField(read_only=True)
    class Meta:
        model = Card
        fields = ['card_id',"user_id",'card_bank_name','card_type', 'card_number','card_holder_name' ,'card_photo','card_exp_date' ,'card_cvv','due_date','due_amount','commission', 'card_status','updated_by', 'created_by', 'paid_by', "commission_total_amount"]


class PaymentSerializer(serializers.ModelSerializer):
    # paid_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    class Meta:
        model = Card
        fields = [ 'card_bank_name', 'due_amount', 'paid_by']

class addCommissionSerializer(serializers.ModelSerializer):
    commission = serializers.FloatField(read_only=True)
    class Meta:
        model = Card
        fields = ['commission']


class AllCardSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    class Meta:
        model = Card
        fields = '__all__'


    


