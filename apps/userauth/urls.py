from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.urls import path

from .views import CustomLoginView, CustomSignupView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', CustomSignupView.as_view(), name='signup'),
    path('success-register/', TemplateView.as_view(
        template_name='apps.userauth/success.html'), name='success')
]
