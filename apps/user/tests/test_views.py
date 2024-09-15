from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.http import HttpResponseBase
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.text import slugify

from apps.user.models import CustomUser, UserProfile
from apps.user.values import ValidationMessages, ValidationValues

from .values import TestValues, TestValuesMethods


class CustomLoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("login")
        self.user = get_user_model().objects.create_user(
            email=TestValues.email, password=TestValues.password
        )

    def tearDown(self):
        UserProfile.objects.all().delete()
        CustomUser.objects.all().delete()

    def test_login_form_valid(self):
        """Test login with correct credentials."""
        response = self.client.post(
            self.url, {"username": TestValues.email, "password": TestValues.password}
        )
        self.assertRedirects(response, reverse("smakolyk:home"))

    def test_login_form_invalid(self):
        """Test login with incorrect credentials."""
        response = self.client.post(
            self.url, {"username": TestValues.email, "password": TestValues.email[:-1]}
        )
        self.assertEqual(response.status_code, HttpResponseBase.status_code)
        self.assertContains(response, ValidationMessages.invalid_login_form_message)


class CustomSignupViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("signup")

    def tearDown(self):
        UserProfile.objects.all().delete()
        CustomUser.objects.all().delete()

    def test_signup_form_valid(self):
        """Test signup with valid data."""
        data = {
            "email": TestValues.email,
            "username": TestValues.username,
            "first_name": TestValues.name,
            "last_name": TestValues.surname,
            "phone": TestValues.valid_phonenumber1,
            "password1": TestValues.password,
            "password2": TestValues.password,
        }
        response = self.client.post(self.url, data)

        self.assertRedirects(response, reverse("success"))
        self.assertTrue(
            get_user_model().objects.filter(email=TestValues.email).exists()
        )

    def test_signup_form_invalid(self):
        """Test signup with invalid data."""
        data = {
            "email": TestValues.email,
            "username": TestValues.username,
            "first_name": TestValues.name,
            "last_name": TestValues.surname,
            "phone": TestValues.valid_phonenumber1,
            "password1": TestValues.password,
            "password2": TestValues.password[:-1],
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, HttpResponseBase.status_code)
        self.assertFormError(
            response, "form", None, ValidationMessages.clean_password_validation_message
        )


class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email=TestValues.email, password=TestValues.password
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            username=TestValues.username,
            first_name=TestValues.name,
            last_name=TestValues.surname,
            slug=slugify(TestValues.username),
            phone=TestValues.valid_phonenumber1,
        )
        self.client.login(email=TestValues.email, password=TestValues.password)
        self.url = reverse("profile")

    def tearDown(self):
        UserProfile.objects.all().delete()
        CustomUser.objects.all().delete()

    def test_profile_view(self):
        """Test that the profile view renders correctly."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HttpResponseBase.status_code)
        self.assertTemplateUsed(response, "profile.html")


class EditProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email=TestValues.email,
            password=TestValues.password,
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            username=TestValues.username,
            first_name=TestValues.name,
            last_name=TestValues.surname,
            slug=slugify(TestValues.username),
            phone=TestValues.valid_phonenumber1,
            birthdate=datetime.now().date()
            - relativedelta(
                days=TestValuesMethods.DAYS_IN_ONE_YEAR
                * (ValidationValues.minimal_user_age + 1)
            ),
        )
        self.client.login(email=TestValues.email, password=TestValues.password)
        self.url = reverse("edit-profile", kwargs={"slug": self.profile.slug})

    def tearDown(self):
        UserProfile.objects.all().delete()
        CustomUser.objects.all().delete()

    def test_edit_profile_form_valid(self):
        """Test editing profile with valid data."""
        data = {
            "username": TestValuesMethods.get_username(),
            "first_name": TestValuesMethods.get_first_name(),
            "last_name": TestValuesMethods.get_last_name(),
            "birthdate": datetime.now().date()
            - relativedelta(
                days=TestValuesMethods.DAYS_IN_ONE_YEAR
                * (ValidationValues.maximal_user_age - 1)
            ),
            "phone": TestValues.valid_phonenumber2,
        }
        response = self.client.post(self.url, data)

        self.assertRedirects(response, reverse("profile"))

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.username, data["username"])
        self.assertEqual(self.profile.first_name, data["first_name"])
        self.assertEqual(self.profile.last_name, data["last_name"])
        self.assertEqual(self.profile.phone, data["phone"])

    def test_edit_profile_form_invalid(self):
        """Test editing profile with invalid data."""
        data = {
            "username": "a" * (ValidationValues.username_min_length - 1),
            "first_name": TestValuesMethods.get_first_name(),
            "last_name": TestValuesMethods.get_last_name(),
            "birthdate": datetime.now().date()
            - relativedelta(
                days=TestValuesMethods.DAYS_IN_ONE_YEAR
                * (ValidationValues.minimal_user_age - 1)
            ),
            "phone": TestValues.valid_phonenumber2,
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, HttpResponseBase.status_code)
        self.assertFormError(
            response, "form", "username", ValidationMessages.username_validation_message
        )
