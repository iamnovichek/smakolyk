from django.db import models

from apps.shared.models import AbstractModel
from apps.user.models import CustomUser

from .values import ValidationValues


class Order(AbstractModel):
    user = models.ForeignKey(CustomUser, related_name="order", on_delete=models.CASCADE)
    date = models.DateField()
    first_course = models.CharField(
        max_length=ValidationValues.first_course_max_length_value
    )
    first_course_quantity = models.PositiveIntegerField(
        default=ValidationValues.first_course_quantity_default_value
    )
    second_course = models.CharField(
        max_length=ValidationValues.second_course_max_length_value
    )
    second_course_quantity = models.PositiveIntegerField(
        default=ValidationValues.second_course_quantity_default_value
    )
    dessert = models.CharField(max_length=ValidationValues.dessert_max_length_value)
    dessert_quantity = models.PositiveIntegerField(
        default=ValidationValues.dessert_quantity_default_value
    )
    drink = models.CharField(max_length=ValidationValues.drink_max_length_value)
    drink_quantity = models.PositiveIntegerField(
        default=ValidationValues.drink_quantity_default_value
    )

    class Meta:
        app_label = "smakolyk"

    def __str__(self):
        return f"{self.user.userprofile}'s order on {self.date}"


class Menu(AbstractModel):
    first_course = models.CharField(
        max_length=ValidationValues.first_course_max_length_value, unique=True
    )
    first_course_price = models.PositiveIntegerField()
    second_course = models.CharField(
        max_length=ValidationValues.second_course_max_length_value, unique=True
    )
    second_course_price = models.PositiveIntegerField()
    dessert = models.CharField(
        max_length=ValidationValues.dessert_max_length_value, unique=True
    )
    dessert_price = models.PositiveIntegerField()
    drink = models.CharField(
        max_length=ValidationValues.drink_max_length_value, unique=True
    )
    drink_price = models.PositiveIntegerField()

    def __str__(self):
        return (
            f"Menu({self.first_course}, "
            f"{self.first_course_price}, "
            f"{self.second_course}, "
            f"{self.second_course_price}, "
            f"{self.dessert}, "
            f"{self.dessert_price}, "
            f"{self.drink}, "
            f"{self.drink_price})"
        )


class History(AbstractModel):
    user = models.ForeignKey(
        CustomUser, related_name="history", on_delete=models.CASCADE
    )
    date = models.DateField()
    total_amount = models.PositiveIntegerField()
    first_course = models.CharField(
        max_length=ValidationValues.first_course_max_length_value
    )
    first_course_quantity = models.PositiveIntegerField(
        default=ValidationValues.first_course_quantity_default_value
    )
    first_course_price = models.PositiveIntegerField()
    second_course = models.CharField(
        max_length=ValidationValues.second_course_max_length_value
    )
    second_course_quantity = models.PositiveIntegerField(
        default=ValidationValues.second_course_quantity_default_value
    )
    second_course_price = models.PositiveIntegerField()
    dessert = models.CharField(max_length=ValidationValues.dessert_max_length_value)
    dessert_quantity = models.PositiveIntegerField(
        default=ValidationValues.dessert_quantity_default_value
    )
    dessert_price = models.PositiveIntegerField()
    drink = models.CharField(max_length=ValidationValues.drink_max_length_value)
    drink_quantity = models.PositiveIntegerField(
        default=ValidationValues.drink_quantity_default_value
    )
    drink_price = models.PositiveIntegerField()

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.userprofile}'s history order on {self.date}"
