from django.contrib import admin
from .models import UserProfile, Attendance

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo')  # Customize fields to display in the admin panel

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'status')  # Customize fields to display
    list_filter = ('date', 'status')  # Add filters for better navigation
