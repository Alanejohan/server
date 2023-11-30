from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager
from category.models import Category



class User(AbstractBaseUser, PermissionsMixin):
    # base models
    email = models.EmailField(unique=True, null=True, db_index=True)
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)

    # fields for management
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    # 
    preferences = models.ManyToManyField(Category, blank=True)


    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        ordering = ("email",)

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"
