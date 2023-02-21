from django.core.mail import send_mail
from django.core.mail import EmailMessage
import random
from django.conf import settings
from .models import User

def send_otp_via_email(email):
    subject = 'Your account verification email '
    otp = random.randint(1000, 9999)
    message = f'Your otp is {otp}'
    email_from =  settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email = email)
    user_obj.otp = otp
    user_obj.save()


def send_reset_password_otp_via_email(email):
    subject = 'Your reset password otp '
    otp = random.randint(1000, 9999)
    message = f'Your otp is {otp}'
    email_from =  settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email = email)
    user_obj.otp = otp
    user_obj.save()     
    # return user_obj
    # print("user_obj", user_obj)

    # if user_obj:
    #     otp
    # user_obj.otp = otp
    # user_obj.save()


# class util:
#     @staticmethod
#     def send_reset_password_otp_via_email(data):
#         email =  EmailMessage(
#             subject=data['subject'],
#             body = data['body'],
#             from_email= settings.EMAIL_HOST_USER,
#             to = [data['to_email']]
#         )
#         email.send()
        

