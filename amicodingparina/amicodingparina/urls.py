
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('app_auth.urls', namespace='app_auth')),
    path('api/dashboard/', include('app_dashboard.urls', namespace='app_dashboard')),
    path('api/data/', include('app_data.urls', namespace='app_data')),
]
