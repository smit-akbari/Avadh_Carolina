from django.urls import path
from .views import *
urlpatterns = [
    path('', dashboard_view, name='dashboard_view'),
    path('services_view/', services_view, name='services_view'),
    path('addEvent/', addEvent, name='addEvent'),
    path('delete_event/<int:booking_id>', delete_event, name='delete_event'),
    path('update_event/<int:booking_id>', update_event, name='update_event'),
    path('gallery_view/', gallery_view, name='gallery_view'),
    path('events_view/', events_view, name='events_view'),
    path('emergency_contact_view/', emergency_contact_view, name='emergency_contact_view'),
    path('news_view/', news_view, name='news_view'),
    path('profile_view/', profile_view, name='profile_view'),
    path('update-profile/<int:member_id>/', update_profile, name='update_profile')

]