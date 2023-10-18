import os

from datetime import datetime

from django.core.exceptions import ValidationError
from django import forms

from apps.userauth.models import UserProfile


class CustomImageWidget(forms.ClearableFileInput):
    initial_text = ""
    input_text = ""
    clear_checkbox_label = ""
    # template_name = "apps.smakolyk/custom_image_field.html"


class ProfileUpdateForm(forms.ModelForm):
    photo = forms.ImageField(widget=CustomImageWidget)

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.userprofile = UserProfile.objects.get(user=self.instance.user)
        self.fields['username'].initial = self.userprofile.username
        self.fields['first_name'].initial = self.userprofile.first_name
        self.fields['last_name'].initial = self.userprofile.last_name
        self.fields['birthdate'].initial = self.userprofile.birthdate
        self.fields['phone'].initial = self.userprofile.phone

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'first_name',
            'last_name',
            'birthdate',
            'photo',
            'phone'
        ]

    def clean(self):
        cleaned_data = super(ProfileUpdateForm, self).clean()
        username = cleaned_data.get('username')
        birthday = cleaned_data.get('birthdate')
        phone = cleaned_data.get('phone')
        userprofile = UserProfile.objects.get(user=self.instance.user)
        if birthday:
            cleaned_birthday = datetime.strptime(str(birthday), __format="%Y-%m-%d").date()

            if self._is_too_young(cleaned_birthday) or self._is_too_old(cleaned_birthday):
                raise ValidationError("Enter a valid date!")

        if userprofile.username != username:
            if UserProfile.objects.filter(username=username).exists():
                raise ValidationError("Current username is already taken!")

        if userprofile.phone != phone:
            if UserProfile.objects.filter(phone=phone).exists():
                raise ValidationError("Current phone number is already taken!")

        return cleaned_data

    def save(self, commit=True):
        if commit:
            try:
                os.remove(f"{os.getcwd()}/{self.userprofile.photo.url}")
            except (FileNotFoundError, ValueError):
                pass
            self.userprofile.username = self.cleaned_data['username']
            self.userprofile.first_name = self.cleaned_data['first_name']
            self.userprofile.last_name = self.cleaned_data['last_name']
            self.userprofile.birthdate = self.cleaned_data['birthdate']
            self.userprofile.phone = self.cleaned_data['phone']
            self.userprofile.photo = self.cleaned_data['photo']
            self.userprofile.save()

    @staticmethod
    def _is_too_young(birthdate):
        today_ = datetime.today()
        age = today_.year - birthdate.year - ((today_.month, today_.day)
                                              < (birthdate.month, birthdate.day))
        return age < 18

    @staticmethod
    def _is_too_old(birthday):
        today_ = datetime.today()
        age = today_.year - birthday.year - ((today_.month, today_.day)
                                             < (birthday.month, birthday.day))
        return age > 90
