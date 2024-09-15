from datetime import date

from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.text import slugify

from apps.smakolyk.models import History, Menu, Order
from apps.smakolyk.values import ViewSettingValues
from apps.user.models import CustomUser, UserProfile

from .values import TestValues, TestValuesMethods


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email=TestValues.email, password=TestValues.password
        )
        UserProfile.objects.create(
            user=cls.user,
            username=TestValues.username,
            first_name=TestValues.name,
            last_name=TestValues.surname,
            phone=TestValues.phone_number,
            slug=slugify(TestValues.username),
        )

        cls.menu = Menu.objects.create(
            first_course=TestValuesMethods.get_dish_name(),
            first_course_price=TestValuesMethods.get_price(),
            second_course=TestValuesMethods.get_dish_name(),
            second_course_price=TestValuesMethods.get_price(),
            dessert=TestValuesMethods.get_dish_name(),
            dessert_price=TestValuesMethods.get_price(),
            drink=TestValuesMethods.get_dish_name(),
            drink_price=TestValuesMethods.get_price(),
        )
        cls.first_course_quantity = TestValuesMethods.get_quantity()
        cls.order = Order.objects.create(
            user=cls.user,
            date=date.today(),
            first_course=cls.menu.first_course,
            first_course_quantity=cls.first_course_quantity,
            second_course=cls.menu.second_course,
            second_course_quantity=TestValuesMethods.get_quantity(),
            dessert=cls.menu.dessert,
            dessert_quantity=TestValuesMethods.get_quantity(),
            drink=cls.menu.drink,
            drink_quantity=TestValuesMethods.get_quantity(),
        )

    def tearDown(self):
        Menu.objects.all().delete()
        Order.objects.all().delete()
        UserProfile.objects.all().delete()
        CustomUser.objects.all().delete()

    def test_order_creation(self):
        """Test that an order is created correctly"""
        order = Order.objects.get(id=self.order.id)

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.first_course, self.menu.first_course)
        self.assertEqual(order.first_course_quantity, self.first_course_quantity)

    def test_order_string_representation(self):
        """Test the string representation of the order"""
        order = Order.objects.get(id=self.order.id)

        self.assertEqual(
            str(order), f"{order.user.userprofile.username}'s order on {order.date}"
        )

    def test_order_foreignkey_relationship(self):
        """Test that order ForeignKey user relationship works"""
        self.assertEqual(self.order.user, self.user)

    def test_invalid_order_quantity(self):
        """Test that invalid order quantity raises validation error"""
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Order.objects.create(
                    user=self.user,
                    date=date.today(),
                    first_course=self.menu.first_course,
                    first_course_quantity=-1,  # Invalid quantity
                    second_course=self.menu.second_course,
                    second_course_quantity=TestValuesMethods.get_quantity(),
                    dessert=self.menu.dessert,
                    dessert_quantity=TestValuesMethods.get_quantity(),
                    drink=self.menu.drink,
                    drink_quantity=TestValuesMethods.get_quantity(),
                )


class MenuModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.menu = Menu.objects.create(
            first_course=TestValuesMethods.get_dish_name(),
            first_course_price=TestValuesMethods.get_price(),
            second_course=TestValuesMethods.get_dish_name(),
            second_course_price=TestValuesMethods.get_price(),
            dessert=TestValuesMethods.get_dish_name(),
            dessert_price=TestValuesMethods.get_price(),
            drink=TestValuesMethods.get_dish_name(),
            drink_price=TestValuesMethods.get_price(),
        )

    def tearDown(self):
        Menu.objects.all().delete()

    def test_menu_creation(self):
        """Test that the menu is created correctly"""
        menu = Menu.objects.get(id=self.menu.id)

        self.assertEqual(menu.first_course, self.menu.first_course)
        self.assertEqual(menu.first_course_price, self.menu.first_course_price)

    def test_menu_unique_fields(self):
        """Test that unique constraint on menu fields is enforced"""
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Menu.objects.create(
                    first_course=self.menu.first_course,
                    first_course_price=TestValuesMethods.get_price(),
                    second_course=TestValuesMethods.get_dish_name(),
                    second_course_price=TestValuesMethods.get_price(),
                    dessert=TestValuesMethods.get_dish_name(),
                    dessert_price=TestValuesMethods.get_price(),
                    drink=TestValuesMethods.get_dish_name(),
                    drink_price=TestValuesMethods.get_price(),
                )


class HistoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email=TestValues.email, password=TestValues.password
        )
        UserProfile.objects.create(
            user=cls.user,
            username=TestValues.username,
            first_name=TestValues.name,
            last_name=TestValues.surname,
            phone=TestValues.phone_number,
            slug=slugify(TestValues.username),
        )

        cls.history = History.objects.create(
            user=cls.user,
            date=date.today(),
            total_amount=ViewSettingValues.MAX_ORDER_AMOUNT,
            first_course=TestValuesMethods.get_dish_name(),
            first_course_quantity=TestValuesMethods.get_quantity(),
            first_course_price=TestValuesMethods.get_price(),
            second_course=TestValuesMethods.get_dish_name(),
            second_course_quantity=TestValuesMethods.get_quantity(),
            second_course_price=TestValuesMethods.get_price(),
            dessert=TestValuesMethods.get_dish_name(),
            dessert_quantity=TestValuesMethods.get_quantity(),
            dessert_price=TestValuesMethods.get_price(),
            drink=TestValuesMethods.get_dish_name(),
            drink_quantity=TestValuesMethods.get_quantity(),
            drink_price=TestValuesMethods.get_price(),
        )

    def tearDown(self):
        Menu.objects.all().delete()
        UserProfile.objects.all().delete()
        CustomUser.objects.all().delete()

    def test_history_creation(self):
        """Test that history is created correctly"""
        history = History.objects.filter(id=self.history.id).first()

        self.assertEqual(history.total_amount, self.history.total_amount)
        self.assertEqual(history.first_course, self.history.first_course)

    def test_history_ordering(self):
        """Test history ordering by date"""
        first_history = History.objects.first()

        self.assertEqual(first_history, self.history)

    def test_history_string_representation(self):
        """Test the string representation of history"""
        history = History.objects.filter(id=self.history.id).first()

        self.assertEqual(
            str(history),
            f"{history.user.userprofile.username}'s history order on {history.date}",
        )
