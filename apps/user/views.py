from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import login
from django.contrib import messages

from .forms import CustomSignupForm, EditProfileForm
from .values import ValidationMessages


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = "login.html"
    success_url = "home"

    def form_invalid(self, form):
        messages.error(self.request, ValidationMessages.invalid_login_form_message)

        return super().form_invalid(form)


class CustomSignupView(CreateView):
    form_class = CustomSignupForm
    success_url = "success"
    template_name = "signup.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        return render(request, self.template_name, context={"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect(self.success_url)

        return render(
            request,
            self.template_name,
            {"form": form, "errors": [value for value in form.errors.values()]},
        )


class ProfileView(CreateView):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class EditProfileView(UpdateView):
    form_class = EditProfileForm
    template_name = "edit_profile.html"
    slug_url_kwarg = "slug"
    success_url = "profile"

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user.userprofile)

        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        if form.is_valid():
            form.save()

            return redirect(self.success_url)

        return render(
            request,
            self.template_name,
            {"form": form, "errors": [value for value in form.errors.values()]},
        )
