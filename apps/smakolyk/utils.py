from datetime import date, datetime, timedelta

import pandas as pd
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import send_mail

from apps.user.models import CustomUser

from .models import Menu, Order
from .values import (
    DataMappingValues,
    EmailSenderTemplates,
    FormDefaultValues,
    ValidationMessages,
    ValidationValues,
    ViewSettingValues,
)


def notify_user(
    user: CustomUser = None, order_date: datetime = None, oversum: int = None
) -> None:
    """
    Sends a notification email to user
    :param user: CustomUser = None
    :param order_date: datetime = None
    :param oversum: int = None
    :return: None
    """
    send_mail(
        subject=EmailSenderTemplates.OVERSUM_SUBJECT,
        message=EmailSenderTemplates.OVERSUM_USER_MESSAGE.format(
            first_name=user.userprofile.first_name,
            last_name=user.userprofile.last_name,
            max_sum=oversum,
            order_date=order_date,
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user],
        fail_silently=False,
    )


def notify_accountant(user: CustomUser = None, oversum: int = None) -> None:
    """
    Sends a notification email to accountant
    :param user: CustomUser = None
    :param oversum: int = None
    :return: None
    """
    send_mail(
        subject=EmailSenderTemplates.OVERSUM_SUBJECT,
        message=EmailSenderTemplates.OVERSUM_ACCOUNTANT_MESSAGE.format(
            first_name=user.userprofile.first_name,
            last_name=user.userprofile.last_name,
            max_sum=oversum,
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.ACCOUNTANT],
        fail_silently=False,
    )


def notify_about_oversum(
    user: CustomUser = None, order_date: datetime = None, oversum: int = None
):
    """
    Notifies user and accountant about max_sum
    :param user: CustomUser = None
    :param order_date: datetime = None
    :param oversum: int = None
    :return: None
    """
    notify_user(user=user, order_date=order_date, oversum=oversum)
    notify_accountant(user=user, oversum=oversum)


def get_order_total(data: dict[str, int]) -> int:
    """
    Returns sum of all values in a dict
    :param data: dict[str, int] = None
    :return: int
    """
    return sum(
        [
            data[quantity] * data[price]
            for quantity, price in zip(
                DataMappingValues.dish_quantity_field_names,
                DataMappingValues.dish_price_field_names,
            )
        ]
    )


def get_dish_price(dish_value: str = None, dish_type: str = None) -> int:
    """
    Returns price of a dish
    :param dish_value: str = None
    :param dish_type: str = None
    :return: int
    """
    if dish_value in (
        dish_types := list(Menu.objects.values_list(f"{dish_type}", flat=True))
    ):
        index = dish_types.index(dish_value)

        return (
            list(Menu.objects.values_list(f"{dish_type}_price", flat=True))[index] or 0
        )


def get_order_data(order: Order = None) -> dict:
    """
    Returns data from a given Order object
    :param order: Order = None
    :return: dict
    """
    dish_quantities = {
        key: value or FormDefaultValues.DISH_QUANTIRY_NOT_CHOSEN_DEFAULT_VALUE
        for key, value in zip(
            DataMappingValues.dish_quantity_field_names,
            [
                getattr(order, value)
                for value in DataMappingValues.dish_quantity_field_names
            ],
        )
    }
    dish_prices = {
        key: value or FormDefaultValues.DISH_QUANTIRY_NOT_CHOSEN_DEFAULT_VALUE
        for key, value in zip(
            DataMappingValues.dish_price_field_names,
            [
                get_dish_price(
                    dish_value=getattr(order, field_name), dish_type=field_name
                )
                for field_name in DataMappingValues.dish_field_names
            ],
        )
    }

    return {**dish_quantities, **dish_prices}


def get_current_week_dates() -> list[date]:
    """
    Returns current week dates
    :return: list[datetime]
    """
    today = date.today()
    current_weekday = today.weekday()
    start_of_week = today + timedelta(days=7 - current_weekday)

    return [start_of_week + timedelta(days=i) for i in range(5)]


