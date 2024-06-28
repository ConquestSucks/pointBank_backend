from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, login, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(login=login, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(login, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    isEmailConfirmed = models.BooleanField(default=False)
    lastCode = models.IntegerField(max_length=4, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    tickets = models.ManyToManyField('Ticket', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.login

class Ticket(models.Model):
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    from_location = models.TextField()
    to_location = models.TextField()
