from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserModelManagers


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserModelManagers()

    # Email orqali login qilish
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def set_fullname(self, value):
        names = value.split()
        self.first_name, self.last_name = names[0], " ".join(names[1:])

    fullname = property(get_fullname, set_fullname)




