from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.text import slugify

from apps.user.models import CustomUser, UserProfile

from .values import TestValues


class CustomUserTests(TestCase):
    def setUp(self):
        self.user_data = {
            "email": TestValues.email,
            "password": TestValues.password,
        }

    def tearDown(self):
        CustomUser.objects.all().delete()

    def test_create_user_with_valid_data(self):
        """Test user creation with valid email and password"""
        user = CustomUser.objects.create_user(**self.user_data)

        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))
        self.assertFalse(user.is_admin)
        self.assertTrue(user.is_active)

    def test_create_user_without_email(self):
        """Test that user creation without email raises an error"""
        with self.assertRaises(ValidationError):
            CustomUser.objects.create_user(
                email=None, password=self.user_data["password"]
            )

    def test_create_user_without_password(self):
        """Test that user creation without password raises an error"""
        with self.assertRaises(ValidationError):
            CustomUser.objects.create_user(email=self.user_data["email"], password=None)

    def test_create_superuser(self):
        """Test superuser creation with valid data"""
        superuser = CustomUser.objects.create_superuser(**self.user_data)

        self.assertEqual(superuser.email, self.user_data["email"])
        self.assertTrue(superuser.check_password(self.user_data["password"]))
        self.assertTrue(superuser.is_admin)

    def test_string_representation(self):
        """Test the string representation of CustomUser"""
        user = CustomUser.objects.create_user(**self.user_data)

        self.assertEqual(str(user), user.email)


class UserProfileTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email=TestValues.email, password=TestValues.password
        )
        self.profile_data = {
            "user": self.user,
            "username": TestValues.username,
            "first_name": TestValues.name,
            "last_name": TestValues.surname,
            "birthdate": TestValues.birthday,
            "phone": TestValues.phone_number,
        }

    def tearDown(self):
        CustomUser.objects.all().delete()
        UserProfile.objects.all().delete()

    def test_profile_creation(self):
        """Test creating a valid user profile"""
        profile = UserProfile.objects.create(**self.profile_data)

        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.username, self.profile_data["username"])
        self.assertEqual(profile.slug, slugify(self.profile_data["username"]))

    def test_invalid_phone_number(self):
        """Test validation of an invalid phone number"""
        self.profile_data["phone"] = ""
        profile = UserProfile(**self.profile_data)

        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_min_length_username(self):
        """Test username minimum length validation"""
        self.profile_data["username"] = ""
        profile = UserProfile(**self.profile_data)

        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_string_representation(self):
        """Test string representation of UserProfile"""
        profile = UserProfile.objects.create(**self.profile_data)

        self.assertEqual(str(profile), profile.username)
