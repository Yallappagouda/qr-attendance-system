from django.contrib import admin
from .models import StudentProfile, AttendanceSession, AttendanceRecord

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'is_approved')

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'is_active')

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'timestamp', 'marked_by_staff')