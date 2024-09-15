from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from .views import CustomLoginView, CustomSignupView, EditProfileView, ProfileView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", CustomSignupView.as_view(), name="signup"),
    path(
        "success-register/",
        TemplateView.as_view(template_name="success.html"),
        name="success",
    ),
    path("my-profile/", ProfileView.as_view(), name="profile"),
    path("edit-profile/<slug:slug>", EditProfileView.as_view(), name="edit-profile"),
]
