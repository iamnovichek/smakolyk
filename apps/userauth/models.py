from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import validate_email, MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db import models

from phonenumber_field.validators import validate_international_phonenumber
from phonenumber_field.modelfields import PhoneNumberField

from PIL.Image import Image

from .custom_validators import age_validator


class CustomUserManager(BaseUserManager):
    def create_user(self,
                    email: str = None,
                    password: str = None) -> object:
        if not email:
            raise ValidationError("Email is required!")

        if "@" not in email or "." not in email:
            raise ValidationError("Invalid email format!")

        if not password:
            raise ValidationError("Password is required!")

        user = self.model(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_active = True
        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,
                         email: str = None,
                         password: str = None) -> object:
        if not email:
            raise ValidationError("Email is required!")

        if "@" not in email or "." not in email:
            raise ValidationError("Invalid email format!")

        if not password:
            raise ValidationError("Password is required!")

        user = self.model(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser):
    email = models.CharField(max_length=255, null=False, unique=True,
                             blank=False, validators=[validate_email])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.email}"

    @staticmethod
    def has_perm(perm, obj=None) -> bool:
        return True

    @staticmethod
    def has_module_perms(app_label) -> bool:
        return True

    @property
    def is_staff(self) -> models.BooleanField:
        return self.is_admin


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='userprofile', on_delete=models.CASCADE)
    username = models.CharField(max_length=30, unique=True, validators=[
        MinLengthValidator(limit_value=2, message="Username should contail at least 2 characters!")
    ])
    slug = models.SlugField(unique=True)
    first_name = models.CharField(max_length=30, validators=[
        MinLengthValidator(limit_value=2, message="First name should contail at least 2 characters!")
    ])
    last_name = models.CharField(max_length=30, validators=[
        MinLengthValidator(limit_value=2, message="Last name should contail at least 2 characters!")
    ])
    birthdate = models.DateField(blank=True, null=True, validators=[age_validator])
    photo = models.ImageField(default="default.png", upload_to='profile_pics', blank=True, null=True)
    phone = PhoneNumberField(max_length=30, unique=True, validators=[validate_international_phonenumber])

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        # img = Image.open(self.photo.path)
        # img.resize(200, 200).save(self.photo.path)
        return super().save(*args, **kwargs)
