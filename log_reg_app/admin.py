from django.contrib import admin
from django.db import models
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)