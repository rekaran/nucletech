from django.contrib import admin

# Register your models here.
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'domain', 'date_joined', 'is_active', 'is_verified', 'is_staff')
    list_display_links = ('id', 'email')
    search_fields = ('email', 'domain')
    list_per_page = 50

admin.site.register(User, UserAdmin)