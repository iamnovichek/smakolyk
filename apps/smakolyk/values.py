import os
from dataclasses import dataclass

from django.conf import settings

OUTPUT_ORDERS_FILE_DIR = os.path.join(settings.BASE_DIR, "orders.xlsx")
ORDERS_SENT_CELERY_MESSAGE: str = "Orders sent"
MENU_UPLOADED_CELERY_MESSAGE: str = "Menu uploaded"


@dataclass(frozen=True)
class FormDefaultValues:
    DISH_NOT_CHOSEN_DEFAULT_VALUE: str = "Not chosen"
    DISH_QUANTIRY_NOT_CHOSEN_DEFAULT_VALUE: int = 0


@dataclass(frozen=True)
class ValidationValues:
    # Menu validation values
    first_course_max_length_value: int = 100
    first_course_min_length_value: int = 1
    first_course_min_price_value: int = 1
    first_course_quantity_default_value: int = 0
    second_course_max_length_value: int = 100
    second_course_min_length_value: int = 1
    second_course_min_price_value: int = 1
    second_course_quantity_default_value: int = 0
    dessert_max_length_value: int = 100
    dessert_min_length_value: int = 1
    dessert_min_price_value: int = 1
    dessert_quantity_default_value: int = 0
    drink_max_length_value: int = 100
    drink_min_length_value: int = 1
    drink_min_price_value: int = 1
    drink_quantity_default_value: int = 0

    # Uploaded file validation values
    one_megabyte: int = 1_048_576
    max_file_size: int = one_megabyte * 10
    valid_file_extensions: tuple[str, ...] = ("xlsx", "xls")

    # CONSTANTS
    MINIMAL_DISH_NAME_LENGTHS: tuple[int, ...] = (
        first_course_min_length_value,
        second_course_min_length_value,
        dessert_min_length_value,
        drink_min_length_value,
    )
    MININMAL_DISH_PRICES: tuple[int, ...] = (
        first_course_min_price_value,
        second_course_min_price_value,
        dessert_min_price_value,
        drink_min_price_value,
    )
    ALL_FILE_FIELDS: tuple[str, ...] = (
        "first_course",
        "first_course_price",
        "second_course",
        "second_course_price",
        "dessert",
        "dessert_price",
        "drink",
        "drink_price",
    )


@dataclass(frozen=True)
class ViewSettingValues:
    CHUNK_MENU_SIZE: int = 3
    FRIDAY_WEEKDAY_NUMBER: int = 4
    WEEKEND_START_HOUR: int = 18
    FORMS_NUMBER: int = 5
    MAX_ORDER_AMOUNT: int = 200  # in UAH
    MIN_ORDER_VALUE: int = 0
    WEEKDAY_NAMES: tuple[str, ...] = (
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
    )
    ORDER_FORM_FIELDS: tuple[str, ...] = (
        "first_course",
        "first_course_quantity",
        "second_course",
        "second_course_quantity",
        "dessert",
        "dessert_quantity",
        "drink",
        "drink_quantity",
        "date",
    )
    HISTORY_OBJECT_FIELDS: tuple[str, ...] = (
        "first_course",
        "first_course_quantity",
        "first_course_price",
        "second_course",
        "second_course_quantity",
        "second_course_price",
        "dessert",
        "dessert_quantity",
        "dessert_price",
        "drink",
        "drink_quantity",
        "drink_price",
        "date",
        "total_amount",
    )


@dataclass(frozen=True)
class DataMappingValues:
    dish_quantity_field_names: tuple[str, ...] = (
        "first_course_quantity",
        "second_course_quantity",
        "dessert_quantity",
        "drink_quantity",
    )
    dish_price_field_names: tuple[str, ...] = (
        "first_course_price",
        "second_course_price",
        "dessert_price",
        "drink_price",
    )
    dish_field_names: tuple[str, ...] = (
        "first_course",
        "second_course",
        "dessert",
        "drink",
    )


@dataclass(frozen=True)
class EmailSenderTemplates:
    OVERSUM_SUBJECT: str = "Oversum"
    OVERSUM_ACCOUNTANT_MESSAGE: str = (
        "{first_name} {last_name}\n-> {max_sum} ₴ max_sum."
    )
    OVERSUM_USER_MESSAGE: str = (
        "Dear {first_name} {last_name},\nyou did {max_sum} ₴ max_sum for {order_date}. The difference will bededucted from your salary."
    )


@dataclass(frozen=True)
class ValidationMessages:
    TOO_BIG_FILE_SIZE: str = "The file size if too big! Max size is {max_size} MB."
    INVALID_FILE_EXTENSION: str = (
        "Invalid file extension! Valid extensions are {valid_extensions}."
    )
    INVALID_COLUMNS_FORMAT: str = (
        f"Invalid column names: {{column_names}}. "
        f"Expected: {', '.join(ValidationValues.ALL_FILE_FIELDS)}."
    )
    INVALID_DISH_NAME_LENGTH: str = (
        "The value '{value}' in the column '{field}' is too short! "
        "Minimal length is {minimal_length}."
    )
    INVALID_DISH_PRICE: str = (
        "The value '{value}' in the column '{field}' is too small! "
        "Minimal price is {minimal_price}."
    )
    EMPTY_DISH_NAME: str = "The value in the column '{field}' cannot be empty!"
