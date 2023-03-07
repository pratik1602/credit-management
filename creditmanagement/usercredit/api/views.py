from rest_framework import generics
from rest_framework.response import Response
from usercredit.models import *
from usercredit.api.serializers import *
from usercredit.emails import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from usercredit.decode import get_object
from django_filters.rest_framework import DjangoFilterBackend
from usercredit.utils import *
from datetime import datetime
from django.contrib.auth.hashers import check_password

### Create your views here. ###

###### GETTING TOKENS FOR USER ######

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
    
####### USER LIST ######

class GetUserList(APIView):
    permission_classes = [IsAuthenticated&IsAdminUser]

    def get(self, request):
        admin = get_object(request)
        request.data["user_id"] = admin.id
        get_admin = User.objects.get(id = admin.id)
        if get_admin:
            user_id = request.GET.get("id")
            if user_id != None or 0:
                try:
                    user_obj = User.objects.get(under_by = admin, id = user_id)
                    serializer = UserSerializer(user_obj)
                    return Response({"Status": True, "Message": "User !!!", "data": serializer.data})
                except:
                    return Response({"Status": False, "Message": "No User found !!!"})
            else:
                user_objs = User.objects.filter(under_by = admin)
                if user_objs:
                    serializer = UserSerializer(user_objs, many=True)
                    return Response({"Status": True, "Message": "Users List !!!", "data": serializer.data})
                else:
                    return Response({"Status": False, "Message": "No Users found !!!"})  
        else:
            return Response({"Status": False, "Message":"No Admin Found !!!"})


######### REGISTRATION - USER #########

@authentication_classes([])
@permission_classes([])
class RegisterUser(APIView):

    def post(self, request):
        if not request.POST._mutable:
            request.POST._mutable = True
        data = request.data
        try:
            admin = User.objects.get(id= data["id"])
            print("admin", admin)
        except:
            return Response({"Message": "Admin not found !!!"})
        
        user = User.objects.filter(phone_no = data["phone_no"])
        if not user.exists():  
            if data["refer_code"] != "":          
                try:
                    referred_user = User.objects.get(refer_code = data["refer_code"])   
                    data["referred_by"] = referred_user.id
                    serializer = UserRegistrationSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save(under_by = admin)
                        # get_user = User.objects.get(id = serializer.data["id"])
 
                        send_otp_via_email(serializer.data['email'])
                        
                        return Response({"Status": True, "Message": 'Registration Successful. Please check your email for verification', "Data": serializer.data})
                    else:
                        return Response({"Data":serializer.errors,"Message":"Something went wrong", "Status":False})
                except:
                    return Response({"Message":"Invalid referral code or doesn't match !!!"})
            else:
                serializer = UserRegistrationSerializer(data=data)
                if serializer.is_valid():
                    serializer.save(under_by = admin)
                    send_otp_via_email(serializer.data['email'])
                    # get_user = User.objects.get(id = serializer.data["id"])
                    
                    return Response({"Status": True, "Message": 'Registration Successful. Please check your email for verification', "Data": serializer.data})
                else:
                    return Response({"Data":serializer.errors,"Message":"Something went wrong", "Status":False})
        else:
            return Response({"Message":"User already exists !!!"})
    
        
###### ADMIN REGISTER API ########

@authentication_classes([])
@permission_classes([])
class RegisterAdmin(APIView):
    def post (self, request):
        data = request.data
        serializer = AdminRegisterSerializer(data=data)
        mobile = data['phone_no']
        if serializer.is_valid():
            user = User.objects.filter(phone_no=mobile)
            if user.exists():
                return Response({"Status":False, "Message":"Mobile number already exists !!!"}) 
            serializer.save()
            send_otp_via_email(serializer.data['email'])
            return Response ({'Status': True , 'Message': 'Registration Successful. Please check your email for verification', "Data":serializer.data})
        else:
            return Response({"Data":serializer.errors}) 


######## USER PROFILE VIEW, UPDATE AND DELETE ############

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,  request):
        user = get_object(request)
        request.data["user_id"] = user.id
        if user:
            serializer = UserProfileSerializer(user)
            return Response({"Status": True, "Data": serializer.data})
        else:
            return Response({"Status": False, "Message":"User not found !!!"})

    def put(self, request):
        if not request.POST._mutable:
            request.POST._mutable = True
        data = request.data
        user= get_object(request)
        request.data["user_id"] = user.id
        serializer = UserProfileSerializer(user, data=data)

        if not serializer.is_valid():
            return Response({'Status': False, 'Data': serializer.errors, 'Message': 'something went wrong'})
        now = datetime.now()
        user.user_modified_at = now
        serializer.save()

        return Response({'Status': True, "Data": serializer.data,  'Message': 'Your data is updated'})

    def delete(self, request):
        try:
            user = get_object(request)
            request.data["user_id"] = user.id
            user_obj = User.objects.get(id=user.id)
            if user_obj is not None:
                user.delete()
                return Response({"Status":True, "Message": "Account deleted"})
        except Exception as e:
            print(e) 
            return Response({"Status":False, "Message": "Account not found"})             
 

###### ADMIN CRUD ######

