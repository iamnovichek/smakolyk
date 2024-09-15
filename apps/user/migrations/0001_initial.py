# Generated by Django 4.2.6 on 2024-09-09 10:54

import uuid

import django.core.validators
import django.db.models.deletion
import phonenumber_field.modelfields
import phonenumber_field.validators
from django.conf import settings
from django.db import migrations, models

import apps.user.custom_validators


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "email",
                    models.EmailField(
                        max_length=255,
                        unique=True,
                        validators=[django.core.validators.EmailValidator()],
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "username",
                    models.CharField(
                        max_length=30,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=2,
                                message="Username should contail at least 2 characters!",
                            )
                        ],
                    ),
                ),
                ("slug", models.SlugField(unique=True)),
                (
                    "first_name",
                    models.CharField(
                        max_length=30,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=2,
                                message="First name should contail at least 2 characters!",
                            )
                        ],
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=30,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=2,
                                message="Last name should contail at least 2 characters!",
                            )
                        ],
                    ),
                ),
                (
                    "birthdate",
                    models.DateField(
                        blank=True,
                        null=True,
                        validators=[apps.user.custom_validators.age_validator],
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True, default="default.png", upload_to="profile_pics"
                    ),
                ),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=30,
                        region=None,
                        unique=True,
                        validators=[
                            phonenumber_field.validators.validate_international_phonenumber
                        ],
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="userprofile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
