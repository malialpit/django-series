from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User, Contact


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    filter_horizontal = ()
    list_filter = ('last_login', 'is_active')
    fieldsets = ()
    list_display = ['email', 'phone_number', 'is_active']
    search_fields = ('email', )
    ordering = ('email', )
    readonly_fields = ['email', 'phone_number']

admin.site.register(Contact)