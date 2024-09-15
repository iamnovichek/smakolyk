from datetime import datetime, time, timedelta

import pandas as pd
from django import forms
from django.contrib import admin
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Menu
from .tasks import upload_menu_task
from .utils import (
    validate_column_names_correspondence,
    validate_dish_prices,
    validate_dish_values,
    validate_file_extension,
    validate_file_size,
)
from .values import ViewSettingValues


class UploadMenuForm(forms.ModelForm):
    file = forms.FileField(required=True)

    class Meta:
        model = Menu
        fields = ["file"]

    def clean_file(self) -> InMemoryUploadedFile:
        """
        Validates the uploaded menu file
        :return: InMemoryUploadedFile
        """
        uploaded_file = self.cleaned_data.get("file", "")

        # File scope validation
        validate_file_extension(uploaded_file)
        validate_file_size(uploaded_file)

        # File content scope validation
        data: pd.DataFrame = pd.read_excel(uploaded_file)

        validate_column_names_correspondence(data)
        validate_dish_values(data)
        validate_dish_prices(data)

        return uploaded_file


@admin.register(Menu)
class UploadedMenuAdmin(admin.ModelAdmin):
    form = UploadMenuForm

    def save_model(self, request, obj, form, change):
        """
        Overriding the save_model method to handle the uploaded file
        :param request: HttpRequest
        :param obj: Menu
        :param form: UploadMenuForm
        :param change: bool
        :return: None
        """
        uploaded_file = form.cleaned_data.get("file", "")

        upload_menu_task.apply_async(
            args=[uploaded_file], countdown=self.get_countdown_time()
        )

    @classmethod
    def get_countdown_time(cls) -> int:
        """
        Returns the countdown time in seconds
        :return: int
        """
        if datetime.now().weekday() >= ViewSettingValues.FRIDAY_WEEKDAY_NUMBER:
            if datetime.now().weekday() > ViewSettingValues.FRIDAY_WEEKDAY_NUMBER:
                return 0
            if (
                datetime.now().weekday() == ViewSettingValues.FRIDAY_WEEKDAY_NUMBER
                and datetime.now().time().hour >= ViewSettingValues.WEEKEND_START_HOUR
            ):
                return 0
            if (
                datetime.now().weekday() == ViewSettingValues.FRIDAY_WEEKDAY_NUMBER
                and datetime.now().time().hour < ViewSettingValues.WEEKEND_START_HOUR
            ):
                return cls.get_seconds_till_weekend_begin()

            return cls.get_seconds_till_weekend_begin()

    @staticmethod
    def get_seconds_till_weekend_begin() -> int:
        """
        Returns the number of seconds till weekend begin
        :return: int
        """
        today = datetime.now()
        last_weekday = datetime.combine(
            today.date(), time(ViewSettingValues.WEEKEND_START_HOUR, minute=0)
        ) + timedelta(
            days=(ViewSettingValues.FRIDAY_WEEKDAY_NUMBER - today.weekday())
            % 7  # 7 -> number of days in one week
        )

        time_difference = last_weekday - today

        return int(time_difference.total_seconds())
