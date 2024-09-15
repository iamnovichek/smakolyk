from dataclasses import dataclass
from datetime import date, datetime, timedelta

from faker import Faker

from apps.user.values import ValidationValues

_FAKER = Faker("en_US")


class TestValuesMethods:
    DAYS_IN_ONE_YEAR = 365

    @staticmethod
    def get_email() -> str:
        """
        Returns random email address
        :return: str
        """
        return _FAKER.email()

    @staticmethod
    def get_random_uuid() -> str:
        """
        Returns random stripe id
        :return: str
        """

        return _FAKER.uuid4()

    @staticmethod
    def get_first_name() -> str:
        """
        Returns a random name of user
        :return: str
        """
        return (
            name
            if len(name := _FAKER.first_name())
            >= ValidationValues.first_name_min_length
            else "John"
        )

    @staticmethod
    def get_username() -> str:
        """
        Returns random username
        :return: str
        """
        return (
            username
            if len(username := _FAKER.word()) >= ValidationValues.username_min_length
            else "username"
        )

    @staticmethod
    def get_last_name() -> str:
        """
        Returns a random surname of user
        :return: str
        """
        return (
            surname
            if len(surname := _FAKER.first_name())
            >= ValidationValues.last_name_min_length
            else "Doe"
        )

    @staticmethod
    def get_phone_number() -> str:
        """
        Returns random phone number
        :return: str
        """
        return _FAKER.phone_number()

    @classmethod
    def get_birthdate(cls) -> date:
        """
        Generates a random birthdate for a person whose age is between min_age and max_age.
        :return: date
        """
        today = datetime.today()

        start_date = today - timedelta(
            days=ValidationValues.maximal_user_age * cls.DAYS_IN_ONE_YEAR
        )  # Oldest age
        end_date = today - timedelta(
            days=ValidationValues.maximal_user_age * cls.DAYS_IN_ONE_YEAR
        )  # Youngest age

        random_date = _FAKER.date_between(start_date=start_date, end_date=end_date)

        return random_date


@dataclass
class TestValues:
    # user test values
    email: str = _FAKER.email()
    invalid_email: str = "invalid_email"
    password: str = _FAKER.password()
    name: str = TestValuesMethods.get_first_name()
    surname: str = TestValuesMethods.get_last_name()
    is_active: bool = True
    username: str = _FAKER.word()
    phone_number: str = _FAKER.phone_number()
    valid_phonenumber1: str = "+380970082875"
    valid_phonenumber2: str = "+380970082876"
    birthday: str = TestValuesMethods.get_birthdate()
