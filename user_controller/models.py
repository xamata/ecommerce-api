"""
Created the users and superuser
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core.exceptions import ObjectDoesNotExist


class UserManager(BaseUserManager):
    """Setting the parameters for all users"""

    def create_user(self, email, password, **extra_fields):
        """verifies the entered data for the user"""
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """creates parameters for superuser and then verifies info"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("first_name", "admin")
        extra_fields.setdefault("last_name", "admin")

        if not extra_fields.get("is_staff", False):
            raise ValueError("Superuser must have is_staff=True")
        if not extra_fields.get("is_superuser", False):
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Creates the parameters for our user"""

    email = models.EmailField(unique=True)
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        super().full_clean()
        super().save(*args, **kwargs)

    class DoesNotExist(ObjectDoesNotExist):
        """taken from django to raise exception"""

        ...


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Ingredients(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(
        Category, related_name="ingredients", on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.name)
