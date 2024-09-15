from django import forms
from django.db import transaction
from django.utils import timezone

from .models import History, Order
from .utils import get_menu_choices, get_order_data, get_order_total
from .values import FormDefaultValues, ViewSettingValues


class DisabledOptionWidget(forms.Select):
    def render(self, name, value, attrs=None, renderer=None):
        html_code = super(DisabledOptionWidget, self).render(
            name, value, attrs, renderer
        )
        html_code = html_code.replace(
            '<option value=""', '<option value="------" disabled'
        )

        return html_code


class OrderForm(forms.ModelForm):
    first_course = forms.ChoiceField(required=False, widget=DisabledOptionWidget)
    first_course_quantity = forms.IntegerField(min_value=0, required=False)
    second_course = forms.ChoiceField(required=False, widget=DisabledOptionWidget)
    second_course_quantity = forms.IntegerField(min_value=0, required=False)
    dessert = forms.ChoiceField(required=False, widget=DisabledOptionWidget)
    dessert_quantity = forms.IntegerField(min_value=0, required=False)
    drink = forms.ChoiceField(required=False, widget=DisabledOptionWidget)
    drink_quantity = forms.IntegerField(min_value=0, required=False)
    date = forms.DateField(required=False)

    class Meta:
        model = Order
        fields = ViewSettingValues.ORDER_FORM_FIELDS

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        self.user = self.initial.get("user", None)

        # I'm altering choices dynamically, so there won't be any error on running `makemigrations` command
        self.fields["first_course"].choices = get_menu_choices("first_course")
        self.fields["second_course"].choices = get_menu_choices("second_course")
        self.fields["dessert"].choices = get_menu_choices("dessert")
        self.fields["drink"].choices = get_menu_choices("drink")

    def save(self, commit=True):
        with transaction.atomic():
            order = self.create_order_object()
            order.save()

            order_data = get_order_data(order)
            total_amount = get_order_total(order_data)

            self.create_history_object(order, total_amount, order_data)

            return order, order_data, total_amount

    def create_order_object(self) -> Order:
        """
        A method that creates an Order object.
        :return: Order object
        """
        return Order(
            user=self.user,
            date=self.cleaned_data.get("date") or timezone.now().date(),
            first_course=self.cleaned_data.get("first_course")
            or FormDefaultValues.DISH_NOT_CHOSEN_DEFAULT_VALUE,
            first_course_quantity=self.cleaned_data.get("first_course_quantity")
            or FormDefaultValues.DISH_QUANTIRY_NOT_CHOSEN_DEFAULT_VALUE,
            second_course=self.cleaned_data.get("second_course")
            or FormDefaultValues.DISH_NOT_CHOSEN_DEFAULT_VALUE,
            second_course_quantity=self.cleaned_data.get("second_course_quantity")
            or FormDefaultValues.DISH_QUANTIRY_NOT_CHOSEN_DEFAULT_VALUE,
            dessert=self.cleaned_data.get("dessert")
            or FormDefaultValues.DISH_NOT_CHOSEN_DEFAULT_VALUE,
            dessert_quantity=self.cleaned_data.get("dessert_quantity")
            or FormDefaultValues.DISH_QUANTIRY_NOT_CHOSEN_DEFAULT_VALUE,
            drink=self.cleaned_data.get("drink")
            or FormDefaultValues.DISH_NOT_CHOSEN_DEFAULT_VALUE,
            drink_quantity=self.cleaned_data.get("drink_quantity")
            or FormDefaultValues.DISH_QUANTIRY_NOT_CHOSEN_DEFAULT_VALUE,
        )

    @staticmethod
    def create_history_object(
        order: Order, total_amount: int, order_data: dict
    ) -> None:
        """
        A method that creates a History object.
        :param order: Order object
        :param total_amount: int
        :param order_data: dict
        :return: None
        """
        History.objects.create(
            user=order.user,
            date=order.date,
            total_amount=total_amount,
            first_course=order.first_course,
            first_course_quantity=order.first_course_quantity,
            first_course_price=order_data.get("first_course_price"),
            second_course=order.second_course,
            second_course_quantity=order.second_course_quantity,
            second_course_price=order_data.get("second_course_price"),
            dessert=order.dessert,
            dessert_quantity=order.dessert_quantity,
            dessert_price=order_data.get("dessert_price"),
            drink=order.drink,
            drink_quantity=order.drink_quantity,
            drink_price=order_data.get("drink_price"),
        )
