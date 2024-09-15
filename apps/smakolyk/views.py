import json
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import (
    HttpResponseBadRequest,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView, TemplateView

from apps.user.models import CustomUser

from .forms import OrderForm
from .models import History, Menu, Order
from .utils import (
    get_current_week_dates,
    get_dates_dict,
    get_days_dict,
    notify_about_oversum,
)
from .values import DataMappingValues, ViewSettingValues


class HomePageView(CreateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        menu: dict[str, list] = dict()

        for field_name in DataMappingValues.dish_field_names:
            dishes = Menu.objects.values_list(field_name, flat=True)
            # Splitting dishes into chunks
            menu[field_name] = [
                dishes[i : i + ViewSettingValues.CHUNK_MENU_SIZE]
                for i in range(0, len(dishes), ViewSettingValues.CHUNK_MENU_SIZE)
            ]

        return render(
            request,
            self.template_name,
            {
                "menu": menu,
                "has_order": History.objects.filter(user_id=request.user.id).exists(),
            },
        )


class OrderView(LoginRequiredMixin, CreateView):
    login_url = "login"
    template_name = "order.html"
    success_url = "smakolyk:order_success"
    model = Order
    formset = formset_factory(
        form=OrderForm,
        extra=ViewSettingValues.FORMS_NUMBER,
    )

    def get(self, request, *args, **kwargs):
        if result := self.check_page_accessibility():
            return result

        formset = self.formset()
        days = get_days_dict()

        return render(
            request,
            self.template_name,
            context={"formset": formset, "days": days, **get_dates_dict()},
        )

    def post(self, request, *args, **kwargs):
        formset = self.formset(
            request.POST,
            initial=[{"user": request.user}] * ViewSettingValues.FORMS_NUMBER,
        )

        if formset.is_valid():
            for form in formset:
                order, order_data, total_amount = form.save()

                if total_amount > ViewSettingValues.MAX_ORDER_AMOUNT:
                    user = get_object_or_404(CustomUser, id=request.user.id)
                    oversum = total_amount - ViewSettingValues.MAX_ORDER_AMOUNT

                    notify_about_oversum(
                        user=user, oversum=oversum, order_date=order.date
                    )

            return redirect(self.success_url)

        [messages.error(request, error) for error in formset.errors]
        return render(
            request,
            self.template_name,
            context={"formset": formset, "days": get_days_dict(), **get_dates_dict()},
        )

    def check_page_accessibility(
        self,
    ) -> None | HttpResponsePermanentRedirect | HttpResponseRedirect:
        """
        Checks if the user has access to the page.
        :return: None
        """
        if self.order_exists_for_the_next_week():
            return redirect("smakolyk:order_error")

        if self.is_weekend():
            return redirect("smakolyk:weekend")

    def order_exists_for_the_next_week(self) -> bool:
        """
        Check if order exists for current week
        :return: bool
        """
        dates = get_current_week_dates()

        for date_ in dates:
            if Order.objects.filter(date=date_, user_id=self.request.user.id).exists():
                return True

        return False

    @staticmethod
    def is_weekend() -> bool:
        """
        Checks if today it's weekend
        :return: bool
        """
        return datetime.now().weekday() > ViewSettingValues.FRIDAY_WEEKDAY_NUMBER or (
            datetime.now().weekday() >= ViewSettingValues.FRIDAY_WEEKDAY_NUMBER
            and datetime.now().time().hour >= ViewSettingValues.WEEKEND_START_HOUR
        )


class PriceSetterAjaxView(View):
    def get(self, request, *args, **kwargs):
        menu = dict()

        for dish_field_name, dish_price_field_name in zip(
            DataMappingValues.dish_field_names, DataMappingValues.dish_price_field_names
        ):
            menu.update({dish_field_name: dict()})

            for dish, price in zip(
                list(Menu.objects.values_list(dish_field_name, flat=True)),
                list(Menu.objects.values_list(dish_price_field_name, flat=True)),
            ):
                menu[dish_field_name].update({dish: price})

        return JsonResponse({"response": menu})


class TotalAmountCounterAjaxView(View):
    total_amount = ViewSettingValues.MAX_ORDER_AMOUNT

    def post(self, request, *args, **kwargs):

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON"}, status=HttpResponseBadRequest.status_code
            )

        dish_quantities = [
            self._get_value(field_name, data)
            for field_name in DataMappingValues.dish_quantity_field_names
        ]
        dish_prices = [
            self._get_value(field_name, data)
            for field_name in DataMappingValues.dish_price_field_names
        ]

        result = self.total_amount - sum(
            [price * quantity for price, quantity in zip(dish_prices, dish_quantities)]
        )

        return JsonResponse(
            {
                "response": result,
                "amount_deducted": result < ViewSettingValues.MIN_ORDER_VALUE,
            }
        )

    @staticmethod
    def _get_value(field_name: str, data: dict) -> int:
        """
        Get price from request.POST
        :param field_name: str
        :param data: dict
        :return: int
        """
        return int(data.get(f"{field_name}", ViewSettingValues.MIN_ORDER_VALUE))


class HistoryView(TemplateView):
    template_name = "history.html"

    def get(self, request, *args, **kwargs):
        current_week_days = self.get_current_week_days()

        if History.objects.filter(date=next(iter(current_week_days))).exists():
            data = {
                weekday: History.objects.get(
                    date=current_week_days[idx], user_id=request.user.id
                )
                for idx, weekday in enumerate(ViewSettingValues.WEEKDAY_NAMES)
            }

        else:
            next_week_days = self.get_next_week_days()

            data = {
                weekday: History.objects.get(
                    date=next_week_days[idx], user_id=request.user.id
                )
                for idx, weekday in enumerate(ViewSettingValues.WEEKDAY_NAMES)
            }

        return render(request, self.template_name, {"data": data})

    @staticmethod
    def get_current_week_days() -> list[date]:
        """
        Returns current week days
        :return: list[date]
        """
        today = date.today()
        current_weekday_number = today.weekday()
        start_of_the_week = today + timedelta(days=0 - current_weekday_number)

        return [(start_of_the_week + timedelta(days=i)) for i in range(5)]

    @staticmethod
    def get_next_week_days() -> list[date]:
        """
        Returns next week days
        :return: list[date]
        """
        today = date.today()
        current_weekday = today.weekday()
        start_of_week = today + timedelta(days=7 - current_weekday)

        return [(start_of_week + timedelta(days=i)) for i in range(5)]


class HistorySetterAjaxView(View):
    def get(self, request, *args, **kwargs):
        chosen_date = request.GET.get("date")

        if not History.objects.filter(date=chosen_date).exists():
            return JsonResponse({"date_exists": False})

        week_dates = self.get_dates_in_week(chosen_date)
        history_data = dict()

        for idx, weekday_name in enumerate(ViewSettingValues.WEEKDAY_NAMES):
            history_object = History.objects.filter(
                date=week_dates[idx], user_id=request.user.id
            ).first()
            history_data[weekday_name.lower()] = dict()

            for field_name in ViewSettingValues.HISTORY_OBJECT_FIELDS:
                field_value = getattr(history_object, field_name)

                history_data[weekday_name.lower()][field_name] = field_value

        return JsonResponse({"history_data": history_data, "date_exists": True})

    @staticmethod
    def get_dates_in_week(date_: str) -> list[str]:
        """
        Returns a list of dates that are present in the same week with `date_`
        :param date_: str
        :return: list[str]
        """
        formated_date = datetime.strptime(date_, "%Y-%m-%d").date()
        start_of_week = formated_date - timedelta(days=formated_date.weekday())

        return [
            (start_of_week + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)
        ]
