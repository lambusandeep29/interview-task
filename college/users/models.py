from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.


class User(AbstractUser):
    USER_TYPE_STUDENT = 1
    USER_TYPE_TEACHER = 2
    USER_TYPE_ADMIN = 3

    CHOICES_USER_TYPE = (
        (USER_TYPE_ADMIN, 'Admin'),
        (USER_TYPE_TEACHER, 'Teacher'),
        (USER_TYPE_STUDENT, 'Student'),
    )

    email = models.EmailField(unique=True)
    user_type = models.IntegerField(choices=CHOICES_USER_TYPE, default=USER_TYPE_STUDENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_type']

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email

    def get_refresh_token_obj(self):
        token = RefreshToken.for_user(self)

        # token['email'] = self.email
        token['role'] = self.user_type
        token['role_display'] = self.get_user_type_display()

        return token

    def get_access_token(self):
        return str(self.get_refresh_token_obj().access_token)

    def get_refresh_token(self):
        return str(self.get_refresh_token_obj())