class AdminProfileView(APIView):
    permission_classes = [IsAuthenticated&IsAdminUser]

    def get(self,  request):
        user = get_object(request)
        request.data["user_id"] = user.id
        serializer = AdminProfileSerializer(user)
        return Response({"Status": True, "Data": serializer.data})

    def put(self, request):
        if not request.POST._mutable:
            request.POST._mutable = True
        user= get_object(request)
        request.data["user_id"] = user.id
        serializer = AdminProfileSerializer(user, data=request.data)

        if not serializer.is_valid():
            return Response({'Status': False, 'Data': serializer.errors, 'Message': 'something went wrong'})
        now = datetime.now()
        user.user_modified_at = now
        serializer.save()

        return Response({'Status': True, "Data": serializer.data,  'Message': 'Your data is updated'})

    def delete(self, request):
        try:
            user = get_object(request)
            request.data["user_id"] = user.id
            user_obj = User.objects.get(id=user.id)
            print("user", user)
            if user_obj is not None:
                user.delete()
                return Response({"Status":True, "Message": "Account deleted"})
        except Exception as e:
            print(e) 
            return Response({"Status":False, "Message": "Account not found"})


######## DELETE USER - ADMIN ONLY ############ (PASS PARAMETER)

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated&IsAdminUser]

    def delete(self, request, format=None):
        try:
            id = request.GET.get('id')    
            user = User.objects.get(id=id)
            user.delete()
            return Response({'Status':True,'Message':"User Deleted Successfully"})
        except Exception as e:
            print(e)
            return Response({'Status':False, 'Message':"User not found !!!"})


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
                return Response({'Status':True, 'Data': {"token": token}, 'Message':"Login successful"})
            elif user is None:
                return Response({'Status':False,'Message':"Invalid credentials"}) 
            else:
                send_otp_via_email(serializer.data['email']) 
                return Response({'Status':False,'Message':"You are not a verified user!!! Please check your email and get verified"})
             
        return Response({'Status':False, 'Data':serializer.errors,'Message':"something went wrong"})


###### VERIFY USER WITH OTP #########

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
                    return Response({'Status': False, 'Data': "Invalid Email", 'Message': "Something went wrong !!!"})

                if user[0].otp != otp:
                    return Response({'Status': False, 'Data': "Invalid OTP or Doesn't Match", 'Message': "Something went wrong !!!"})

                user = user.first()
                user.is_verified = True
                user.save()

                return Response({'Status': True,  'Message': "Account Verified Successfully !!!"})
            return Response({'Status': True, 'Data': serializer.errors, 'Message': "Something went wrong"})
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
                    return Response({'Status': False, 'Data': "Invalid Email", 'Message': "User not found !!!"})

                if user[0].otp != otp:
                    return Response({'Status': False, 'Data': "Invalid OTP", 'Message': "Something went wrong"})

                user = user.first()
                user.is_verified = True
                user.is_admin = True
                user.is_staff = True
                user.save()
                return Response({'Status': True,  'Message': "Account Verified Successfully !!!"})
            return Response({'Status': False, 'Data': serializer.errors, 'Message': "Something went wrong"})
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
                    return Response({'Status': False, 'Data': "Invalid Email", 'Message': "Something went wrong"})
                send_otp_via_email(serializer.data['email'])  
                return Response({'Status': True,  'Message': "Please check your email again !!!"})
            return Response({'Status': False, 'Data': serializer.errors, 'Message': "Something went wrong"})

        except Exception as e:
            print(e)


######## USER CHANGE PASSWORD VIEW ############

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = get_object(request)
        data = request.data
        user_id = user.id
        user_obj = User.objects.get(id=user_id)
        if user_obj:    
            user_password = user_obj.password
            old_password= data["old_password"]
            checkPass = check_password(old_password, user_password)

            if checkPass:
                serializer = USerChangePasswordSerializer(
                    data=request.data, context={'user': request.user})
                if serializer.is_valid():
                    return Response({'Status': True,  "Message": "Password changed successfully !!!"})
                else:
                    return Response({"Data":serializer.errors})
            else:
                return Response({"Message": "Old password doesn't match !!!"})
        else:
            return Response({"Message": "user not found"})


######### SEND RESET PASSWORD EMAIL #########

@authentication_classes([])
@permission_classes([])
class SendResetPasswordEmail(APIView):

    def post(self, request):
        data = request.data
        try:
            serializer = ResetPasswordEmailSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response({'Status': False, 'Data': "Invalid Email", 'Message': "Something went wrong"})
                send_reset_password_otp_via_email(serializer.data['email']) 
                return Response({'Status': True,  'Message': "Please check your email !!!"})
            return Response({'Status': False, 'Data': serializer.errors, 'Message': "Something went wrong"})

        except Exception as e:
            print(e)

@authentication_classes([])
@permission_classes([])
class VerifyResetPasswordOTPView(APIView):
    
    def post(self, request):
        data = request.data
        try:
            serializer = VerifyPasswoprdOTPSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response({'Status': False, 'Data': "Invalid Email", 'Message': "User not found !!!"})

                if user[0].otp != otp:
                    return Response({'Status': False, 'Data': "Invalid OTP", 'Message': "Something went wrong"})

                return Response({'Status': True,  'Message': "OTP verified successfully !!!"})
            return Response({'Status': False, 'Data': serializer.errors, 'Message': "Something went wrong"})
        except Exception as e:
                print(e)


###### RESET PASSWORD ######

@authentication_classes([])
@permission_classes([])
class PasswordResetView(APIView):
    def post(self, request,  format=None):
        data = request.data
        user_email = data["email"]
        password = data["password"]
        cpassword = data["password2"]
        try:
            user_obj = User.objects.get(email = user_email)

            if password != cpassword:
                return Response({"Status":False, "Message":"password and confirm password doesn't match"})
            user_obj.set_password(password)
            user_obj.save()
            return Response({"Status":True, "Message": "Password Reset Successfully !!!"})
        except Exception as e:
            print(e)
            return Response({'Status': False,  "Message": "User not found !!!"})

























