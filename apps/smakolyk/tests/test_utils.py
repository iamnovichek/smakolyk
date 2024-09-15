from datetime import date, datetime
from unittest.mock import patch

import pandas as pd
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.text import slugify

from apps.smakolyk.models import Menu, Order
from apps.smakolyk.utils import (
    get_current_week_dates,
    get_dates_dict,
    get_days_dict,
    get_dish_price,
    get_menu_choices,
    get_order_data,
    get_order_total,
    notify_about_oversum,
    notify_accountant,
    notify_user,
    validate_column_names_correspondence,
    validate_file_extension,
    validate_file_size,
)
from apps.smakolyk.values import DataMappingValues, ValidationValues, ViewSettingValues
from apps.user.models import CustomUser, UserProfile

from .values import TestValues, TestValuesMethods


class NotificationTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email=TestValues.email,
            password=TestValues.password,
        )
        self.max_sum = ViewSettingValues.MAX_ORDER_AMOUNT
        UserProfile(
            user=self.user,
            username=TestValues.username,
            first_name=TestValues.name,
            last_name=TestValues.surname,
            slug=slugify(TestValues.username),
            phone=TestValues.phone_number,
        ).save()

    def tearDown(self):
        UserProfile.objects.all().delete()
        CustomUser.objects.all().delete()

    @patch("apps.smakolyk.utils.send_mail")
    def test_notify_user(self, mock_send_mail):
        """Test notify_user function to ensure it sends an email."""
        order_date = datetime.today()

        notify_user(user=self.user, order_date=order_date, oversum=self.max_sum + 1)
        mock_send_mail.assert_called_once()

    @patch("apps.smakolyk.utils.send_mail")
    def test_notify_accountant(self, mock_send_mail):
        """Test notify_accountant function to ensure it sends an email."""

        notify_accountant(user=self.user, oversum=self.max_sum + 1)
        mock_send_mail.assert_called_once()

    @patch("apps.smakolyk.utils.notify_user")
    @patch("apps.smakolyk.utils.notify_accountant")
    def test_notify_about_oversum(self, mock_notify_user, mock_notify_accountant):
        """Test notify_about_oversum to ensure both user and accountant are notified."""
        order_date = datetime.today()

        notify_about_oversum(
            user=self.user, order_date=order_date, oversum=self.max_sum + 1
        )
        mock_notify_user.assert_called_once()
        mock_notify_accountant.assert_called_once()


class CalculationTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email=TestValues.email,
            password=TestValues.password,
        )

    def tearDown(self):
        Menu.objects.all().delete()
        CustomUser.objects.all().delete()

    def test_get_order_total(self):
        """Test get_order_total to ensure the total sum is calculated correctly."""
        fist_course_price = TestValuesMethods.get_price()
        second_course_price = TestValuesMethods.get_price()
        dessert_price = TestValuesMethods.get_price()
        drink_price = TestValuesMethods.get_price()
        data = {
            "first_course_quantity": TestValuesMethods.get_quantity(),
            "first_course_price": fist_course_price,
            "second_course_quantity": TestValuesMethods.get_quantity(),
            "second_course_price": second_course_price,
            "dessert_quantity": TestValuesMethods.get_quantity(),
            "dessert_price": dessert_price,
            "drink_quantity": TestValuesMethods.get_quantity(),
            "drink_price": drink_price,
        }
        total = get_order_total(data)
        self.assertEqual(
            total,
            sum(
                [
                    data[quantity] * data[price]
                    for quantity, price in zip(
                        DataMappingValues.dish_quantity_field_names,
                        DataMappingValues.dish_price_field_names,
                    )
                ]
            ),
        )

    def test_get_dish_price(self):
        """Test get_dish_price to ensure it returns the correct price for a dish."""
        Menu.objects.create(
            first_course="Soup",
            first_course_price=10,
            second_course="Steak",
            second_course_price=15,
            dessert="Ice Cream",
            dessert_price=5,
            drink="Water",
            drink_price=2,
        )
        price = get_dish_price(dish_value="Soup", dish_type="first_course")
        self.assertEqual(price, 10)

    def test_get_order_data(self):
        """Test get_order_data to ensure it returns the correct data for an order."""
        Menu.objects.create(
            first_course="Soup",
            first_course_price=10,
            second_course="Steak",
            second_course_price=15,
            dessert="Ice Cream",
            dessert_price=5,
            drink="Water",
            drink_price=2,
        )
        order = Order.objects.create(
            user=self.user,
            date=date.today(),
            first_course="Soup",
            first_course_quantity=2,
            second_course="Steak",
            second_course_quantity=1,
            dessert="Ice Cream",
            dessert_quantity=1,
            drink="Water",
            drink_quantity=1,
        )

        data = get_order_data(order)

        self.assertEqual(data["first_course_quantity"], 2)
        self.assertEqual(data["first_course_price"], 10)


class UtilityTestCase(TestCase):
    def test_get_current_week_dates(self):
        """Test get_current_week_dates to ensure it returns correct dates."""
        dates = get_current_week_dates()

        self.assertEqual(len(dates), ViewSettingValues.FORMS_NUMBER)
        self.assertTrue(all(isinstance(date_, date) for date_ in dates))

    def test_get_days_dict(self):
        """Test get_days_dict to ensure it returns correct days."""
        days = get_days_dict()

        self.assertEqual(len(days), ViewSettingValues.FORMS_NUMBER)

    def test_get_dates_dict(self):
        """Test get_dates_dict to ensure it returns correct dates."""
        dates = get_dates_dict()

        self.assertEqual(len(dates), ViewSettingValues.FORMS_NUMBER)


class FileValidationTestCase(TestCase):
    def test_validate_file_extension(self):
        """Test validate_file_extension to ensure invalid file extension raises error."""
        file = SimpleUploadedFile("file.txt", b"file_content")

        with self.assertRaises(ValidationError):
            validate_file_extension(file)

    def test_validate_file_size(self):
        """Test validate_file_size to ensure large file raises error."""
        file = SimpleUploadedFile("file.csv", b"file_content" * 1000)
        file.size = ValidationValues.max_file_size + 1

        with self.assertRaises(ValidationError):
            validate_file_size(file)

    def test_validate_column_names_correspondence(self):
        """Test validate_column_names_correspondence to ensure column mismatch raises error."""
        data = pd.DataFrame(
            {
                "wrong_col": ["value1", "value2"],
                "another_wrong_col": ["value3", "value4"],
            }
        )

        with self.assertRaises(ValidationError):
            validate_column_names_correspondence(data)


class MenuChoicesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.menu = Menu.objects.create(
            first_course="Soup",
            first_course_price=10,
            second_course="Steak",
            second_course_price=15,
            dessert="Ice Cream",
            dessert_price=5,
            drink="Water",
            drink_price=2,
        )

    def tearDown(self):
        Menu.objects.all().delete()

    def test_get_menu_choices(self):
        """Test get_menu_choices to ensure correct choices are returned."""
        choices = get_menu_choices("first_course")

        self.assertIn(("Soup", "Soup"), choices)
