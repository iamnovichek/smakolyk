from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import validate_email, MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db import models

from phonenumber_field.validators import validate_international_phonenumber
from phonenumber_field.modelfields import PhoneNumberField

from PIL import Image

from apps.shared.models import AbstractModel

from .custom_validators import age_validator
from .values import ValidationMessages, ValidationValues


class CustomUserManager(BaseUserManager):
    @staticmethod
    def _validate_email(email: str = None) -> None:
        """
        Validate's email
        :param email: str = None
        :return: None
        """
        if not email:
            raise ValidationError(
                ValidationMessages.email_not_provided_validation_message
            )

    @staticmethod
    def _validate_password(password: str = None) -> None:
        """
        Validate's password
        :param password: str = None
        :return: None
        """
        if not password:
            raise ValidationError(
                ValidationMessages.password_not_provided_validation_message
            )

    def create_user(self, email: str = None, password: str = None) -> "CustomUser":
        """
        Creates a new user
        :param email: str = None
        :param password: str = None
        :return: CustomUser
        """
        self._validate_email(email)
        self._validate_password(password)

        user = self.model(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_active = True
        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str = None, password: str = None) -> "CustomUser":
        """
        Creates a new superuser
        :param email: str = None
        :param password: str = None
        :return: CustomUser
        """
        user = self.create_user(email, password)

        user.is_admin = True
        user.save(update_fields=["is_admin", "is_active"])

        return user


class CustomUser(AbstractModel, AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, validators=[validate_email])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = "email"

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


class UserProfile(AbstractModel):
    user = models.OneToOneField(
        CustomUser, related_name="userprofile", on_delete=models.CASCADE
    )
    username = models.CharField(
        max_length=ValidationValues.username_max_length,
        unique=True,
        validators=[
            MinLengthValidator(
                limit_value=ValidationValues.username_min_length,
                message=ValidationMessages.username_validation_message,
            )
        ],
    )
    slug = models.SlugField(unique=True)
    first_name = models.CharField(
        max_length=ValidationValues.first_name_max_length,
        validators=[
            MinLengthValidator(
                limit_value=ValidationValues.first_name_min_length,
                message=ValidationMessages.first_name_validation_message,
            )
        ],
    )
    last_name = models.CharField(
        max_length=ValidationValues.last_name_max_length,
        validators=[
            MinLengthValidator(
                limit_value=ValidationValues.last_name_min_length,
                message=ValidationMessages.last_name_validation_message,
            )
        ],
    )
    birthdate = models.DateField(blank=True, null=True, validators=[age_validator])
    photo = models.ImageField(
        default="default.png", upload_to="profile_pics", blank=True
    )
    phone = PhoneNumberField(
        max_length=ValidationValues.phone_max_length,
        unique=True,
        validators=[validate_international_phonenumber],
    )

    def __str__(self):
        return self.username

    def _save_image(self):
        img = Image.open(self.photo.path)
        img.resize(size=ValidationValues.default_photo_size)
        img.save(self.photo.path)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)
        self._save_image()
