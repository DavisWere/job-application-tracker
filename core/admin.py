from core.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Other Fields",
            {
                "fields": (

                    "email",
                    'first_name',
                    'second_name',
                    'user_type',
                    'phone_number',
                    'resume',




                )
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Job)
admin.site.register(Payment)
admin.site.register(Notification)
admin.site.register(Application)
