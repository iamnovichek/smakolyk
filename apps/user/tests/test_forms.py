from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.test import TestCase

from apps.user.forms import CustomSignupForm, EditProfileForm
from apps.user.models import CustomUser, UserProfile
from apps.user.values import ValidationValues

from .values import TestValues, TestValuesMethods


class CustomSignupFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            "email": TestValues.email,
            "username": TestValues.username,
            "first_name": TestValues.name,
            "last_name": TestValues.surname,
            "phone": TestValues.valid_phonenumber1,
            "password1": TestValues.password,
            "password2": TestValues.password,
        }

    def tearDown(self):
        UserProfile.objects.all().delete()
        CustomUser.objects.all().delete()

    def test_valid_form(self):
        """Test that the form is valid with correct data."""
        form = CustomSignupForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_form_invalid_email(self):
        """Test that the form is invalid with an existing email."""
        CustomUser.objects.create_user(
            email=TestValues.email, password=TestValues.password
        )
        form = CustomSignupForm(data={**self.valid_data, "email": TestValues.email})

        self.assertFalse(form.is_valid())

    def test_form_password_mismatch(self):
        """Test that the form is invalid when passwords do not match."""
        form = CustomSignupForm(
            data={**self.valid_data, "password2": TestValues.password[:-1]}
        )

        self.assertFalse(form.is_valid())

    def test_save_creates_user_and_profile(self):
        """Test that the form correctly creates a user and profile."""
        form = CustomSignupForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertIsInstance(user, CustomUser)
        self.assertTrue(UserProfile.objects.filter(user=user).exists())


class EditProfileFormTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email=TestValues.email, password=TestValues.password
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            username=TestValues.username,
            first_name=TestValues.name,
            last_name=TestValues.surname,
            phone=TestValues.valid_phonenumber1,
            birthdate=TestValues.birthday,
        )

        self.form_data = {
            "username": TestValuesMethods.get_username(),
            "first_name": TestValuesMethods.get_first_name(),
            "last_name": TestValuesMethods.get_last_name(),
            "birthdate": TestValuesMethods.get_birthdate(),
            "phone": TestValues.valid_phonenumber2,
        }

    def tearDown(self):
        UserProfile.objects.all().delete()
        CustomUser.objects.all().delete()

    def test_valid_form(self):
        """Test that the form is valid with correct data."""
        form = EditProfileForm(
            instance=self.profile,
            data=self.form_data,
        )
        self.assertTrue(form.is_valid())

    def test_save_updates_profile(self):
        """Test that the form correctly updates the user profile."""
        form = EditProfileForm(
            instance=self.profile,
            data=self.form_data,
        )
        self.assertTrue(form.is_valid())

        form.save()

        self.profile.refresh_from_db()

        self.assertEqual(self.profile.username, self.form_data["username"])
        self.assertEqual(self.profile.first_name, self.form_data["first_name"])
        self.assertEqual(self.profile.last_name, self.form_data["last_name"])
        self.assertEqual(self.profile.phone, self.form_data["phone"])

    def test_form_invalid_birthday(self):
        """Test that the form is invalid with an inappropriate birthdate."""
        invalid_form_data = {
            **self.form_data,
            "birthdate": datetime.now().date()
            - relativedelta(
                days=TestValuesMethods.DAYS_IN_ONE_YEAR
                * (ValidationValues.minimal_user_age - 1)
            ),
        }  # Too young
        form = EditProfileForm(
            instance=self.profile,
            data=invalid_form_data,
        )
        self.assertFalse(form.is_valid())
