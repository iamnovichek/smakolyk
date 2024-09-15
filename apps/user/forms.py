import os

from django import forms
from django.db import transaction
from phonenumber_field.formfields import PhoneNumberField

from .models import CustomUser, UserProfile
from .utils import EditProfileFieldsValidator, SignUpFieldsDataValidator
from .values import ValidationValues


class CustomSignupForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(
        max_length=ValidationValues.username_max_length,
        min_length=ValidationValues.username_min_length,
    )
    first_name = forms.CharField(
        max_length=ValidationValues.first_name_max_length,
        min_length=ValidationValues.first_name_min_length,
    )
    last_name = forms.CharField(
        max_length=ValidationValues.last_name_max_length,
        min_length=ValidationValues.last_name_min_length,
    )
    phone = PhoneNumberField(max_length=ValidationValues.phone_max_length)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ["email"]

    def clean(self):
        cleaned_data = super(CustomSignupForm, self).clean()

        SignUpFieldsDataValidator.validate(cleaned_data)

        return cleaned_data

    def save(self, commit=True):
        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=self.cleaned_data.get("email", ""),
                password=self.cleaned_data.get("password1", ""),
            )

            UserProfile.objects.create(
                user=user,
                username=self.cleaned_data.get("username", ""),
                first_name=(self.cleaned_data.get("first_name", "").capitalize()),
                last_name=(self.cleaned_data.get("last_name", "").capitalize()),
                phone=self.cleaned_data.get("phone", ""),
            )

            return user


class EditProfileForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.FileInput())

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.userprofile = UserProfile.objects.filter(user=self.instance.user).first()

        for field in self.fields:
            self.fields[field].initial = getattr(self.userprofile, field)

    class Meta:
        model = UserProfile
        fields = ["username", "first_name", "last_name", "birthdate", "photo", "phone"]

    def clean(self):
        cleaned_data = super(EditProfileForm, self).clean()

        EditProfileFieldsValidator.validate(cleaned_data, self.userprofile)

        return cleaned_data

    def _remove_old_profile_photo(self):
        if self.userprofile.photo != "default.png":
            os.remove(os.path.join(os.getcwd(), self.userprofile.photo.path))

    def save(self, commit=True):
        with transaction.atomic():
            super().save(commit=False)

            self._remove_old_profile_photo()

            for field in self.fields:
                setattr(self.userprofile, field, self.cleaned_data[field])

            self.userprofile.save()

            return self.userprofile
