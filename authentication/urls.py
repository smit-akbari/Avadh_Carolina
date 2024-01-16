from django.urls import path
from .views import *

urlpatterns = [
    path('', login_view, name='login_view'),
    path('dashboard/', index_view, name='index_view'),
    path('logout/', logout, name='logout'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('otp_verify/', otp_verify, name='otp_verify'),
]