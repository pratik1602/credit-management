from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from .emails import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from usercredit.decode import get_object
from django_filters.rest_framework import DjangoFilterBackend
from .utils import *
from datetime import datetime
from django.utils import timezone
# from django.utils.timezone import 

### Create your views here. ###

###### GETTING TOKENS FOR USER ######

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

####### USER VIEWS ######

class UserListGeneric(generics.ListAPIView):
    permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id',]


######### REGISTRATION #########

@authentication_classes([])
@permission_classes([])
class RegisterUser(APIView):

    def post(self, request):
        if not request.POST._mutable:
            request.POST._mutable = True
        try:
            user = User.objects.get(refer_code=request.data['refer_code'])
            request.data['referred_by'] = user.id
        except:
            return Response({"message":"Invalid Referral Code"})
        try:
            request.data['refer_code'] = generate_ref_code()

            serializer = UserRegistrationSerializer(data=request.data)
    
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                
                return Response({'status': True, 'message': 'Registration Successful. Please check your email for verification'})
        except:
            return Response({"error":serializer.errors,"message":"Something went wrong"})
       
        
###### ADMIN REGISTER API ########

@authentication_classes([])
@permission_classes([])
class RegisterAdmin(APIView):
    def post (self, request):
        serializer = AdminRegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response ({'status': False, 'errors' : serializer.errors, 'message': 'something went wrong'})
        serializer.save()
        send_otp_via_email(serializer.data['email'])
        return Response ({'status': True , 'message': 'Registration Successful. Please check your email for verification'})


######## USER PROFILE VIEW, UPDATE AND DELETE ############

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,  request):
        user = get_object(request)
        request.data["user_id"] = user.id
        serializer = UserProfileSerializer(user)
        return Response({"status": True, "data": serializer.data})

    def put(self, request):
        if not request.POST._mutable:
            request.POST._mutable = True
        user= get_object(request)
        request.data["user_id"] = user.id
        serializer = UserProfileSerializer(user, data=request.data)

        if not serializer.is_valid():
            return Response({'status': False, 'errors': serializer.errors, 'message': 'something went wrong'})
        now = datetime.now()
        user.user_modified_at = now
        serializer.save()

        return Response({'status': True, "data": serializer.data,  'message': 'Your data is updated'})

    def delete(self, request):
        try:
            user = get_object(request)
            request.data["user_id"] = user.id
            user_obj = User.objects.get(id=user.id)
            print("user", user)
            if user_obj is not None:
                user.delete()
                return Response({"status":True, "message": "Account deleted"})
        except Exception as e:
            print(e) 
            return Response({"status":False, "message": "Account not found"})             
 

######## DELETE USER - ADMIN ONLY ############ (PASS PARAMETER)

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated&IsAdminUser]

    def delete(self, request, format=None):
        try:
            id = request.GET.get('id')    
            user = User.objects.get(id=id)
            user.delete()
            return Response({'status':True,'message':"User Deleted Successfully"})
        except Exception as e:
            print(e)
            return Response({'status':False, 'message':"Invalid User Id"})


######## LOGIN USER #############

@authentication_classes([])
@permission_classes([])
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password') 
            user = authenticate(email=email, password=password) 
            if user is not None and user.is_verified:
                token=  get_tokens_for_user(user)
                return Response({'status':True, 'token': token, 'message':"Login successful"})
            elif user is None:
                return Response({'status':False,'message':"Invalid credentials"}) 
            else:
                send_otp_via_email(serializer.data['email'])
                return Response({'status':False,'message':"You are not a verified user!!! Please check your email and get verified"})
             
        return Response({'status':False, 'errors':serializer.errors,'message':"something went wrong"})


###### VERIFY USER #########

@authentication_classes([])
@permission_classes([])
class VerifyOTP(APIView):
    def post(self, request):
        try:
            serializer = VerifyAccountSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response({'status': False, 'data': "Invalid Email", 'message': "Something went wrong"})

                if user[0].otp != otp:
                    return Response({'status': False, 'data': "Invalid OTP", 'message': "Something went wrong"})

                user = user.first()
                user.is_verified = True
                user.save()

                return Response({'status': True,  'message': "Account Verified"})
            return Response({'status': True, 'errors': serializer.errors, 'message': "Something went wrong"})
        except Exception as e:
            print(e)


######### VERIFY ADMIN ############

@authentication_classes([])
@permission_classes([])
class VerifyAdminOTP(APIView):
    def post(self, request):
        try:
            serializer = VerifyAccountSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response({'status': False, 'data': "Invalid Email", 'message': "Something went wrong"})

                if user[0].otp != otp:
                    return Response({'status': False, 'data': "Invalid OTP", 'message': "Something went wrong"})

                user = user.first()
                user.is_verified = True
                user.is_admin = True
                user.is_staff = True
                user.save()
                return Response({'status': True,  'message': "Account Verified"})
            return Response({'status': False, 'errors': serializer.errors, 'message': "Something went wrong"})
        except Exception as e:
            print(e)


###### RESEND OTP #########

@authentication_classes([])
@permission_classes([])
class ResendOTP(APIView):
    def post(self, request):
        try:
            serializer = ResendOTPSerializer(data=request.data)

            if serializer.is_valid():
                email = serializer.data['email']
                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response({'status': False, 'data': "Invalid Email", 'message': "Something went wrong"})
                send_otp_via_email(serializer.data['email'])
                return Response({'status': True,  'message': "Please check your email"})
            return Response({'status': False, 'data': serializer.errors, 'message': "Something went wrong"})

        except Exception as e:
            print(e)


######## USER CHANGE PASSWORD VIEW ############

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = USerChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            return Response({'status': True,  "message": "Password changed successfully"})

        return Response({'status': False, 'errors': serializer.errors, 'message': 'something went wrong'})


######### SEND RESET PASSWORD EMAIL #########

@authentication_classes([])
@permission_classes([])
class SendResetPasswordEmail(APIView):
    
    def post(self, request, format=None):
        serializer = ResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'status': True,  "message": "Reset password link has been sent on your email"})
        return Response({'status': False, 'errors': serializer.errors, 'message': 'something went wrong'})


###### RESET PASSWORD ######

@authentication_classes([])
@permission_classes([])
class PasswordResetView(APIView):
    def post(self, request, uid, token,  format=None):
        serializer = ResetPasswordChangeSerializer(data=request.data, context={'uid':uid, 'token':token})
        if serializer.is_valid():
            return Response({'status': True,  "message": "Password reset successfully"})

        return Response({'status': False, 'errors': serializer.errors, 'message': 'something went wrong'})
























