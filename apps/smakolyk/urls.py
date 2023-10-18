from django.views.generic import TemplateView
from django.urls import path

from .views import ProfileView


urlpatterns = [
    path('', TemplateView.as_view(template_name="apps.smakolyk/welcome.html"), name='welcome'),
    path('smakolyk/', TemplateView.as_view(template_name="apps.smakolyk/home.html"), name='home'),
    path('my-profile/', ProfileView.as_view(), name='profile'),
]
