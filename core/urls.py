from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.shortcuts import redirect
def home_redirect(request):
    return redirect('student_login') 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('attendance.urls')),
    path('', home_redirect),
    path('accounts/', include('django.contrib.auth.urls')),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)