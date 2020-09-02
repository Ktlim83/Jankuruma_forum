from django.contrib import admin
from .models import ContactUser
from .models import Chassis


# Register your models here.
class ContactUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(ContactUser, ContactUserAdmin)

class ChassisAdmin(admin.ModelAdmin):
    pass

admin.site.register(Chassis, ChassisAdmin)



