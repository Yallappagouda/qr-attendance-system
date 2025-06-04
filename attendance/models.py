from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=30, unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

class AttendanceSession(models.Model):
    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    session_qr = models.ImageField(upload_to='session_qr/', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time})"

class AttendanceRecord(models.Model):
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    marked_by_staff = models.BooleanField(default=False)  # Manual override

    def __str__(self):
        return f"{self.student} - {self.session.title} [{self.timestamp}]"