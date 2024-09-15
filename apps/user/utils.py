from abc import ABC, abstractmethod
from datetime import datetime

from django.core.exceptions import ValidationError

from .custom_validators import is_too_old, is_too_young
from .models import CustomUser, UserProfile
from .values import ValidationMessages


class BaseFieldsDataValidator(ABC):
    @staticmethod
    def _validate_username(username: str = None) -> None:
        """
        Validate's username
        :param username: str = None
        :return: None
        """

        if UserProfile.objects.filter(username=username).exists():
            raise ValidationError(ValidationMessages.clean_username_validation_message)

    @staticmethod
    def _validate_phone_number(phone_number: str = None) -> None:
        """
        Validate's phone number
        :param phone_number: phone_number: str = None
        :return: None
        """

        if UserProfile.objects.filter(phone=phone_number).exists():
            raise ValidationError(ValidationMessages.clean_phone_validation_message)

    @abstractmethod
    def validate(self):
        pass


class SignUpFieldsDataValidator(BaseFieldsDataValidator):
    @staticmethod
    def _validate_email(email: str = None) -> None:
        """
        Validate's email
        :param email: str = None
        :return: None
        """

        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(ValidationMessages.clean_email_validation_message)

    @staticmethod
    def _password_match_validator(password1: str = None, password2: str = None) -> None:
        """
        Validate's password match
        :param password1: str = None
        :param password2: str = None
        :return: None
        """

        if not password1 == password2:
            raise ValidationError(ValidationMessages.clean_password_validation_message)

    @classmethod
    def validate(cls, cleaned_data: dict = None) -> None:
        """
        Validates given cleaned data
        :param cleaned_data: dict = None
        :return: None
        """

        cls._validate_email(
            email=cleaned_data.get("email", ""),
        )
        cls._validate_username(username=cleaned_data.get("username", ""))
        cls._validate_phone_number(phone_number=cleaned_data.get("phone", ""))
        cls._password_match_validator(
            password1=cleaned_data.get("password1", ""),
            password2=cleaned_data.get("password2", ""),
        )


class EditProfileFieldsValidator(BaseFieldsDataValidator):
    @staticmethod
    def _validate_birthday(birthday: datetime = None) -> None:
        """
        Validates birthday
        :param birthday: datetime = None
        :return: None
        """
        if birthday:
            cleaned_birthday = datetime.strptime(str(birthday), "%Y-%m-%d").date()

            if is_too_young(cleaned_birthday) or is_too_old(cleaned_birthday):
                raise ValidationError(
                    ValidationMessages.clean_birthday_validation_message
                )

    @classmethod
    def validate(
        cls, cleaned_data: dict = None, userprofile: UserProfile = None
    ) -> None:
        """
        Validates given cleaned data
        :param cleaned_data: dict = None
        :param userprofile: UserProfile = None
        :return: None
        """

        cls._validate_birthday(birthday=cleaned_data.get("birthdate", None))

        if (username := cleaned_data.get("username", "")) != userprofile.username:
            cls._validate_username(username=username)

        if (phone := cleaned_data.get("phone", "")) != userprofile.phone:
            cls._validate_phone_number(phone_number=phone)
