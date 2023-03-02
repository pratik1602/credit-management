from rest_framework import serializers
from usercredit.models import *
from usercredit.emails import *
from django.core.validators import MaxValueValidator, MinValueValidator
percentage_validators=[MinValueValidator(0.1), MaxValueValidator(100)]

######## USER REGISTRATION SERIALIZER ############

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name','password', 'password2','email', 'phone_no', 'aadhar', 'pan', 'cheque', 'refer_code', 'referred_by', 'under_by', 'tc', 'role', 'created_by']

        extra_kwargs = {
            'password' : {'write_only' : True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("password and confirm password dosen't match")

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data["refer_code"] = generate_ref_code()
        validated_data["role"] = 2
        
        return User.objects.create_user(**validated_data)

######### LOGIN SERIALIZER ##########

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

####### RESEND OTP #########

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
####### VERIFY ACCOUNT #########

class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp  = serializers.CharField()

####### VERIFY RESET PASSWORD OTP #########

class VerifyPasswoprdOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp  = serializers.CharField()

######## USER LIST #########

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['password', 'groups', 'user_permissions']

####### USER PROFILE SERIALIZER #########
 
class UserProfileSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'phone_no', 'aadhar', 'pan', 'cheque', 'tc' ]

##### ADMIN PROFILE SERIALIZER #####

class AdminProfileSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'phone_no']


######## USER CHANGE PASSWORD #########

class USerChangePasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password and confirm password dosen't match")
        user.set_password(password)
        user.save()
        return super().validate(attrs)

###### ADMIN REGISTER ########

class AdminRegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','password','password2','email', 'phone_no']

        extra_kwargs = {
            'password' : {'write_only' : True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("password and confirm password dosen't match")

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data["role"] = 1
        return User.objects.create_admin(**validated_data)

        
###### RESET PASSWORD EMAIL ########

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()





 






    
    

    