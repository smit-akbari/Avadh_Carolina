from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import membersModel
from .helpers import create_jwt_token, require_access_token,generate_otp
from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            CHECK_MEMBER = membersModel.objects.get(email=email)
        except membersModel.DoesNotExist:
            messages.error(request, "Member does not exist")
            return render(request, 'login.html')
        else:
            if len(email) != 0 and len(password) != 0 and CHECK_MEMBER:
                if password == CHECK_MEMBER.password:
                    request.session['token'] = create_jwt_token(email)

                    print(request.session.get('token'))
                    messages.success(request, "Now you are logged in")
                    return redirect('dashboard_view')
                else:
                    messages.error(request, "Incorrect Email or Password")
                    return render(request, 'login.html')
    return render(request, 'login.html')

# Create your views here.
def index_view(request):
    querySet = membersModel.objects.all()
    print(querySet)
    for member in querySet:
        print(member.first_name)
    return render(request, 'index.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            CHECK_MEMBER = membersModel.objects.get(email=email)
        except membersModel.DoesNotExist:
            messages.error(request, "Member does not exist")
            return render(request, 'forgot-password.html')
        else:
            otp_ = generate_otp(6)
            subject = 'Access code for [Forgot-Password]'
            message = f"""
            Dear {CHECK_MEMBER.first_name} {CHECK_MEMBER.last_name} \n\n
            You have requested to reset your password. Please use the following One-Time Password (OTP) to verify your identity:

            Your OTP: {otp_}

            This OTP is valid for the next 10 minutes. If you did not request a password reset, please ignore this message.

            Thank you,
            Antilia
            """
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [f'{email}']
            send_mail(subject, message, from_email, recipient_list)
            CHECK_MEMBER.otp = otp_
            CHECK_MEMBER.save()
            context = {
                'email':email
            }
            messages.success(request, "Please check your email. OTP mail has been sent successfully")
            return render(request, 'otp-verification.html', context)
    return render(request, 'forgot-password.html')

def otp_verify(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp_ = request.POST['otp']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        try:
            CHECK_MEMBER = membersModel.objects.get(email=email)
        except membersModel.DoesNotExist:
            messages.error(request, "Member does not exist")
            return render(request, 'forgot-password.html')
        else:
            if CHECK_MEMBER.otp == otp_:
                if new_password == confirm_password:
                    CHECK_MEMBER.password = new_password
                    CHECK_MEMBER.save()
                    messages.success(request, "Your password Changed.")
                    return redirect('login_view')
                else:
                    context = {
                        'email':email
                    }
                    messages.error(request, "new password and confirm password doesn't match")
                    return render(request, 'otp-verification.html', context)
            else:
                context = {
                    'email':email
                }
                messages.error(request, "Invalid OTP")
                return render(request, 'otp-verification.html', context)
    return render(request, 'otp-verification.html')


@require_access_token
def logout(request):
    request.session.clear()
    messages.success(request, "You are logged out")
    return redirect('login_view')