# QR Attendance System

A Django-based attendance management system using QR codes for session-based attendance marking.

## Features
- Admin-only creation of faculty and students
- Session creation with QR code generation
- Students scan QR to mark attendance

## Setup
1. Clone the repo:  
   `git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git`
2. Install requirements:  
   `pip install -r requirements.txt`
3. Run migrations:  
   `python manage.py migrate`
4. Create a superuser:  
   `python manage.py createsuperuser`
5. Start the server:  
   `python manage.py runserver`