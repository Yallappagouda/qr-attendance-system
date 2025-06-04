from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from .models import StudentProfile, AttendanceSession, AttendanceRecord
from .forms import StaffLoginForm, StudentProfileForm, AttendanceSessionForm
from .qr_utils import generate_qr_code
from django.contrib.auth.models import User
from django.db import IntegrityError
from io import BytesIO
import base64
import qrcode
import csv

def landing(request):
    return render(request, "attendance/landing.html")

# STAFF VIEWS

def staff_login_view(request):
    """
    Staff login view.
    """
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('staff_dashboard')
    form = StaffLoginForm(request.POST or None)
    msg = ""
    if request.method == "POST":
        user = authenticate(username=form.data['username'], password=form.data['password'])
        if user and user.is_staff:
            login(request, user)
            return redirect('staff_dashboard')
        else:
            msg = "Invalid credentials or not staff."
    return render(request, 'attendance/staff_login.html', {'form': form, 'msg': msg})

@login_required
@user_passes_test(lambda u: u.is_staff)
def staff_dashboard(request):
    """
    Staff dashboard: List sessions and option to create/download.
    """
    sessions = AttendanceSession.objects.filter(created_by=request.user)
    return render(request, "attendance/staff_dashboard.html", {"sessions": sessions})

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_student(request):
    """
    Staff adds a student.
    """
    msg = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        fullname = request.POST['fullname']
        student_id = request.POST['student_id']
        if User.objects.filter(username=username).exists():
            msg = "Username already exists. Please choose a different username."
        else:
            try:
                user = User.objects.create_user(username=username, password=password, first_name=fullname)
                profile = StudentProfile.objects.create(user=user, student_id=student_id, is_approved=True)
                # Generate QR code for student
                qr_file = generate_qr_code(f"{student_id}")
                profile.qr_code.save(f"{student_id}.png", qr_file)
                profile.save()
                return redirect('staff_dashboard')
            except IntegrityError:
                msg = "A user with this username already exists."
    return render(request, 'attendance/add_student.html', {'msg': msg})

@login_required
@user_passes_test(lambda u: u.is_staff)
def create_attendance_session(request):
    """
    Staff creates an attendance session.
    """
    form = AttendanceSessionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        session = form.save(commit=False)
        session.created_by = request.user
        session.save()
        # Generate QR code with session info (e.g. session id)
        qr_file = generate_qr_code(f"session:{session.id}")
        session.session_qr.save(f"session_{session.id}.png", qr_file)
        session.save()
        return redirect('staff_dashboard')
    return render(request, 'attendance/create_session.html', {'form': form})
@login_required
@user_passes_test(lambda u: u.is_staff)
def export_attendance(request, session_id):
    """
    Export attendance for a session as CSV.
    """
    session = get_object_or_404(AttendanceSession, id=session_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="attendance_{session_id}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Student ID', 'Timestamp'])
    for record in AttendanceRecord.objects.filter(session=session):
        writer.writerow([record.student.user.get_full_name(), record.student.student_id, record.timestamp])
    return response

# STUDENT VIEWS

def student_login(request):
    """
    Student login view.
    """
    msg = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:  # Only allow students
            login(request, user)
            return redirect("student_profile")
        else:
            msg = "Invalid credentials or not student!"
    return render(request, "attendance/student_login.html", {"msg": msg})

@login_required
def student_logout(request):
    logout(request)
    return redirect('student_login')

@login_required
def student_profile(request):
    """
    Student profile page.
    """
    profile = get_object_or_404(StudentProfile, user=request.user)
    return render(request, 'attendance/student_profile.html', {'profile': profile})

@login_required
def download_id_card(request):
    """
    Download student's QR ID card.
    """
    profile = get_object_or_404(StudentProfile, user=request.user)
    with open(profile.qr_code.path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="image/png")
        response['Content-Disposition'] = f'attachment; filename={profile.student_id}_qr.png'
        return response

# ATTENDANCE VIEWS

@login_required
def attendance_scan(request):
    """
    Student scans for latest active session.
    """
    session = AttendanceSession.objects.filter(is_active=True).order_by('-start_time').first()
    qr_img = None
    if session and session.session_qr:
        qr_img = session.session_qr.url
    return render(request, "attendance/attendance_scan.html", {"session": session, "qr_img": qr_img})

@login_required
def mark_attendance(request):
    """
    Mark attendance for student.
    """
    if request.method == "POST":
        session_id = request.POST.get('session_id')
        session = get_object_or_404(AttendanceSession, id=session_id, is_active=True)
        profile = get_object_or_404(StudentProfile, user=request.user)
        if AttendanceRecord.objects.filter(session=session, student=profile).exists():
            return JsonResponse({'status': 'already_marked'})
        AttendanceRecord.objects.create(session=session, student=profile)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid'})