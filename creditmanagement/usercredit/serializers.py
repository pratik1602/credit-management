from rest_framework import serializers
from .models import *
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .emails import *
from django.core.validators import MaxValueValidator, MinValueValidator
percentage_validators=[MinValueValidator(0.1), MaxValueValidator(100)]

######## USER REGISTRATION SERIALIZER ############

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name','password', 'password2','email', 'phone_no', 'aadhar', 'pan', 'cheque', 'refer_code', 'referred_by']

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


######## USER LIST #########

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'


####### USER PROFILE VIEW #########
 
class UserProfileSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'phone_no', 'aadhar', 'pan', 'cheque', 'tc' ]


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
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email =email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("encoded uid", uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("Password  reset token", token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('password reset link', link)

            # Send Email configuration
            body = 'Click following link to reset your password' + link
            data = {
                'subject':"Reset your password",
                'body':body,
                'to_email':user.email
            }
            util.send_reset_password_link_via_email(data)
            return attrs
        else:
            raise ValidationError("You are not a registered user")

class ResetPasswordChangeSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("password and confirm password dosen't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError("Token is not valid or expired")
            user.set_password(password)
            user.save()
            return super().validate(attrs)
        except DjangoUnicodeDecodeError:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError("Token is not valid or expired")



 






    
    

    