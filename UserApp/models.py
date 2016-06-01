from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, is_staff, is_superuser, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

class CustomizedUser(AbstractBaseUser):
    objects = CustomUserManager()
    name = models.CharField(max_length=60)
    balance = models.PositiveIntegerField(default=0)
    debit_card = models.PositiveIntegerField( null=True)
    email = models.EmailField(unique=True, verbose_name='email address', max_length=255)
    is_staff = models.BooleanField(('staff status'), default=False,
                                   help_text=('Designates whether the user can log into this admin '
                                              'site.'))
    is_active = models.BooleanField(('active'), default=True,
                                    help_text=('Designates whether this user should be treated as '
                                               'active. Unselect this instead of deleting accounts.'))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []




