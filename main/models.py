from django.db import models
from authentication.models import baseModel, membersModel
from main.utils.constant import PERMISSIONS
from datetime import datetime
from authentication import helpers

# Create your models here.
#basemodel

class baseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

#service model 
class services(baseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

# clubhousebookingmodel

class clubHouseBooking(baseModel):
    member_id = models.ForeignKey(membersModel, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255, null=False, blank= False)
    from_date = models.DateField(max_length=30, null=False, blank=False)
    to_date = models.DateField(max_length=30, null=False, blank=False) 
    content = models.TextField()
    total_days = models.IntegerField(blank=True)
    status = models.CharField(default='Pending', max_length=50, choices=PERMISSIONS)
    description = models.TextField(max_length=255, null=False, blank= False)

    def __str__(self):
        return f"{self.event_name}"
    
    def save(self, *args, **kwargs):
        fdate = str(self.from_date)
        tdate = str(self.to_date)

        def string_to_date(date_string):
            try:
                date_object = datetime.strptime(date_string, '%Y-%m-%d').date()
                return date_object
            except ValueError:
                # Handle invalid date strings here
                return None
            
        def date_difference_in_days(self):
            if fdate and tdate:
                difference = string_to_date(tdate) - string_to_date(fdate)
                return difference.days
            else:
                return None
        self.total_days = date_difference_in_days(self)
        super(clubHouseBooking, self).save(*args, **kwargs)



#emergencyContactsModel

class emergencyContactsModel(baseModel):
    DIR_NAME = 'card_img'
    icon = models.FileField(upload_to=helpers.custom_file_name, default='default-profile.png')
    name= models.CharField(max_length=255, null=False, blank= False)
    number = models.CharField(max_length=20, null=False, blank= False, unique= True)

    def __str__(self):
     return f"{self.name}"
    
#eventsModel

class eventsModel(baseModel):
    DIR_NAME = 'event_img'
    img = models.ImageField(upload_to=helpers.custom_file_name, default='default-profile.png')
    event_name = models.CharField(max_length=255, null=False, blank= False)
    event_description = models.TextField(max_length=255, null=False, blank= False)

    def __str__(self):
     return f"{self.event_name}"
    

class galleryModel(baseModel):
    DIR_NAME = 'gallery_img'
    gallery_img = models.ImageField(upload_to=helpers.custom_file_name, default='default-profile.png')

    def __str__(self):
        return f"{self.gallery_img}"