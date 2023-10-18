from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="apps.smakolyk/welcome.html"), name='welcome'),
    path('smakolyk/', TemplateView.as_view(template_name="apps.smakolyk/home.html"), name='home'),
]
