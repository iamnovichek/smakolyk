import pandas as pd
from celery import shared_task
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import EmailMessage
from django.db import transaction

from .models import Menu, Order
from .values import (
    MENU_UPLOADED_CELERY_MESSAGE,
    ORDERS_SENT_CELERY_MESSAGE,
    OUTPUT_ORDERS_FILE_DIR,
    ViewSettingValues,
)


def agrigate_orders() -> dict[str, list]:
    """
    Returns all existing orders and remove them from the DB
    :return: dict[str, list]
    """
    agregated_orders = dict()
    agregated_orders["names"] = list()

    with transaction.atomic():
        for field_name in ViewSettingValues.ORDER_FORM_FIELDS:
            agregated_orders[field_name] = Order.objects.values_list(
                field_name, flat=True
            )

        for order in Order.objects.all():
            agregated_orders["names"].append(
                f"{order.user.userprofile.first_name} {order.user.userprofile.last_name}"
            )

        Order.objects.all().delete()

    return agregated_orders


@shared_task()
def upload_menu_task(uploaded_file: InMemoryUploadedFile) -> str:
    """
    Parses an uploaded file and writes it to the DB
    :param uploaded_file: InMemoryUploadedFile
    :return: str
    """
    data_frame = pd.read_excel(uploaded_file)

    with transaction.atomic():
        Menu.objects.all().delete()

        created_objects = list()
        for _, row in data_frame.iterrows():
            new_menu = Menu(
                first_course=row.get("first_course", ""),
                first_course_price=row.get("first_course_price", None),
                second_course=row.get("second_course", ""),
                second_course_price=row.get("second_course_price", None),
                dessert=row.get("dessert", ""),
                dessert_price=row.get("dessert_price", None),
                drink=row.get("drink", ""),
                drink_price=row.get("drink_price", None),
            )
            created_objects.append(new_menu)

        Menu.objects.bulk_create(created_objects)

    return MENU_UPLOADED_CELERY_MESSAGE


@shared_task()
def send_orders_task() -> str:
    """
    A scheduled task that sends all orders to catering company
    :return: str
    """
    pd.DataFrame(agrigate_orders()).to_excel(OUTPUT_ORDERS_FILE_DIR, index=False)

    email = EmailMessage(
        subject="Orders",
        body="Orders for current week:",
        from_email=settings.EMAIL_HOST_USER,
        to=[settings.ORDERS_RECEIVER],
    )

    email.attach_file(OUTPUT_ORDERS_FILE_DIR)
    email.send(fail_silently=False)

    return ORDERS_SENT_CELERY_MESSAGE
