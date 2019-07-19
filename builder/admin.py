from django.contrib import admin

# Register your models here.
from .models import *

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'user', 'is_cached', 'builder_auth', 'human_auth', 'analatics_auth', 'is_live', 'is_active', 'retrain_date', 'human_takeover', 'date_created', 'billing_amount', 'user_limit')
    list_display_links = ('id', 'project_name', 'user', 'billing_amount')
    search_fields = ('user', 'project_name')
    list_per_page = 50

class IpAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ipaddress', 'browser', 'os', 'platform', 'is_bot', 'geo_location')
    list_display_links = ('id', 'user', 'ipaddress')
    search_fields = ('user', 'browser', 'os', 'platform')
    list_per_page = 50

class ProjectAuthAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'builder_view', 'human_view', 'analytics_view', 'builder_edit', 'human_chat', 'analytics_download', 'is_creator', 'date_created')
    list_display_links = ('user', 'project')
    search_fields = ('user', 'project', 'is_creator')
    list_per_page = 50

class BillingHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'date', 'url', 'mode', 'project_list')
    list_display_links = ('user', 'id')
    search_fields = ('user', 'amount', 'mode')
    list_per_page = 50

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'api_key', 'is_company', 'coupon')
    list_display_links = ('user', 'id')
    search_fields = ('user', 'coupon', 'is_company')
    list_per_page = 50

admin.site.register(Project, ProjectAdmin)
admin.site.register(Ipaddress, IpAdmin)
admin.site.register(ProjectAuth, ProjectAuthAdmin)
admin.site.register(BillingHistory, BillingHistoryAdmin)
admin.site.register(Profile, ProfileAdmin)