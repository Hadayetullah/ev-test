
from django.urls import path
from . import views

app_name = 'app_auth'

urlpatterns = [
    path('user/registration/',
         views.UserRegistrationView.as_view(), name='registration'),
    path('authenticate/<uid>/<user_token>/',
         views.UserRegistrationVarificationView.as_view(), name='authenticate'),
    path('user/login/', views.UserLoginView.as_view(), name='login'),
    # path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
]
