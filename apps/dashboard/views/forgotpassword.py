import math
import random
from django.views import View
# from django.contrib.auth.models import User,auth
from ... accounts.models import User
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.shortcuts import render
global OTP,recipient_list

class Send_Verification(View):
    def post(self,request):
        try:
            if request.method == "POST":
                email = request.POST.get("email")
                user_obj=User.objects.filter(email=email).values()
                for u in user_obj:
                    verified_email=u['email']
                otp = generate_otp(settings.TOTP_DIGITS)

                send_forgot_password_mail(verified_email,otp)

                return render(request,"dashboard/demo.html")
        except:
            return render(request, "dashboard/login.html") #no admin user is present with this id, alert has to be raised

class Change_Password(View):
    global recipient_list
    def post(self,request):
        try:
            if request.method == 'POST':
                pass1=request.POST.get("pass1")
                pass2=request.POST.get("pass2")
                if pass1 == pass2:
                    u = User.objects.get(email=recipient_list[0])
                    u.set_password(pass1)
                    u.save()

                    return render(request,"dashboard/login.html")

                return render(request, "dashboard/change-password.html")
        except:
            # raise ValidationError("No User Present")
            return render(request, "dashboard/login.html")#user not present alert has to be raised



class Check_OTP(View):
    global OTP
    def post(self,request):
        if request.method == 'POST':
            otp=[request.POST.get("1"),
                 request.POST.get("2"),
                 request.POST.get("3"),
                 request.POST.get("4"),
                 request.POST.get("5"),
                 request.POST.get("6"),
                 ]
            otp=int("".join(map(str,otp)))
            if str(otp)==OTP:
                return render(request,"dashboard/change-password.html")
            return render(request, "dashboard/demo.html")


def generate_otp(OTP_DIGIT_SIZE=6):
    global OTP
    digits = "0123456789"
    OTP = ""
    for i in range(OTP_DIGIT_SIZE):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def send_forgot_password_mail(email,otp):

    global recipient_list
    subject = 'Your forgot password otp is '+str(otp)
    message = f'Hi,enter the otp: '+str(otp)+' to reset your password'
    # email_from = settings.EMAIL_HOST_USER
    recipient_list=[email]
    # send_mail(subject,message,email_from,recipient_list)
    Email=EmailMessage(subject,message,to=recipient_list)
    Email.send()

    return True