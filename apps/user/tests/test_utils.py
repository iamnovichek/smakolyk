from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.user.models import CustomUser, UserProfile
from apps.user.utils import EditProfileFieldsValidator, SignUpFieldsDataValidator

from .values import TestValues, TestValuesMethods


class SignUpFieldsDataValidatorTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email=TestValues.email, password=TestValues.password
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            username=TestValues.username,
            phone=TestValues.phone_number,
        )
        self.cleaned_data = {
            "email": TestValuesMethods.get_email(),
            "username": TestValuesMethods.get_username(),
            "phone": TestValuesMethods.get_phone_number(),
            "password1": TestValues.password,
            "password2": TestValues.password,
        }

    def tearDown(self):
        UserProfile.objects.all().delete()
        CustomUser.objects.all().delete()

    def test_validate_valid_data(self):
        """Test that the validator passes with valid data."""
        try:
            SignUpFieldsDataValidator.validate(self.cleaned_data)
        except ValidationError:
            self.fail("ValidationError raised with valid data.")

    def test_validate_existing_email(self):
        """Test that the validator raises an error for an existing email."""
        self.cleaned_data["email"] = TestValues.email

        with self.assertRaises(ValidationError):
            SignUpFieldsDataValidator.validate(self.cleaned_data)

    def test_validate_existing_username(self):
        """Test that the validator raises an error for an existing username."""
        self.cleaned_data["username"] = TestValues.username

        with self.assertRaises(ValidationError):
            SignUpFieldsDataValidator.validate(self.cleaned_data)

    def test_validate_existing_phone(self):
        """Test that the validator raises an error for an existing phone number."""
        self.cleaned_data["phone"] = TestValues.phone_number

        with self.assertRaises(ValidationError):
            SignUpFieldsDataValidator.validate(self.cleaned_data)

    def test_password_mismatch(self):
        """Test that the validator raises an error for mismatched passwords."""
        self.cleaned_data["password2"] = TestValues.password[:-1]

        with self.assertRaises(ValidationError):
            SignUpFieldsDataValidator.validate(self.cleaned_data)


class EditProfileFieldsValidatorTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email=TestValues.email, password=TestValues.password
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            username=TestValues.username,
            phone=TestValues.phone_number,
            birthdate=TestValuesMethods.get_birthdate(),
        )
        self.cleaned_data = {
            "username": TestValuesMethods.get_username(),
            "phone": TestValuesMethods.get_phone_number(),
            "birthdate": TestValuesMethods.get_birthdate(),
        }

    def tearDown(self):
        UserProfile.objects.all().delete()
        CustomUser.objects.all().delete()

    def test_validate_valid_data(self):
        """Test that the validator passes with valid data."""
        try:
            EditProfileFieldsValidator.validate(self.cleaned_data, self.profile)
        except ValidationError:
            self.fail("ValidationError raised with valid data.")

    def test_validate_new_username(self):
        """Test that the validator raises an error for an existing username."""

        existing_username = TestValuesMethods.get_username()

        UserProfile.objects.create(
            user=CustomUser.objects.create_user(
                email=TestValuesMethods.get_email(), password=TestValues.password
            ),
            username=existing_username,
            phone=TestValuesMethods.get_phone_number(),
        )
        self.cleaned_data["username"] = existing_username

        with self.assertRaises(ValidationError):
            EditProfileFieldsValidator.validate(self.cleaned_data, self.profile)

    def test_validate_new_phone(self):
        """Test that the validator raises an error for an existing phone number."""
        existing_phone_number = TestValuesMethods.get_phone_number()
        UserProfile.objects.create(
            user=CustomUser.objects.create_user(
                email=TestValuesMethods.get_email(), password=TestValues.password
            ),
            username=TestValuesMethods.get_username(),
            phone=existing_phone_number,
        )
        self.cleaned_data["phone"] = existing_phone_number

        with self.assertRaises(ValidationError):
            EditProfileFieldsValidator.validate(self.cleaned_data, self.profile)