def get_days_dict() -> dict[str, int]:
    """
    Returns a dict with day names as key and day dates as value
    :return: dict[str, int]
    """
    return {
        day: value.day
        for day, value in zip(ViewSettingValues.WEEKDAY_NAMES, get_current_week_dates())
    }


def get_dates_dict() -> dict[str, str]:
    """
    Returns a dict with day names as key and day dates as value
    :return: dict[str, date]
    """
    return {
        day: value.strftime("%Y-%m-%d")
        for day, value in zip(ViewSettingValues.WEEKDAY_NAMES, get_current_week_dates())
    }


def validate_file_extension(uploaded_file: InMemoryUploadedFile) -> None:
    """
    Validates the uploaded menu file extension
    :param uploaded_file: InMemoryUploadedFile
    :return: None
    """
    if (
        next(iter(reversed(uploaded_file.name.split("."))))
        not in ValidationValues.valid_file_extensions
    ):
        raise ValidationError(
            ValidationMessages.INVALID_FILE_EXTENSION.format(
                valid_extensions=", ".join(ValidationValues.valid_file_extensions)
            )
        )


def validate_file_size(uploaded_file: InMemoryUploadedFile) -> None:
    """
    Validates the uploaded menu file size
    :param uploaded_file: InMemoryUploadedFile
    :return: None
    """
    if uploaded_file.size > ValidationValues.max_file_size:
        raise ValidationError(
            ValidationMessages.TOO_BIG_FILE_SIZE.format(
                max_size=ValidationValues.max_file_size // ValidationValues.one_megabyte
            )
        )


def validate_column_names_correspondence(data: pd.DataFrame) -> None:
    """
    Validates the uploaded menu file column names
    :param data: pd.DataFrame
    :return: None
    """
    if (column_names := tuple(data.keys())) != ValidationValues.ALL_FILE_FIELDS:
        raise ValidationError(
            ValidationMessages.INVALID_COLUMNS_FORMAT.format(
                column_names=", ".join(column_names)
            )
        )


def validate_dish_values(data: pd.DataFrame) -> None:
    """
    Validates the uploaded menu dish values
    :param data: pd.DataFrame
    :return: None
    """
    for field in DataMappingValues.dish_field_names:
        for index, value in enumerate(tuple(data.get(field))):
            if str(value) == "nan":
                raise ValidationError(
                    ValidationMessages.EMPTY_DISH_NAME.format(field=field)
                )

            if len(value) < ValidationValues.MINIMAL_DISH_NAME_LENGTHS[index]:
                raise ValidationError(
                    ValidationMessages.INVALID_DISH_NAME_LENGTH.format(
                        value=value,
                        field=field,
                        minimal_length=ValidationValues.MINIMAL_DISH_NAME_LENGTHS[
                            index
                        ],
                    )
                )


def validate_dish_prices(data: pd.DataFrame) -> None:
    """
    Validates the uploaded menu dish prices
    :param data: pd.DataFrame
    :return: None
    """
    for field in DataMappingValues.dish_price_field_names:
        for index, value in enumerate(tuple(data.get(field))):
            if int(value) < ValidationValues.MININMAL_DISH_PRICES[index]:
                raise ValidationError(
                    ValidationMessages.INVALID_DISH_PRICE.format(
                        value=value,
                        field=field,
                        minimal_price=ValidationValues.MININMAL_DISH_PRICES[index],
                    )
                )


def get_menu_choices(field_name: str) -> tuple:
    """
    Returns a tuple of choices for `forms.ChoiceField` based on `field_name`.
    :param field_name: The field name to get choices for.
    :return: A tuple of choices for `forms.ChoiceField` based on `field_name`.
    """
    return tuple(
        [("", "Select a dish")]
        + [
            (value_, value_)
            for value_ in Menu.objects.values_list(field_name, flat=True)
        ]
    )
