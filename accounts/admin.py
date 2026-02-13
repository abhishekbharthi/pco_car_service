from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User

from django.contrib import admin

admin.site.site_header = "Car Service Administration"
admin.site.site_title = "Car Service Admin"
admin.site.index_title = "Welcome to Car Service Dashboard"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)


admin.site.unregister(User)
admin.site.register(User)