from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile, AttendanceSession

class StaffLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['student_id']

class AttendanceSessionForm(forms.ModelForm):
    class Meta:
        model = AttendanceSession
        fields = ['title', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }