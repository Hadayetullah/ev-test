
from django.urls import path
from . import views

app_name = 'app_data'

urlpatterns = [
    path('user/userdata/<str:start>/<str:end>/',
         views.UserDataView.as_view(), name='data'),
]
