from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    display_name = models.CharField(max_length=150, blank = True, null=True)
    username = models.CharField(max_length=150, unique=True, blank = False, null = False, help_text="Any characters allowed in username.")
    email = models.EmailField(max_length=150, blank=False, null=False)
    avatar = models.ImageField(upload_to="user/profile_pictures/", blank=True, null=True)
    is_online = models.BooleanField(default=False)
    last_online = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('username', 'email'), name = "unique_username_email")
        ]

    def __str__(self):
        return f"{self.username} - {self.email}"
