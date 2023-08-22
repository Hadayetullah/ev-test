
from django.urls import path
from . import views

app_name = 'app_dashboard'

urlpatterns = [
    path('user/input/', views.UserInputView.as_view(), name='input'),
    # path('input/', views.UserDashboardView.as_view(), name='dashboard'),
]
