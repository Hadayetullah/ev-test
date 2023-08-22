from django.db import models
from app_auth.models import User

# Create your models here.


class Dashboard(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User")
    array_value = models.TextField(verbose_name="Array Value", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
