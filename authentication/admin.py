from django.contrib import admin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import membersModel, memberProfileModel
from .helpers import textLower
from django.conf import settings

class MembersModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

   # Send an email with an HTML template
        subject = f"Member Login Credentials for {obj.first_name} {obj.last_name} at Avadh Carolina"
        # from_email = "brijeshgondaliya.tops@gmail.com"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [f'{obj.email}']


        context = {
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'member_email': obj.email,
            'member_password': obj.password
        }
        html_message = render_to_string('member-login-credentials.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject, plain_message, from_email, recipient_list,
            html_message=html_message,
        )
# Register your models here.

admin.site.register(membersModel, MembersModelAdmin)
admin.site.register(memberProfileModel)