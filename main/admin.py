from django.contrib import admin
from .models import clubHouseBooking,services,emergencyContactsModel,eventsModel, galleryModel
# Register your models here.

admin.site.register(clubHouseBooking)
admin.site.register(services)
admin.site.register(emergencyContactsModel)
admin.site.register(eventsModel)
admin.site.register(galleryModel)
