from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from apps.smakolyk.forms import OrderForm
from apps.smakolyk.models import History, Menu, Order
from apps.smakolyk.values import FormDefaultValues
from apps.user.models import CustomUser

from .values import TestValues, TestValuesMethods


class OrderFormTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email=TestValues.email,
            password=TestValues.password,
        )
        self.menu_data = {
            "first_course": TestValuesMethods.get_dish_name(),
            "first_course_price": TestValuesMethods.get_price(),
            "second_course": TestValuesMethods.get_dish_name(),
            "second_course_price": TestValuesMethods.get_price(),
            "dessert": TestValuesMethods.get_dish_name(),
            "dessert_price": TestValuesMethods.get_price(),
            "drink": TestValuesMethods.get_dish_name(),
            "drink_price": TestValuesMethods.get_price(),
        }
        Menu(**self.menu_data).save()

    def tearDown(self):
        Menu.objects.all().delete()
        CustomUser.objects.all().delete()
        History.objects.all().delete()
        Order.objects.all().delete()

    @patch("apps.smakolyk.forms.get_menu_choices")
    def test_order_form_valid(self, mock_get_menu_choices):
        """Test valid form submission creates an order and history entry."""
        mock_get_menu_choices.return_value = [
            (self.menu_data["first_course"], self.menu_data["first_course"]),
            (self.menu_data["second_course"], self.menu_data["second_course"]),
            (self.menu_data["dessert"], self.menu_data["dessert"]),
            (self.menu_data["drink"], self.menu_data["drink"]),
        ]

        form_data = {
            "first_course": self.menu_data["first_course"],
            "first_course_quantity": TestValuesMethods.get_quantity(),
            "second_course": self.menu_data["second_course"],
            "second_course_quantity": TestValuesMethods.get_quantity(),
            "dessert": self.menu_data["dessert"],
            "dessert_quantity": TestValuesMethods.get_quantity(),
            "drink": self.menu_data["drink"],
            "drink_quantity": TestValuesMethods.get_quantity(),
            "date": timezone.now().date(),
        }
        form = OrderForm(data=form_data, initial={"user": self.user})

        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(History.objects.count(), 1)

    def test_empty_fields_defaults(self):
        """Test that empty fields default to the specified values."""
        form_data = {
            "first_course": "",
            "first_course_quantity": 0,
            "second_course": "",
            "second_course_quantity": 0,
            "dessert": "",
            "dessert_quantity": 0,
            "drink": "",
            "drink_quantity": 0,
            "date": timezone.now().date(),
        }
        form = OrderForm(data=form_data, initial={"user": self.user})

        self.assertTrue(form.is_valid())
        order, order_data, total_amount = form.save()

        self.assertEqual(
            order.first_course, FormDefaultValues.DISH_NOT_CHOSEN_DEFAULT_VALUE
        )
        self.assertEqual(
            order.first_course_quantity,
            FormDefaultValues.DISH_QUANTIRY_NOT_CHOSEN_DEFAULT_VALUE,
        )

    @patch("apps.smakolyk.forms.get_order_total")
    def test_order_creation_with_total(self, mock_get_order_total):
        """Test that the correct total is calculated for an order."""
        mock_get_order_total.return_value = 100

        form_data = {
            "first_course": self.menu_data["first_course"],
            "first_course_quantity": TestValuesMethods.get_quantity(),
            "second_course": self.menu_data["second_course"],
            "second_course_quantity": TestValuesMethods.get_quantity(),
            "drink": self.menu_data["drink"],
            "drink_quantity": TestValuesMethods.get_quantity(),
            "date": timezone.now().date(),
        }
        form = OrderForm(data=form_data, initial={"user": self.user})

        self.assertTrue(form.is_valid())
        order, order_data, total_amount = form.save()

        self.assertEqual(total_amount, 100)

    @patch("apps.smakolyk.forms.get_menu_choices")
    def test_menu_choices_populated(self, mock_get_menu_choices):
        """Test that menu choices are correctly populated in form fields."""
        mock_get_menu_choices.return_value = [
            ("Dish 1", "Dish 1"),
            ("Dish 2", "Dish 2"),
        ]

        form = OrderForm(initial={"user": self.user})
        self.assertEqual(
            form.fields["first_course"].choices,
            [("Dish 1", "Dish 1"), ("Dish 2", "Dish 2")],
        )

    def test_disabled_option_widget_render(self):
        """Test that the DisabledOptionWidget renders a disabled empty option."""
        form = OrderForm(initial={"user": self.user})
        rendered_html = form["first_course"].as_widget()

        self.assertIn('<option value="------" disabled', rendered_html)
