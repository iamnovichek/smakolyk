from django.db import models

from apps.shared.models import AbstractModel
from apps.user.models import CustomUser


class Order(AbstractModel):
    user = models.ForeignKey(CustomUser, related_name="order", on_delete=models.CASCADE)
    date = models.DateField()
    first_course = models.CharField(blank=True, max_length=30)
    first_course_quantity = models.PositiveIntegerField(default=0)
    second_course = models.CharField(blank=True, max_length=30)
    second_course_quantity = models.PositiveIntegerField(blank=True, default=0)
    dessert = models.CharField(blank=True, max_length=30)
    dessert_quantity = models.PositiveIntegerField(blank=True, default=0)
    drink = models.CharField(blank=True, max_length=30)
    drink_quantity = models.PositiveIntegerField(blank=True, default=0)

    class Meta:
        app_label = "smakolyk"

    def __str__(self):
        return f"{self.user.userprofile}'s order on {self.date}"


class Menu(AbstractModel):
    first_course = models.CharField(max_length=100, unique=True)
    first_course_price = models.PositiveIntegerField()
    second_course = models.CharField(max_length=100, unique=True)
    second_course_price = models.PositiveIntegerField()
    dessert = models.CharField(max_length=100, unique=True)
    dessert_price = models.PositiveIntegerField()
    drink = models.CharField(max_length=100, unique=True)
    drink_price = models.PositiveIntegerField()

    def __repr__(self):
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
    first_course = models.CharField(blank=True, max_length=100)
    first_course_quantity = models.PositiveIntegerField(default=0)
    second_course = models.CharField(blank=True, max_length=100)
    second_course_quantity = models.PositiveIntegerField(default=0)
    dessert = models.CharField(blank=True, max_length=100)
    dessert_quantity = models.PositiveIntegerField(default=0)
    drink = models.CharField(blank=True, max_length=100)
    drink_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.userprofile}'s history order on {self.date}"
