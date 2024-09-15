from dataclasses import dataclass
from random import randint

from faker import Faker

from apps.user.values import ValidationValues

_FAKER = Faker("en_US")


class TestValuesMethods:
    @staticmethod
    def get_quantity() -> int:
        """
        Returns the quantity of the dish
        :return: the quantity of the dish
        """
        return randint(1, 5)

    @staticmethod
    def get_dish_name() -> str:
        """
        Returns the name of the dish
        :return: the name of the dish
        """
        return _FAKER.word()

    @staticmethod
    def get_price() -> int:
        """
        Returns random dish price
        :return: int
        """
        return randint(1, 100)

    @staticmethod
    def get_email() -> str:
        """
        Returns random email address
        :return: str
        """
        return _FAKER.email()

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


@dataclass
class TestValues:
    # user test values
    email: str = _FAKER.email()
    password: str = _FAKER.password()
    name: str = TestValuesMethods.get_first_name()
    surname: str = TestValuesMethods.get_last_name()
    username: str = _FAKER.word()
    phone_number: str = _FAKER.phone_number()
    valid_phonenumber1: str = "+380970082875"
    valid_phonenumber2: str = "+380970082876"
