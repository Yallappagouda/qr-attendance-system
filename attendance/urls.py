from django.urls import path
from . import views

urlpatterns = [
    # Staff URLs
    path('staff/login/', views.staff_login_view, name='staff_login'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/add_student/', views.add_student, name='add_student'),
    path('staff/create_session/', views.create_attendance_session, name='create_session'),
    path('staff/export/<int:session_id>/', views.export_attendance, name='staff_export_attendance'),

    # Student URLs
    path('student/profile/', views.student_profile, name='student_profile'),
    path('student/download_id/', views.download_id_card, name='download_id_card'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/logout/', views.student_logout, name='student_logout'),

    # Attendance URLs
    path('attendance/scan/', views.attendance_scan, name='attendance_scan'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/export/<int:session_id>/', views.export_attendance, name='attendance_export_attendance'),

    # Root
    path('', views.landing, name='landing'),
]