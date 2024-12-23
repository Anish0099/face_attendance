

from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.student_list,name='student_list'),
    path('register/', views.register,name='register'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
     path('attendance_records/', views.attendance_records, name='attendance_records'),
    path('attendance_success/', TemplateView.as_view(template_name='attendance_success.html'), name='attendance_success'),
    path('attendance_failure/', TemplateView.as_view(template_name='attendance_failure.html'), name='attendance_failure'),
    path('mark_attendance_admin/<int:record_id>/', views.mark_attendance_admin, name='mark_attendance_admin'),
    path('export_attendance/', views.export_attendance, name='export_attendance'),

] 
