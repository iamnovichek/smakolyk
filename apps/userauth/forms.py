from django.core.exceptions import ValidationError
from django import forms

from phonenumber_field.formfields import PhoneNumberField

from .models import CustomUser, UserProfile


class CustomSignupForm(forms.ModelForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = PhoneNumberField(required=True)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['email']

    def clean(self):
        cleaned_data = super(CustomSignupForm, self).clean()
        username = cleaned_data.get('username')
        phone = cleaned_data.get('phone')

        if UserProfile.objects.filter(username=username).exists():
            raise ValidationError("Current username is already taken!")

        if UserProfile.objects.filter(phone=phone).exists():
            raise ValidationError("Current phone number is already taken!")

    def save(self, commit=True):
        if commit:
            user = CustomUser.objects.create_user(
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password1']
            )

            UserProfile.objects.create(
                user=user,
                username=self.cleaned_data['username'],
                first_name=(self.cleaned_data['first_name'][0].capitalize() +
                            self.cleaned_data['first_name'][1:]),
                last_name=(self.cleaned_data['last_name'][0].capitalize() +
                           self.cleaned_data['last_name'][1:]),
                phone=self.cleaned_data['phone']
            )

            return user
