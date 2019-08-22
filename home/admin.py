from django.contrib import admin

# Register your models here.
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'domain', 'date_joined', 'is_active', 'mobile_verified', 'is_verified', 'is_staff', 'login_as')
    list_display_links = ('id', 'email')
    search_fields = ('email', 'domain')
    list_per_page = 50
    list_filter = ('mobile_verified', 'is_verified')

    def login_as(self, obj):
        return '<a href="https://www.nucletech.com/%s">Login</a>' % (obj.id)
    
    login_as.allow_tags = True
    login_as.short_description = 'Action'

admin.site.register(User, UserAdmin)